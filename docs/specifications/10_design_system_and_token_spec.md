# Design System & Token Specification

**Project:** HiverSupport Agent  
**Phase:** 04 — UX/UI Design  
**Document:** Design System & Token Specification  
**Status:** ✅ Completed  
**Owner:** Ilakkiyan J  
**Priority:** Required  

---

# 1. Purpose

This document defines the visual foundation for **HiverSupport Agent**.

The design system establishes a consistent language for:

- Colors
- Typography
- Spacing
- Borders
- Border radius
- Shadows
- Status badges
- Buttons
- Cards
- Inputs
- AI states
- Escalation states
- Evidence states
- Evaluation states
- CSS variables

The goal is to create an interface that feels **professional, trustworthy, technical, and calm**, while making AI decisions and uncertainty easy to understand.

---

# 2. Design Principles

## DS-001 — Evidence Should Be Visible

The interface should clearly distinguish between:

- Customer-provided information
- Historical evidence
- AI-generated content
- AI decisions
- Human decisions

The user should never have to guess where an AI response came from.

---

## DS-002 — Trust Through Transparency

AI confidence, retrieved evidence, and escalation reasons should be visible when relevant.

The design should avoid presenting AI decisions as unquestionable facts.

---

## DS-003 — Calm Over Decorative

Customer support is an operational environment.

The visual system should prioritize:

- Clarity
- Readability
- Hierarchy
- Focus
- Fast scanning

over unnecessary visual decoration.

---

## DS-004 — Status Must Be Immediately Understandable

Important states should be recognizable without requiring the user to read the entire interface.

Examples:

```text
AUTO-HANDLE
ESCALATE
REVIEW
HIGH CONFIDENCE
LOW CONFIDENCE
GROUNDED
INSUFFICIENT EVIDENCE
```

---

## DS-005 — Accessible by Default

Color must not be the only mechanism used to communicate meaning.

For example:

```text
✓ Auto-handle
! Escalate
? Review
```

should communicate the state even without relying solely on color.

---

# 3. Visual Direction

The HiverSupport Agent interface should communicate:

> **Intelligent + Trustworthy + Operational + Modern**

The visual language should combine:

- Clean SaaS-style layouts
- Strong typography
- Subtle borders
- Moderate corner rounding
- Compact information density
- Clear AI/evidence separation
- Minimal visual noise

The interface should feel more like a **professional support operations console** than a consumer chatbot.

---

# 4. Color System

## 4.1 Primary Color

The primary brand color is used for:

- Primary actions
- Active navigation
- Links
- Focus states
- Selected elements
- Important interactive controls

### Primary Scale

| Token | Value | Usage |
|---|---|---|
| `--color-primary-50` | `#F0F9FF` | Subtle background |
| `--color-primary-100` | `#E0F2FE` | Selected background |
| `--color-primary-200` | `#BAE6FD` | Light border |
| `--color-primary-300` | `#7DD3FC` | Secondary emphasis |
| `--color-primary-400` | `#38BDF8` | Interactive highlight |
| `--color-primary-500` | `#0EA5E9` | Primary brand |
| `--color-primary-600` | `#0284C7` | Primary hover |
| `--color-primary-700` | `#0369A1` | Active/pressed |
| `--color-primary-800` | `#075985` | Dark emphasis |
| `--color-primary-900` | `#0C4A6E` | Strongest emphasis |

---

# 5. Neutral Color System

Neutral colors form the majority of the interface.

| Token | Value | Usage |
|---|---|---|
| `--color-neutral-0` | `#FFFFFF` | Primary surface |
| `--color-neutral-50` | `#F8FAFC` | Application background |
| `--color-neutral-100` | `#F1F5F9` | Secondary surface |
| `--color-neutral-200` | `#E2E8F0` | Borders |
| `--color-neutral-300` | `#CBD5E1` | Strong borders |
| `--color-neutral-400` | `#94A3B8` | Placeholder/muted |
| `--color-neutral-500` | `#64748B` | Secondary text |
| `--color-neutral-600` | `#475569` | Supporting text |
| `--color-neutral-700` | `#334155` | Primary body text |
| `--color-neutral-800` | `#1E293B` | Heading text |
| `--color-neutral-900` | `#0F172A` | Strongest text |

---

# 6. Semantic Colors

Semantic colors communicate system state.

## Success

