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
    Primary: Groq (Llama-3.3-70b-versatile)
    Fallback: Gemini 2.0 Flash
    Safety Net: Deterministic Heuristic Fallback
    """
    def __init__(self):
        self.groq_client = None
        self.gemini_client = None
        
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
                self.gemini_client = genai.GenerativeModel('gemini-3.6-flash')
            except Exception as e:
                print(f"[CONFIG WARNING] Failed to initialize Gemini client: {e}")

    def call_agent_llm(self, role: str, system_prompt: str, user_prompt: str) -> str:
        """
        Attempts Groq primary -> Gemini fallback -> Safety Net fallback.
        Guarantees non-empty text response.
        """
        # Try Primary: Groq API
        if self.groq_client:
            models_to_try = ["groq/compound", "qwen/qwen3.8-27b", "openai/gpt-oss-120b", "llama-3.3-70b-versatile"]
            for model_id in models_to_try:
                try:
                    response = self.groq_client.chat.completions.create(
                        model=model_id,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        temperature=0.2,
                        max_tokens=2000
                    )
                    res_text = response.choices[0].message.content
                    if res_text and len(res_text.strip()) > 0:
                        return res_text
                except Exception:
                    continue
            print(f"[FALLBACK TRIGGERED] Agent '{role}' failed on all Groq models. Switching to Gemini...")

        # Try Secondary Fallback: Gemini 2.0 Flash
        if self.gemini_client:
            try:
                full_prompt = f"{system_prompt}\n\nUSER INPUT:\n{user_prompt}"
                response = self.gemini_client.generate_content(full_prompt)
                if response and response.text:
                    return response.text
            except Exception as e:
                print(f"[CRITICAL FALLBACK] Agent '{role}' failed on Gemini API: {e}. Switching to Safety Net...")

        # Final Safety Net: Deterministic Domain Heuristic (Ensures swarm never crashes)
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
