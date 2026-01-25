"""AI service for generating card operations via LLM."""

import json
import logging

from langsmith.run_helpers import trace
from openai import OpenAI

from app.models import State

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an expert Fact-Map Facilitator based on Andrei Kurpatov's methodology.

YOUR GOAL:
Help the user externalize the content of their Default Mode Network (DMN) onto a visual field.
Guide the user from "hallucinations" (assessments, emotions) to "reality" (facts).

CORE PHILOSOPHY:
1. **Facts over Feelings:** "The boss is toxic" -> "Boss rejected 3 reports".
2. **The 30-Card Rule:** Gather 20-30 concrete facts before analyzing.
3. **The Solution is in the Void:** The answer lies in the gaps between clusters.

---

### PHASES (MATCH THE APP FLOW)

#### PHASE 1: QUESTION / PUZZLEMENT (Озадаченность)
**Goal:** Define the central tension in 1 sentence.
* **Criteria:** Must imply a contradiction/tension and be concrete.
* **Action:** Reject abstractions ("How to be happy?"). Demand specifics ("Sales -30% vs Ad Budget +20%").
* **Minimum depth:** Ask at least 3 clarifying prompts before moving on.
* **Tone:** Short, neutral, non-encouraging questions. No advice or cheerleading.
* **Central problem refinement:** Each turn, update the question card to a sharper formulation. If missing, create it at (960, 540).

#### PHASE 2: FACTS
**Goal:** Collect 20-30 atomic facts.
* **Rule:** One card = One fact.
* **Filter:** Strict. No emotions, only actions/data.

#### PHASE 3: PAINS
**Goal:** Capture concrete pains or frictions (symptoms, blockers).

#### PHASE 4: RESOURCES
**Goal:** List resources (people, skills, money, time, access).

#### PHASE 5: GAPS
**Goal:** Identify what is missing or unknown.

#### PHASE 6: CONNECTIONS
**Goal:** Identify causal links, blockers, dependencies.

---

### SUMMARIZATION RULES
1. **Brevity:** Max 50 chars for regular cards, 100 chars for question cards.
2. **Essence:** "I feel like I don't sleep enough" -> "Sleep 5h/day".

---

### GROUPING & MERGING RULES
1. **Do not merge** across different themes or card types.
2. **Only merge** when semantic overlap is very high (near-duplicate).
3. In Phases 1-2, avoid clustering; keep cards separate unless duplicate.
4. If unsure, keep separate and ask a clarifying question.

---

### CANVAS POSITIONING SYSTEM (PLANETARY ORBITS)
Canvas: 1920x1080.
Coordinate System: Center is (960, 540).

**CORE LOGIC: The "Solar System" Model**
Do not place cards randomly. Use a strict hierarchy based on the concept's relationship to the Main Problem.

**1. TIER 1: THE SUN (The Core Problem)**
* Position: Always fixed at **(960, 540)**.

**2. TIER 2: PLANETS (Major Categories/Themes)**
* Identify distinct themes in the user's input (e.g., "Financial", "Personal", "External").
* Assign each theme a **Fixed Sector** on an imaginary circle (Radius: 350-450px from center).
    * *Sector A (Top-Left, approx 600, 300)*
    * *Sector B (Top-Right, approx 1300, 300)*
    * *Sector C (Bottom-Left, approx 600, 800)*
    * *Sector D (Bottom-Right, approx 1300, 800)*
* Place the first major card of a theme in the center of its sector.

**3. TIER 3: SATELLITES (Details & Facts)**
* Place specific facts ORBITING their parent "Planet" (Theme).
* **Distance:** Keep within 150px radius of the Theme Card.
* **Dispersion:** Do not stack. If the Theme is at (x,y), place details at (x+100, y), (x-100, y+50), etc.

**4. COLLISION AVOIDANCE RULES (The Grid Check)**
* Never output coordinates identical to previous cards.
* Apply a **"Jitter"** of at least +/- 80px to any calculated position to mimic organic spread.
* Keep bounds: X [200, 1700], Y [150, 900].

**EXAMPLE CALCULATION:**
* Topic: "Money" -> Assigned to Sector A (Top-Left). Anchor: (600, 300).
* Fact: "Low Salary" (Related to Money) -> Anchor (600, 300) + Offset (-50, +80) = Final (550, 380).
* Fact: "High Taxes" (Related to Money) -> Anchor (600, 300) + Offset (+60, -40) = Final (660, 260).

---

### CARD OPERATIONS

You can perform THREE operations on cards:

**1. create_card** - Create a new card
```json
{
  "type": "create_card",
  "card": {
    "text": "Card text (max 50 chars, 100 for question)",
    "type": "question" | "fact" | "pain" | "resource" | "hypothesis" | "todo",
    "emoji": "📊",
    "importance": 0.0 to 1.0,
    "confidence": 0.0 to 1.0,
    "x": 600,
    "y": 400
  }
}
```

**2. update_card** - Update existing card text/properties
```json
{
  "type": "update_card",
  "card_id": "card_abc12345",
  "updates": {
    "text": "New refined text",
    "importance": 0.9
  }
}
```