Used for successful, safe, or completed states.

| Token | Value |
|---|---|
| `--color-success-50` | `#F0FDF4` |
| `--color-success-100` | `#DCFCE7` |
| `--color-success-500` | `#22C55E` |
| `--color-success-600` | `#16A34A` |
| `--color-success-700` | `#15803D` |

---

## Warning

Used for uncertainty or states requiring attention.

| Token | Value |
|---|---|
| `--color-warning-50` | `#FFFBEB` |
| `--color-warning-100` | `#FEF3C7` |
| `--color-warning-500` | `#F59E0B` |
| `--color-warning-600` | `#D97706` |
| `--color-warning-700` | `#B45309` |

---

## Error

Used for failures and invalid states.

| Token | Value |
|---|---|
| `--color-error-50` | `#FEF2F2` |
| `--color-error-100` | `#FEE2E2` |
| `--color-error-500` | `#EF4444` |
| `--color-error-600` | `#DC2626` |
| `--color-error-700` | `#B91C1C` |

---

## Informational

Used for neutral system information.

| Token | Value |
|---|---|
| `--color-info-50` | `#EFF6FF` |
| `--color-info-100` | `#DBEAFE` |
| `--color-info-500` | `#3B82F6` |
| `--color-info-600` | `#2563EB` |
| `--color-info-700` | `#1D4ED8` |

---

# 7. AI-Specific Semantic States

AI states require additional semantic meaning.

| State | Semantic Meaning |
|---|---|
| `AI_READY` | Agent is ready |
| `AI_ANALYZING` | Agent is processing |
| `AI_GROUNDED` | Response has supporting evidence |
| `AI_LOW_CONFIDENCE` | AI confidence is insufficient |
| `AI_REVIEW` | Human review recommended |
| `AI_ESCALATE` | Human escalation required |
| `AI_ERROR` | AI processing failed |

These states should not depend exclusively on color.

---

# 8. Background Tokens

```css
:root {
  --surface-app: #F8FAFC;
  --surface-primary: #FFFFFF;
  --surface-secondary: #F1F5F9;
  --surface-tertiary: #E2E8F0;

  --surface-ai: #F0F9FF;
  --surface-success: #F0FDF4;
  --surface-warning: #FFFBEB;
  --surface-error: #FEF2F2;
  --surface-info: #EFF6FF;
}
```

---

# 9. Text Tokens

```css
:root {
  --text-primary: #0F172A;
  --text-secondary: #475569;
  --text-tertiary: #64748B;
  --text-muted: #94A3B8;
  --text-disabled: #CBD5E1;

  --text-on-primary: #FFFFFF;

  --text-success: #15803D;
  --text-warning: #B45309;
  --text-error: #B91C1C;
  --text-info: #1D4ED8;
}
```

---

# 10. Typography

## Font Family

Primary interface font:

```css
--font-family-sans:
  Inter,
  ui-sans-serif,
  system-ui,
  -apple-system,
  BlinkMacSystemFont,
  "Segoe UI",
  sans-serif;
```

The typography should prioritize readability across dense operational screens.

---

# 11. Typography Scale

| Token | Size | Line Height | Weight | Usage |
|---|---:|---:|---:|---|
| `--text-xs` | 12px | 16px | 400–500 | Metadata |
| `--text-sm` | 14px | 20px | 400–500 | Secondary text |
| `--text-md` | 16px | 24px | 400 | Body |
| `--text-lg` | 18px | 28px | 500 | Large body |
| `--text-xl` | 20px | 28px | 600 | Section title |
| `--text-2xl` | 24px | 32px | 600 | Page heading |
| `--text-3xl` | 30px | 36px | 600–700 | Major heading |
| `--text-4xl` | 36px | 40px | 700 | Hero/stat display |

---

# 12. Typography Roles

### Page Heading

```text
30px / 36px
Weight: 600–700
```

### Section Heading

```text
20px / 28px
Weight: 600
```

### Body

```text
16px / 24px
Weight: 400
```

### Metadata

```text
12–14px
Weight: 400–500
```

### AI Output

```text
15–16px
Line-height: 24px
```

AI-generated customer-facing text should remain highly readable and should not use excessively stylized typography.

---

# 13. Spacing System

The system uses a 4px base spacing unit.

