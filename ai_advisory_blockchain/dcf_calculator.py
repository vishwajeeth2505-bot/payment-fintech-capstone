from stock_universe import RISK_FREE_RATE, MARKET_RETURN, STOCK_UNIVERSE

# --- Stated inputs for a hypothetical Paytm business line (in INR) ---
EBIT = 100_000_000        # illustrative EBIT, base year
TAX_RATE = 0.25
DA = 8_000_000            # depreciation & amortization
CAPEX = 12_000_000
DELTA_NWC = 3_000_000     # change in net working capital

# Unlevered FCFF = EBIT * (1 - tax) + D&A - CapEx - dNWC
FCFF_BASE = EBIT * (1 - TAX_RATE) + DA - CAPEX - DELTA_NWC

# 5-year fading growth rate (starts high, fades toward terminal growth)
GROWTH_RATES = [0.12, 0.105, 0.09, 0.075, 0.06]

# --- WACC inputs ---
BETA = STOCK_UNIVERSE["PAYINFRA"]["beta"]   # 1.10, used for cost of equity
COST_OF_EQUITY = RISK_FREE_RATE + BETA * (MARKET_RETURN - RISK_FREE_RATE)
AFTER_TAX_COST_OF_DEBT = 0.06                # illustrative
EQUITY_WEIGHT = 0.70
DEBT_WEIGHT = 0.30
BASE_WACC = EQUITY_WEIGHT * COST_OF_EQUITY + DEBT_WEIGHT * AFTER_TAX_COST_OF_DEBT

# Terminal growth: chosen >= 3pp below base WACC (spec constraint)
TERMINAL_GROWTH = BASE_WACC - 0.06   # comfortably more than 3pp below


def project_fcff(fcff_base, growth_rates):
    projections = []
    fcff = fcff_base
    for g in growth_rates:
        fcff = fcff * (1 + g)
        projections.append(fcff)
    return projections


def dcf_value(fcff_base, growth_rates, wacc, terminal_growth):
    projections = project_fcff(fcff_base, growth_rates)
    pv_fcff = sum(cf / (1 + wacc) ** (i + 1) for i, cf in enumerate(projections))

    terminal_value = projections[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal = terminal_value / (1 + wacc) ** len(projections)

    return pv_fcff + pv_terminal, projections, terminal_value


def sensitivity_table(fcff_base, growth_rates, base_wacc, base_growth):
    wacc_range = [base_wacc - 0.01, base_wacc, base_wacc + 0.01]
    growth_range = [base_growth - 0.01, base_growth, base_growth + 0.01]
    table = {}
    min_gap = 999
    for w in wacc_range:
        for g in growth_range:
            ev, _, _ = dcf_value(fcff_base, growth_rates, w, g)
            table[(round(w, 4), round(g, 4))] = ev
            gap = w - g
            min_gap = min(min_gap, gap)
    return table, min_gap


if __name__ == "__main__":
    print(f"Base FCFF (year 0): INR {FCFF_BASE:,.0f}")
    print(f"Cost of equity (CAPM, beta={BETA}): {COST_OF_EQUITY:.2%}")
    print(f"Base WACC: {BASE_WACC:.2%}")
    print(f"Terminal growth rate: {TERMINAL_GROWTH:.2%}")
    print(f"Gap (WACC - terminal growth): {(BASE_WACC - TERMINAL_GROWTH):.2%}")

    ev, projections, tv = dcf_value(FCFF_BASE, GROWTH_RATES, BASE_WACC, TERMINAL_GROWTH)
    print("\n5-year FCFF projections:")
    for i, cf in enumerate(projections, 1):
        print(f"  Year {i}: INR {cf:,.0f}")
    print(f"Terminal value: INR {tv:,.0f}")
    print(f"Enterprise value (base case DCF): INR {ev:,.0f}")

    table, min_gap = sensitivity_table(FCFF_BASE, GROWTH_RATES, BASE_WACC, TERMINAL_GROWTH)
    print(f"\nSensitivity table (WACC x terminal growth), worst-case gap: {min_gap:.2%}")
    for (w, g), val in table.items():
        print(f"  WACC={w:.2%}, growth={g:.2%} -> EV=INR {val:,.0f}")

    # EV/EBITDA cross-check
    EBITDA = EBIT + DA
    ILLUSTRATIVE_MULTIPLE = 8.0
    ev_multiple = EBITDA * ILLUSTRATIVE_MULTIPLE
    print(f"\nEV/EBITDA cross-check: EBITDA=INR {EBITDA:,.0f}, multiple={ILLUSTRATIVE_MULTIPLE}x")
    print(f"EV via multiple: INR {ev_multiple:,.0f}")
    print(f"EV via DCF:      INR {ev:,.0f}")
    diff_pct = (ev - ev_multiple) / ev_multiple
    print(f"DCF is {diff_pct:+.1%} vs the multiple-based estimate.")