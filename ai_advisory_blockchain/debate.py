from stock_universe import STOCK_UNIVERSE

TICKER = "PAYTECH"  # chosen ticker for this debate demo


def bull_agent(ticker, data):
    return (f"Bull: With an expected return of {data['analyst_expected_return']:.1%} "
            f"against a beta of {data['beta']:.2f}, this offers attractive risk-adjusted upside.")


def bear_agent(ticker, data):
    return (f"Bear: A standard deviation of {data['std_dev']:.1%} signals significant "
            f"volatility risk that could erode returns during a downturn.")


def synthesizer_agent(ticker, bull_arg, bear_arg, data):
    return (f"Synthesizer: {ticker} offers a return/beta profile of "
            f"{data['analyst_expected_return']:.1%}/{data['beta']:.2f}, but its "
            f"{data['std_dev']:.1%} volatility means it suits only investors with "
            f"higher risk tolerance and a longer time horizon.")


def run_debate(ticker):
    data = STOCK_UNIVERSE[ticker]
    bull = bull_agent(ticker, data)
    bear = bear_agent(ticker, data)
    synthesis = synthesizer_agent(ticker, bull, bear, data)
    return bull, bear, synthesis


if __name__ == "__main__":
    bull, bear, synthesis = run_debate(TICKER)
    print(f"--- Debate on {TICKER} ---")
    print(bull)
    print(bear)
    print(synthesis)