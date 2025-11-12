import numpy as np

def compute_credit_trust_score(transactions):
    if not transactions:
        return 20, {"reason": "No transactions found"}
    amounts = np.array([t['amount'] for t in transactions])
    avg_monthly = float(np.mean(np.abs(amounts)))
    volatility = float(np.std(amounts))
    deposit_share = float(np.sum(amounts[amounts>0]) / (np.sum(np.abs(amounts)) + 1e-9))
    s_income = min(40, (avg_monthly / 2000) * 40)
    s_stability = max(0, 30 - (volatility / (avg_monthly + 1e-9)) * 30)
    s_deposit = min(30, deposit_share * 30)
    score = int(max(0, min(100, s_income + s_stability + s_deposit)))
    explanation = {"avg_monthly": avg_monthly, "volatility": volatility, "deposit_share": deposit_share, "components": {"income": s_income, "stability": s_stability, "deposit": s_deposit}}
    return score, explanation
