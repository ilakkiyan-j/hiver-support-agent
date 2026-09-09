from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Type, List
import json
import logging
from pydantic import BaseModel
from configs.settings import settings

logger = logging.getLogger(__name__)

class LLMProvider(ABC):
    """
    Abstract interface for replaceable LLM backends.
    """
    @abstractmethod
    def generate(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        pass

    @abstractmethod
    def generate_structured(
        self,
        prompt: str,
        response_schema: Type[BaseModel],
        system_instruction: Optional[str] = None
    ) -> BaseModel:
        pass


FALLBACK_MODELS = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-3.6-flash"]

class GeminiProvider(LLMProvider):
    """
    Google Gemini SDK implementation with automatic model fallback and structured output validation.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None
    ):
        if api_key is not None:
            self.api_key = api_key
        else:
            self.api_key = settings.GEMINI_API_KEY

        self.model_name = model_name or settings.LLM_MODEL
        self._client = None
        self._genai_type = None

        if self.api_key and self.api_key != "mock":
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
                self._genai_type = "new"
                logger.info(f"Initialized Gemini Client using google.genai SDK.")
            except Exception as e:
                try:
                    import google.generativeai as ggenai
                    ggenai.configure(api_key=self.api_key)
                    self._client = ggenai.GenerativeModel(self.model_name)
                    self._genai_type = "legacy"
                    logger.info(f"Initialized Gemini Client using legacy google.generativeai SDK.")
                except Exception as ex:
                    logger.warning(f"Could not initialize Gemini SDK: {ex}")

    def generate(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        if not self._client or not self.api_key or self.api_key == "mock":
            logger.warning("No active Gemini API key. Returning deterministic mock response.")
            return "Mock response: Gemini API call simulated."

        candidate_models = [self.model_name] + [m for m in FALLBACK_MODELS if m != self.model_name]
        
        last_error = None
        for model in candidate_models:
            try:
                if self._genai_type == "new":
                    config = {}
                    if system_instruction:
                        config["system_instruction"] = system_instruction
                    response = self._client.models.generate_content(
                        model=model,
                        contents=prompt,
                        config=config if config else None
                    )
                    return response.text
                else:
                    import google.generativeai as ggenai
                    gen_model = ggenai.GenerativeModel(model)
                    full_prompt = f"{system_instruction}\n\n{prompt}" if system_instruction else prompt
                    response = gen_model.generate_content(full_prompt)
                    return response.text

            except Exception as e:
                err_str = str(e)
                logger.warning(f"Gemini call with model '{model}' failed: {err_str[:150]}")
                last_error = e
                # Continue trying next fallback model if model 404/not found
                if "404" in err_str or "NOT_FOUND" in err_str or "not available" in err_str:
                    continue
                else:
                    break

        logger.error(f"All Gemini models failed. Last error: {last_error}")
        raise RuntimeError(f"Gemini API call failed: {last_error}")

    def generate_structured(
        self,
        prompt: str,
        response_schema: Type[BaseModel],
        system_instruction: Optional[str] = None
    ) -> BaseModel:
        json_instruction = (
            f"Respond ONLY with a valid JSON object strictly matching this schema:\n"
            f"{json.dumps(response_schema.model_json_schema(), indent=2)}\n"
            f"Do not include markdown code block formatting or extra commentary."
        )

        sys_prompt = f"{system_instruction}\n\n{json_instruction}" if system_instruction else json_instruction

        raw_output = self.generate(prompt, system_instruction=sys_prompt)
        
        # Clean markdown wrappers if present
        clean_json = raw_output.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json[7:]
        if clean_json.startswith("```"):
            clean_json = clean_json[3:]
        if clean_json.endswith("```"):
            clean_json = clean_json[:-3]
        clean_json = clean_json.strip()

        try:
            parsed_dict = json.loads(clean_json)
            return response_schema(**parsed_dict)
        except Exception as e:
            logger.error(f"Failed to parse structured response into {response_schema.__name__}: {e}. Raw output: {raw_output[:200]}")
            raise ValueError(f"Malformed LLM output: {e}")
