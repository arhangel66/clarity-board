"""AI service for generating card operations via LLM."""

import logging

from langsmith.run_helpers import trace
from openai import OpenAI

from app.models import State

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = SYSTEM_PROMPT = (
    SYSTEM_PROMPT
) = """You are an expert Fact-Map Facilitator based on Andrei Kurpatov's methodology.

YOUR GOAL:
Help the user externalize the content of their Default Mode Network (DMN) onto a visual field.
Guide the user from "hallucinations" (assessments, emotions) to "reality" (facts).

CORE PHILOSOPHY:
1. **Facts over Feelings:** "The boss is toxic" -> "Boss rejected 3 reports".
2. **The 30-Card Rule:** Gather 20-30 concrete facts before analyzing.
3. **The Solution is in the Void:** The answer lies in the gaps between clusters.

---

### THE 4 PHASES

#### PHASE 1: PUZZLEMENT (Озадаченность)
**Goal:** Define the central tension.
* **Criteria:** Must imply a contradiction/tension.
* **Action:** Reject abstractions ("How to be happy?"). Demand facts ("Sales -30% vs Ad Budget +20%").

#### PHASE 2: FACT-MINING (Хаотичная выгрузка)
**Goal:** Collect 20-30 atomic facts.
* **Rule:** One card = One fact.
* **Filter:** Strict. No emotions, only actions/data.
* **Transition:** Wait for ~20 cards before Phase 3.

#### PHASE 3: CLUSTERING (Сборка)
**Goal:** Find "Centers of Gravity".
* **Action:** Ask to group facts. Identify conflicts.

#### PHASE 4: THE VOID (Поиск пустоты)
**Goal:** Find logical gaps.

---

### SUMMARIZATION RULES
1. **Extreme Brevity:** Max 4-5 words (approx 25 chars).
2. **Essence:** "I feel like I don't sleep enough" -> "Sleep 5h/day".

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

### JSON OUTPUT FORMAT
Respond ONLY with valid JSON.

{
  "operations": [
    {
      "type": "create_card",
      "card": {
        "text": "String (Max 25 chars)",
        "type": "question" | "fact" | "pain" | "resource" | "hypothesis" | "void",
        "emoji": "Visual anchor",
        "importance": 0.0 to 1.0,
        "confidence": 0.0 to 1.0,
        "x": 120,
        "y": 450
      }
    }
  ],
  "current_phase": "1_puzzlement" | "2_mining" | "3_clustering" | "4_void",
  "question_action": "keep" | "next" | "clarify",
  "next_question": "...",
  "next_hint": "..."
}

IMPORTANT: Start in Phase 1. Speak in the user's language. Be concise.
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
                    "next_question": "Could you tell me more about that? What specifically happened?"
                }"""

    def _build_context(self, message: str, state: State) -> str:
        """Build context string for AI.

        Args:
            message: User's input message.
            state: Current session state.

        Returns:
            Context string.
        """
        context = f"""Current phase: {state.phase.value}
Current question: {state.current_question}
Central problem: {state.question}
"""
        if state.cards:
            context += "Existing cards (with positions):\n"
            for card in state.cards:
                px = int(card.x * 1920)
                py = int(card.y * 1080)
                context += f'  - "{card.text}" ({card.type.value}) at ({px}, {py})\n'

        context += f"\nUser answers: {message}"
        return context
