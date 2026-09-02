import math
from stock_universe import STOCK_UNIVERSE, RISK_FREE_RATE, MARKET_RETURN
from investor_profiles import INVESTOR_PROFILES

CORRELATION = 0.3

ALLOCATION_TABLE = {
    "Conservative": ["PAYBOND", "PAYGOLD", "PAYRETAIL"],
    "Moderate": ["PAYRETAIL", "PAYINFRA", "PAYGOLD"],
    "Aggressive": ["PAYTECH", "PAYFIN", "PAYINFRA"],
}

def get_stock_data(ticker):
    """Simulated tool call - looks up stock data from STOCK_UNIVERSE."""
    return STOCK_UNIVERSE[ticker]

def think(investor_profile):
    """THINK stage: determine allocation from risk_tolerance using the prescribed table."""
    tickers = ALLOCATION_TABLE[investor_profile["risk_tolerance"]]
    weights = {t: 1/3 for t in tickers}
    return tickers, weights

def act(tickers):
    """ACT stage: call the get_stock_data tool for each ticker."""
    return {t: get_stock_data(t) for t in tickers}

def observe_decide(tickers, weights, stock_data):
    """OBSERVE -> DECIDE: CAPM expected return (beta only) + portfolio variance/std."""
    expected_returns = {}
    for t in tickers:
        beta = stock_data[t]["beta"]
        expected_returns[t] = RISK_FREE_RATE + beta * (MARKET_RETURN - RISK_FREE_RATE)

    portfolio_return = sum(weights[t] * expected_returns[t] for t in tickers)

    variance = sum((weights[t] ** 2) * (stock_data[t]["std_dev"] ** 2) for t in tickers)
    for i in range(len(tickers)):
        for j in range(i + 1, len(tickers)):
            ti, tj = tickers[i], tickers[j]
            cov_ij = CORRELATION * stock_data[ti]["std_dev"] * stock_data[tj]["std_dev"]
            variance += 2 * weights[ti] * weights[tj] * cov_ij

    return portfolio_return, math.sqrt(variance)

def human_in_loop_check(portfolio_std):
    return portfolio_std > 0.20

def build_narrative(investor_profile, tickers, portfolio_return, portfolio_std):
    """MOCK_LLM path: deterministic f-string template, no LLM call."""
    return (f"For {investor_profile['risk_tolerance']} investor {investor_profile['investor_id']}, "
            f"we recommend an allocation across {tickers} with an expected portfolio return "
            f"of {portfolio_return:.1%} and volatility of {portfolio_std:.1%}.")

def run_agent(investor_profile):
    tickers, weights = think(investor_profile)
    stock_data = act(tickers)
    portfolio_return, portfolio_std = observe_decide(tickers, weights, stock_data)
    escalate = human_in_loop_check(portfolio_std)

    result = {
        "investor_id": investor_profile["investor_id"],
        "risk_tolerance": investor_profile["risk_tolerance"],
        "tickers": tickers,
        "portfolio_return": portfolio_return,
        "portfolio_std": portfolio_std,
    }
    if escalate:
        result["status"] = "ESCALATED_TO_HUMAN_ADVISOR"
    else:
        result["status"] = "FINALIZED"
        result["narrative"] = build_narrative(investor_profile, tickers, portfolio_return, portfolio_std)
    return result

if __name__ == "__main__":
    for profile in INVESTOR_PROFILES:
        r = run_agent(profile)
        print(f"\n--- {r['investor_id']} ({r['risk_tolerance']}) ---")
        print(f"Allocation: {r['tickers']}")
        print(f"Expected return: {r['portfolio_return']*100:.2f}%")
        print(f"Std dev: {r['portfolio_std']*100:.2f}%")
        print(f"Status: {r['status']}")
        if r['status'] == "FINALIZED":
            print(f"Narrative: {r['narrative']}")