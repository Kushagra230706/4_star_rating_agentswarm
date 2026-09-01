import os
import json
import time
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


class LLMRouter:
    """
    Multi-provider resilient LLM router.
    Primary: Groq (tries a list of current models)
    Fallback: Gemini (tries a list of supported models)
    Safety Net: Deterministic Heuristic Fallback
    """
    def __init__(self):
        self.groq_client = None
        self.gemini_client = None
        self.groq_model_candidates = [
            "groq/compound",
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "llama-3.1-70b-versatile",
        ]
        self.gemini_model_candidates = [
            "gemini-3.6-flash",
            "gemini-3.5-flash",
            "gemini-2.5-flash",
            "gemini-2.0-flash",
        ]
        self.groq_model = self.groq_model_candidates[0]
        self.gemini_model = self.gemini_model_candidates[0]

        if GROQ_API_KEY and GROQ_API_KEY != "your_groq_api_key_here":
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=GROQ_API_KEY)
            except Exception as e:
                print(f"[CONFIG WARNING] Failed to initialize Groq client: {e}")

        if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
            try:
                import google.generativeai as genai
                genai.configure(api_key=GEMINI_API_KEY)
                self.gemini_client = genai.GenerativeModel(self.gemini_model)
            except Exception as e:
                print(f"[CONFIG WARNING] Failed to initialize Gemini client: {e}")

    def _try_groq(self, role: str, system_prompt: str, user_prompt: str):
        if not self.groq_client:
            return None

        last_error = None
        for model_name in self.groq_model_candidates:
            try:
                response = self.groq_client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.2,
                    max_tokens=2000
                )
                res_text = response.choices[0].message.content
                if res_text and len(res_text.strip()) > 0:
                    self.groq_model = model_name
                    return res_text
            except Exception as e:
                last_error = e
                print(f"[FALLBACK TRIGGERED] Agent '{role}' failed on Groq model '{model_name}': {e}")

        if last_error:
            print(f"[FALLBACK TRIGGERED] Agent '{role}' exhausted Groq models. Final error: {last_error}")
        return None

    def _try_gemini(self, role: str, system_prompt: str, user_prompt: str):
        if not self.gemini_client:
            return None

        import google.generativeai as genai
        full_prompt = f"{system_prompt}\n\nUSER INPUT:\n{user_prompt}"
        last_error = None

        for model_name in self.gemini_model_candidates:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(full_prompt)
                if response and getattr(response, 'text', None):
                    self.gemini_model = model_name
                    return response.text
            except Exception as e:
                last_error = e
                print(f"[CRITICAL FALLBACK] Agent '{role}' failed on Gemini model '{model_name}': {e}")

        if last_error:
            print(f"[CRITICAL FALLBACK] Agent '{role}' exhausted Gemini models. Final error: {last_error}")
        return None

    def call_agent_llm(self, role: str, system_prompt: str, user_prompt: str) -> str:
        """
        Attempts Groq primary -> Gemini fallback -> Safety Net fallback.
        Guarantees non-empty text response.
        """
        groq_response = self._try_groq(role, system_prompt, user_prompt)
        if groq_response:
            return groq_response

        gemini_response = self._try_gemini(role, system_prompt, user_prompt)
        if gemini_response:
            return gemini_response

        print(f"[SAFETY NET ACTIVATED] Generating heuristic fallback for agent '{role}'")
        return self._generate_heuristic_response(role, user_prompt)

    def _generate_heuristic_response(self, role: str, prompt: str) -> str:
        """Returns safe structured fallback text if all external APIs are unreachable."""
        return json.dumps({
            "status": "HEURISTIC_FALLBACK",
            "agent_name": role,
            "summary": f"Standard risk-weighted fallback evaluation generated for {role}.",
            "key_findings": [
                "API connectivity issue detected; applying standard business domain heuristic.",
                "[ASSUMPTION: Default industry benchmark metrics applied for operational continuity]"
            ],
            "recommendations": [
                f"Proceed with conservative baseline strategy for {role} pending API restoration."
            ],
            "financial_or_operational_impact": "Conservative estimate: ±15% variance from budget target.",
            "explicit_assumptions": [
                "[ASSUMPTION: Baseline market growth rate of 5% per annum]"
            ],
            "metrics": {"confidence_score": 0.75, "mode": "Heuristic Safety Net"}
        })


# Global singleton router
router = LLMRouter()
