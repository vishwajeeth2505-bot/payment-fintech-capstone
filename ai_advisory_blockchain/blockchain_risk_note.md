# Blockchain & Crypto Risk Note

## 1. Stablecoin Type and DeFi/DAO Governance Risk

Before Paytm could responsibly surface a "Paytm Crypto Insights" watchlist feature to
retail users, it would need to clearly distinguish between fiat-collateralized and
algorithmic stablecoins, because the two carry very different levels of real backing
and risk. A fiat-collateralized stablecoin is backed roughly 1:1 by real currency held
in reserve, making it relatively straightforward to verify and less prone to sudden
collapse. An algorithmic stablecoin, by contrast, tries to hold its peg through code
and market incentives rather than real assets — and history has shown this can fail
catastrophically and quickly, wiping out holders with little warning. A watchlist that
lumps both types together under a single "stablecoin" label would mislead retail users
into assuming a uniform level of safety that does not exist.

On the DeFi/DAO side, many crypto protocols are governed by token-holder voting rather
than a traditional company structure. The key risk retail users need to understand is
that voting power in these DAOs can become concentrated among a small number of large
holders, so governance decisions may not reflect the interests of ordinary retail
participants at all. A protocol can be marketed as "community-governed," while in
practice a handful of large wallets control most outcomes. Any Paytm feature that shows
a "governance risk" score needs to make this concentration risk explicit rather than
implying that decentralized governance automatically means fair or safe governance.

## 2. Crypto-as-an-Asset-Class Recommendation

Applying standard CAPM-style portfolio theory, cryptocurrency is a poor fit for an
optimal portfolio: it has no intrinsic value or dividend stream, its correlation with
traditional assets tends to break down and turn positive precisely during market stress
(when diversification benefits matter most), historical return data suffers from
survivorship bias since failed tokens disappear from the record, its return
distribution is heavy-tailed and unpredictable, and transaction costs for retail
investors are high. None of these properties reward automatic inclusion in a portfolio
the way a standard equity or bond would.

Given this, I would recommend a maximum allocation of up to 2% of a retail portfolio
for Paytm Money's advisory product. This gives investors a limited opportunity to
participate in crypto's potential upside without exposing a meaningful share of their
savings to its high volatility, weak diversification benefit during downturns, and
elevated transaction costs. A hard 2% ceiling also keeps any single bad outcome — even
a total loss of the crypto allocation — from doing serious damage to an investor's
overall financial plan, which is the standard a responsible retail advisory product
should be held to.

## 3. T.A.N.G. Fraud Framework

For a combined UPI/wallet + lending + wealth platform like Paytm, the two most relevant
social-engineering vectors are Authority and Greed.
*Authority*: Because Paytm spans payments, lending, and investing in one account,
a scammer impersonating "Paytm support" can exploit that breadth — claiming an issue
across the user's linked services to pressure them into sharing an OTP or UPI PIN
"to verify their account." A bank-side real-time defense against this is a device and
login anomaly check: flagging logins from unusual devices, unfamiliar locations, or
sudden unexplained account activity, and automatically triggering additional
step-up verification before any sensitive action (like an OTP-linked transfer) is
allowed to proceed.

*Greed*: Because Paytm Money users already have money actively invested through the
platform, they are a natural target for fake high-return investment schemes promising
unrealistic gains. A bank-side real-time defense here is a transaction and beneficiary
risk check: automatically flagging unusual transfers to new, unfamiliar, or high-risk
beneficiary accounts, and temporarily holding those transfers for review before funds
move, rather than relying solely on the user to recognize the scam in the moment.

Both defenses share a common principle: they operate on the bank's side of the
transaction, independent of whether the user has been fooled, which is what makes them
meaningfully protective rather than just advisory.