# 04 — Mandatory Section: What is Misleading About the Headline Number?

> **Headline Number**: **0.8500 Intent Accuracy** & **0.6510 Macro F1**

While achieving an **0.8500 Intent Accuracy** demonstrates strong performance over classical ML baselines, headline metrics in AI customer-support systems can be inherently misleading if interpreted without context.

---

## 1. Class Imbalance Distorts Aggregate Accuracy

In real-world Twitter support datasets, customer queries are heavily skewed towards high-volume categories like `software_update_issue` and `battery_drain`. 

A simple model that performs exceptionally well on frequent classes can achieve high overall accuracy while performing poorly on rare classes like `hardware_repair` or `wifi_connectivity`.

---

## 2. Accuracy Masks False Auto-Handling Operational Risks

Accuracy treats all classification errors equally. In customer support:
* Misclassifying a general OS update query is a minor annoyance.
* **Incorrectly auto-handling a high-risk legal dispute or battery explosion hazard is a catastrophic failure.**

A system with 90% accuracy that auto-handles 5% of high-risk cases is far more dangerous than an 80% accurate system that safely escalates 100% of high-risk cases.

---

## 3. Historical Support Text is Not Absolute Ground Truth

Twitter support interactions frequently consist of generic brand requests asking customers to send a Direct Message (DM). 

A high retrieval similarity score confirms that the agent matches historical Twitter response behavior, but does not guarantee that the underlying issue was fully resolved in the public tweet.

---

## 4. Single-Brand Evaluation Bias

The golden evaluation set is constructed around `AppleSupport`. High performance on technology support queries does not automatically transfer to distinct domains (e.g. airlines, retail, or financial services) without custom taxonomy discovery and retrieval index construction.
