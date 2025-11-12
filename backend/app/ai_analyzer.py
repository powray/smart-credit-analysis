"""AI Analyzer using OpenAI Chat API to generate richer explanations and risk signals."""
import os
import openai
from typing import List, Dict

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')  # change as needed

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

def _build_prompt(transactions: List[Dict], score: int, explanation: Dict) -> str:
    # Create a compact prompt with instructions
    prompt = []

    prompt.append("You are a financial analyst assistant specialized in UK personal banking.")
    prompt.append("Given parsed bank transactions and a numeric Credit Trust Score (0-100), produce:")
    prompt.append("1) A short plain-English summary (3-5 sentences) of the user's financial health.")
    prompt.append("2) Top 3 risk signals or anomalies (e.g., overdrafts, sudden income drop, frequent charges).")
    prompt.append("3) Simple, actionable recommendations to improve the score.")
    prompt.append("4) A JSON object named 'structured_insights' containing: {estimated_monthly_income, expense_ratio, risk_flags:[...]}.")
    prompt.append("Respond with two sections separated by a line with '---JSON---' where the second section is only the JSON object.")

    prompt.append("\nTransactions (most recent first):")
    # include only top 100 lines to keep prompt small
    for t in (transactions or [])[:120]:
        # safe-stringify keys
        amt = t.get('amount')
        date = t.get('date')
        raw = t.get('raw', '')
        prompt.append(f"- {date} | {amt} | {raw}")

    prompt.append(f"\nCredit Trust Score: {score}")
    prompt.append(f"\nScoring explanation: {explanation}")

    return "\n".join(prompt)

def analyze_with_ai(transactions: List[Dict], score: int, explanation: Dict, use_openai: bool = True):
    """Return a dict with 'summary' and 'structured_insights'. If OpenAI key missing, return a fallback."""
    if not use_openai or not OPENAI_API_KEY:
        return {
            "summary": "OpenAI API key not configured. Enable OPENAI_API_KEY to get natural-language analysis.",
            "structured_insights": {
                "estimated_monthly_income": None,
                "expense_ratio": None,
                "risk_flags": []
            }
        }

    prompt = _build_prompt(transactions, score, explanation)

    # Call ChatCompletion (Chat API). Uses a compact response expectation per prompt design.
    try:
        resp = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.2
        )
        text = resp.choices[0].message.content.strip()
        # Split sections by marker
        if '---JSON---' in text:
            summary, json_part = text.split('---JSON---', 1)
            structured = None
            try:
                import json as _json
                structured = _json.loads(json_part.strip())
            except Exception:
                structured = {"error": "Could not parse JSON from model."}
            return {"summary": summary.strip(), "structured_insights": structured}
        else:
            return {"summary": text, "structured_insights": {}}
    except Exception as e:
        return {"summary": f"OpenAI request failed: {e}", "structured_insights": {}}