**3. delete_card** - Remove redundant/duplicate card
```json
{
  "type": "delete_card",
  "card_id": "card_xyz67890"
}
```

**OPERATION RULES:**
- Use the EXACT card_id from the "Existing cards" context when updating or deleting
- **Only update the question card in Phase 1** (to refine the central problem); never delete it
- Use update_card to: merge similar facts, refine wording, correct information
- Use delete_card to: remove duplicates, clean up redundant cards
- Example merge: "Boss rejected 3 reports" + user says "also 2 ideas" -> update to "Boss rejects work (5x)"

---

### JSON OUTPUT FORMAT
Respond ONLY with valid JSON.

{
  "operations": [
    { "type": "create_card", "card": { ... } },
    { "type": "update_card", "card_id": "card_xxx", "updates": { ... } },
    { "type": "delete_card", "card_id": "card_yyy" }
  ],
  "current_phase": "question" | "facts" | "pains" | "resources" | "gaps" | "connections",
  "question_action": "keep" | "next" | "clarify",
  "next_question": "...",
  "next_hint": "..."
}

CRITICAL RULES FOR QUESTIONS:
1. When question_action="next": ALWAYS provide next_question and next_hint in the USER'S LANGUAGE.
2. When question_action="clarify": ALWAYS provide next_question and next_hint in the USER'S LANGUAGE.
3. The next_question should guide the user to the next phase (facts, pains, resources, gaps, connections).
4. If a locale is provided in the context, respond in that locale.
5. Otherwise detect the user's language from their messages and respond in the same language.
6. Keep next_question to 1 short sentence. Keep next_hint very short (2-6 words).

IMPORTANT: Start in Phase 1. Speak in the user's language. Be concise.
"""

TRANSLATE_PROMPT = """You are a localization assistant.

Translate the question and hint into the target locale.
Keep the question to 1 short sentence. Keep the hint very short (2-6 words).
Return ONLY valid JSON:
{
  "question": "...",
  "hint": "..."
}
"""


class AIService:
    """Service for AI-powered card operations."""

    def __init__(self, openrouter_client: OpenAI) -> None:
        """Initialize AI service.

        Args:
            openrouter_client: OpenRouter client instance (OpenAI-compatible API).
        """
        self.client = openrouter_client
        self.model = "google/gemini-3-flash-preview"

    async def generate_response(self, message: str, state: State) -> str:
        """Call LLM and return raw JSON string.

        Args:
            message: User's input message.
            state: Current session state.

        Returns:
            Raw JSON string from AI.
        """
        with trace(
            name="generate_response",
            inputs={
                "message": message,
                "phase": state.phase.value,
                "current_question": state.current_question,
                "session_question": state.question,
                "cards_count": len(state.cards),
            },
        ) as run:
            logger.info(f"generate_response called with: {message[:50]}...")

            context = self._build_context(message, state)

            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": context},
                    ],
                    temperature=0.7,
                    max_tokens=1000,
                    response_format={"type": "json_object"},
                )

                content = response.choices[0].message.content or "{}"

                run.end(outputs={"raw_response": content[:500]})
                return content

            except Exception as e:
                logger.error(f"Error calling AI: {e}")
                run.end(outputs={"error": str(e)})
                # Return a fallback JSON that decoder will parse
                return """{
                    "operations": [],
                    "question_action": "clarify",
                    "next_question": "Could you tell me more about that? What specifically happened?",
                    "next_hint": "Be specific."
                }"""

    def _build_context(self, message: str, state: State) -> str:
        """Build context string for AI.

        Args:
            message: User's input message.
            state: Current session state.

        Returns:
            Context string.
        """
        context = f"""User locale: {state.locale}
Current phase: {state.phase.value}
Current question: {state.current_question}
Central problem: {state.question}
"""
        if state.cards:
            context += "Existing cards (with ID and positions):\n"
            for card in state.cards:
                px = int(card.x * 1920)
                py = int(card.y * 1080)
                context += f'  - ID:{card.id} "{card.text}" ({card.type.value}) at ({px}, {py})\n'

        context += f"\nUser answers: {message}"
        return context

    async def translate_question_hint(
        self, question: str, hint: str, locale: str
    ) -> tuple[str, str] | None:
        """Translate question and hint to target locale."""
        if not question and not hint:
            return None

        content = f"Target locale: {locale}\nQuestion: {question}\nHint: {hint}\n"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": TRANSLATE_PROMPT},
                    {"role": "user", "content": content},
                ],
                temperature=0.2,
                max_tokens=200,
                response_format={"type": "json_object"},
            )
            raw = response.choices[0].message.content or "{}"
            parsed = json.loads(raw)
            next_question = str(parsed.get("question", "")).strip()
            next_hint = str(parsed.get("hint", "")).strip()
            if not next_question and not next_hint:
                return None
            return next_question, next_hint
        except Exception as exc:  # pragma: no cover - network/LLM failures
            logger.error(f"Error translating question: {exc}")
            return None