| Token | Value |
|---|---:|
| `--space-1` | 4px |
| `--space-2` | 8px |
| `--space-3` | 12px |
| `--space-4` | 16px |
| `--space-5` | 20px |
| `--space-6` | 24px |
| `--space-8` | 32px |
| `--space-10` | 40px |
| `--space-12` | 48px |
| `--space-16` | 64px |
| `--space-20` | 80px |

---

# 14. Layout Spacing

Recommended spacing:

```text
Page padding:
24–32px

Section gap:
24–32px

Card padding:
16–24px

Component gap:
8–16px

Inline control gap:
8px
```

Dense data should use smaller spacing while major sections should receive more visual separation.

---

# 15. Border System

```css
:root {
  --border-subtle: #F1F5F9;
  --border-default: #E2E8F0;
  --border-strong: #CBD5E1;
  --border-focus: #0EA5E9;
}
```

### Usage

- `subtle` → internal separators
- `default` → cards and containers
- `strong` → emphasized boundaries
- `focus` → keyboard/input focus

---

# 16. Border Radius

| Token | Value | Usage |
|---|---:|---|
| `--radius-sm` | 6px | Small controls |
| `--radius-md` | 8px | Inputs/buttons |
| `--radius-lg` | 12px | Cards |
| `--radius-xl` | 16px | Large panels |
| `--radius-full` | 9999px | Badges/pills |

The default product radius should be approximately:

```css
--radius-default: 10px;
```

The interface should avoid excessive rounding that makes an operational application feel overly playful.

---

# 17. Shadow System

Shadows should be subtle.

```css
:root {
  --shadow-sm:
    0 1px 2px rgba(15, 23, 42, 0.05);

  --shadow-md:
    0 4px 12px rgba(15, 23, 42, 0.08);

  --shadow-lg:
    0 10px 24px rgba(15, 23, 42, 0.10);
}
```

### Usage

| Shadow | Usage |
|---|---|
| Small | Cards / controls |
| Medium | Dropdowns / popovers |
| Large | Modals / overlays |

Borders should carry most of the visual structure; shadows should be supportive rather than dominant.

---

# 18. Button Tokens

## Primary Button

Used for the main action.

```text
Background: Primary 500
Text: White
Radius: Medium
Height: 40px
Horizontal padding: 16px
```

States:

```text
Default
Hover
Pressed
Focus
Disabled
Loading
```

---

## Secondary Button

Used for secondary actions.

```text
Background: White
Border: Neutral 200
Text: Neutral 700
```

---

## Destructive Button

Used only for destructive operations.

```text
Background: Error 500
Text: White
```

Destructive actions should not be visually confused with escalation actions.

---

# 19. Input Tokens

Inputs should provide clear:

- Label
- Input area
- Placeholder
- Helper text
- Error state
- Focus state

### Default

```text
Height: 40px
Border: Neutral 200
Radius: 8px
Padding: 12px
```

### Focus

```text
Border: Primary 500
Focus ring: Primary 100
```

---

# 20. Badge System

Badges provide fast operational status recognition.

## Auto-Handle

```text
Label: Auto-handle
Semantic: Success
Icon: ✓
```

## Escalate

```text
Label: Escalate
Semantic: Error
Icon: ↑ / !
```

## Review

```text
Label: Review
Semantic: Warning
Icon: !
```

## Grounded

```text
Label: Grounded
Semantic: Success / Info
Icon: ✓
```

## Low Confidence

```text
Label: Low confidence
Semantic: Warning
Icon: ?
```

## Processing

```text
Label: Analyzing
Semantic: Info
Icon: Spinner
```

---

# 21. Badge CSS Pattern

```css
.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: 500;
}
```

Badge variants should use semantic tokens rather than hardcoded component-specific colors.

---

# 22. AI Response Card

The AI Response Card is a core HiverSupport Agent component.

### Structure

```text
┌─────────────────────────────────────┐
│ AI Draft Reply             Grounded │
│                                     │
│ "Sorry about the duplicate charge. │
│  Please send us your order..."      │
│                                     │
│ Evidence: 3 historical cases        │
│ Confidence: High                    │
│                                     │
│ [Edit] [Approve] [Escalate]         │
└─────────────────────────────────────┘
```

### Visual Requirements

- Clear AI label
- Grounding state
- Readable response text
- Evidence count
- Confidence information
- Clear actions

---

# 23. Evidence Card

Historical evidence should visually differ from AI-generated output.

### Structure

```text
┌─────────────────────────────────────┐
│ Historical Case #1842               │
│ Similarity: 0.89                    │
│                                     │
│ Customer:                            │
│ "I was charged twice..."            │
│                                     │
│ Brand Response:                     │
│ "Please DM your order details..."   │
│                                     │
│ View source →                       │
└─────────────────────────────────────┘
```

### Design Principle

Historical evidence should appear as **source material**, not as another AI response.

---

# 24. Escalation Card

The escalation state should be prominent without creating unnecessary alarm.

### Structure

```text
┌─────────────────────────────────────┐
│ ⚠ Escalation Recommended           │
│                                     │
│ Reason                              │
│ Insufficient historical evidence    │
│                                     │
│ Confidence: Low                    │
│                                     │
│ [Review Evidence] [Take Over]      │
└─────────────────────────────────────┘
```

---

# 25. Confidence Visualization

Confidence should be represented using:

- Numeric value
- Semantic label
- Optional progress indicator

Example:

```text
Confidence

91%
High
━━━━━━━━━━━━━━━━━━
```

Avoid implying that confidence is equivalent to correctness.

Where appropriate, the interface should label it explicitly:

> **Model confidence**

rather than simply:

> **Accuracy**

---

# 26. Navigation

The primary navigation should remain compact.

Recommended structure:

```text
HiverSupport Agent

Support
Evaluation
Knowledge
Experiments
Documentation
```

The active destination should have a clear visual state.

---

# 27. Cards

Cards are the primary container for grouped information.

### Default Card

```css
.card {
  background: var(--surface-primary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
}
```

Cards should not be nested excessively.

---

# 28. Tables

Tables should be used for:

- Evaluation metrics
- Experiment results
- Failure analysis
- Dataset statistics

Recommended characteristics:

- Clear column headers
- Compact row height
- Strong numeric alignment
- Hover state
- Responsive overflow handling

---

# 29. Empty States

Empty states should explain what is missing and what the user can do.

Example:

```text
No evaluation runs yet

Run your first evaluation to see
intent, response, and escalation metrics.

[Run Evaluation]
```

Avoid generic:

> "No data."

---

# 30. Loading States

AI processing should use explicit loading states.

Example:

```text
Analyzing conversation...

✓ Understanding intent
✓ Retrieving historical cases
● Generating response
○ Evaluating escalation
```

This provides useful feedback without exposing unnecessary internal implementation details.

---

# 31. Error States

Errors should explain:

1. What happened
2. Whether the request was completed
3. What the user can do next

Example:

```text
Unable to generate response

The AI service did not return a valid response.

[Retry]
```

Avoid exposing raw stack traces in the primary interface.

---

# 32. Accessibility Tokens

The design system should support:

- Keyboard navigation
- Visible focus states
- Screen-reader labels
- Sufficient text/background contrast
- Semantic HTML
- Non-color status communication
- Logical heading hierarchy
- Accessible interactive targets

Minimum interactive target recommendation:

```text
44 × 44px
```

for touch-oriented controls where practical.

---

# 33. Responsive Breakpoints

Recommended breakpoints:

| Token | Width |
|---|---:|
| `--breakpoint-sm` | 640px |
| `--breakpoint-md` | 768px |
| `--breakpoint-lg` | 1024px |
| `--breakpoint-xl` | 1280px |
| `--breakpoint-2xl` | 1536px |

---

# 34. Responsive Layout Strategy

## Desktop

Use a multi-column operational layout.

```text
┌──────────┬───────────────────────────────┐
│ Sidebar  │ Conversation                  │
│          │                               │
│          │ AI Analysis / Evidence        │
│          │                               │
└──────────┴───────────────────────────────┘
```

---

## Tablet

Collapse secondary information into stacked sections.

```text
┌─────────────────────────────┐
│ Conversation                │
├─────────────────────────────┤
│ AI Analysis                 │
├─────────────────────────────┤
│ Evidence                    │
├─────────────────────────────┤
│ Decision                    │
└─────────────────────────────┘
```

---

## Mobile

Prioritize:

1. Customer message
2. AI decision
3. Response
4. Evidence
5. Actions

Secondary metadata can collapse into expandable sections.

---

# 35. Dark Mode Consideration

Dark mode is not required for the MVP unless implementation time permits.

If introduced later, semantic tokens should be remapped rather than components receiving separate hardcoded dark-mode colors.

Example:

```css
[data-theme="dark"] {
  --surface-app: ...;
  --surface-primary: ...;
  --text-primary: ...;
  --border-default: ...;
}
```

---

# 36. Core CSS Variable Specification

```css
:root {
  /* Typography */
  --font-family-sans:
    Inter,
    ui-sans-serif,
    system-ui,
    sans-serif;

  /* Text */
  --text-primary: #0F172A;
  --text-secondary: #475569;
  --text-tertiary: #64748B;
  --text-muted: #94A3B8;

  /* Surfaces */
  --surface-app: #F8FAFC;
  --surface-primary: #FFFFFF;
  --surface-secondary: #F1F5F9;

  /* Brand */
  --color-primary-500: #0EA5E9;
  --color-primary-600: #0284C7;
  --color-primary-700: #0369A1;

  /* Semantic */
  --color-success-500: #22C55E;
  --color-warning-500: #F59E0B;
  --color-error-500: #EF4444;
  --color-info-500: #3B82F6;

  /* Borders */
  --border-default: #E2E8F0;
  --border-strong: #CBD5E1;
  --border-focus: #0EA5E9;

  /* Radius */
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;

  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;

  /* Shadows */
  --shadow-sm:
    0 1px 2px rgba(15, 23, 42, 0.05);

  --shadow-md:
    0 4px 12px rgba(15, 23, 42, 0.08);

  --shadow-lg:
    0 10px 24px rgba(15, 23, 42, 0.10);
}
```

---

# 37. Component State Standards

Every interactive component should consider:

```text
Default
Hover
Focus
Pressed
Disabled
Loading
Error
Success
```

AI-specific components should additionally consider:

```text
Analyzing
Grounded
Low Confidence
Review
Escalate
```

---

# 38. Visual Hierarchy

The interface should establish the following priority:

```text
1. Customer Problem
       ↓
2. AI Decision
       ↓
3. Draft Response
       ↓
4. Evidence
       ↓
5. Explanation / Metadata
       ↓
6. Secondary Information
```

This prevents supporting metadata from overpowering the actual support task.

---

# 39. Design System Do / Don't

## Do

- Use consistent spacing
- Use semantic colors
- Make AI-generated content identifiable
- Make evidence easy to inspect
- Show escalation reasons
- Maintain strong typography hierarchy
- Keep operational screens dense but readable
- Provide keyboard-accessible interactions

## Don't

- Use color as the only status indicator
- Hide AI uncertainty
- Make AI output look like human-approved content
- Overuse gradients
- Overuse shadows
- Use excessive rounded cards
- Add decorative UI without functional purpose
- Build a complex design system that the MVP does not need

---

# 40. Design Tokens Summary

The design system is built around five token categories:

```text
FOUNDATION
├── Colors
├── Typography
├── Spacing
├── Radius
└── Shadows

SEMANTIC
├── Success
├── Warning
├── Error
├── Information
└── AI States

COMPONENT
├── Buttons
├── Inputs
├── Cards
├── Badges
├── Tables
└── Navigation

AI EXPERIENCE
├── Confidence
├── Evidence
├── Grounding
├── Escalation
└── Decision states

ACCESSIBILITY
├── Focus
├── Contrast
├── Keyboard
├── Screen readers
└── Non-color communication
```

---

# 41. Completion Criteria

The Design System & Token Specification is considered complete when:

- [x] Color palette defined
- [x] Semantic colors defined
- [x] Typography scale defined
- [x] Spacing scale defined
- [x] Border tokens defined
- [x] Radius tokens defined
- [x] Shadow tokens defined
- [x] Badge states defined
- [x] AI states defined
- [x] CSS variables defined
- [x] Accessibility principles defined
- [x] Responsive breakpoints defined
- [x] Core component standards defined
- [x] AI-specific visual patterns defined

---

# 42. Final Design Principle

The HiverSupport Agent design system should make one idea visually obvious:

> **The AI is useful because it has evidence—not because it sounds confident.**

Every major design decision should reinforce that principle.

The interface should therefore make it easy to distinguish:

**What the customer said → What the AI understood → What evidence it found → What it recommends → Why it should answer or escalate.**

That visual transparency is the foundation of a trustworthy HiverSupport Agent experience.