# Python for finance (Universidad Pontificia Comillas, Madrid)

Five practice sessions from Foundations of Finance and Engineering Economy during my exchange semester. The sessions are guided notebooks: the course provides the structure and plotting, and the exercises are the functions and calculations I wrote. Outputs are cleared.

| Session | What I built | Tools |
|---|---|---|
| `p01-npv-and-irr` | Payback, NPV and IRR as functions; the crossover rate of two projects; payoff profile plot | numpy, numpy-financial, plotly |
| `p02-bond-basics` | A table of bond cash flows, bond pricing as the present value of cash flows, yield to maturity found numerically | pandas, scipy.optimize |
| `p03-yield-curve-calibration` | Downloading US Treasury yield curve data and fitting a Nelson-Siegel-Svensson curve | nelson-siegel-svensson, pandas |
| `p04-bonds` | Bond duration and convexity functions and a plot of both | numpy, matplotlib, plotly |
| `p05-portfolios` | Stock and gold price history joined into one dataset, returns, annual expected return, volatility and covariance, portfolio return and Sharpe ratio, random portfolios, and the maximum-Sharpe portfolio via constrained optimisation (group work) | pandas, scipy.optimize, statsmodels, plotly |

## What I learned

- **Time value of money in code.** Writing NPV and IRR myself showed why the two can rank projects differently, which is what the crossover rate captures.
- **Prices and yields are the same thing seen from two sides.** A bond price is a sum of discounted cash flows, and the yield to maturity is the discount rate that makes that sum equal the market price, which needs a numerical solver.
- **Risk measures for bonds.** Duration and convexity describe how a bond price reacts to a change in the interest rate, first-order and second-order.
- **Yield curves are fitted, not observed.** Only a few maturities are quoted, so a parametric model (level, slope and curvature factors) fills in the rest.
- **Portfolio theory with real data.** Annualising with 252 trading days, using the covariance matrix for portfolio risk, comparing portfolios by Sharpe ratio, and then letting an optimiser search for the best weights under the constraint that they add up to one.
- **Practical data work.** Joining price tables from different sources, checking for missing values and choosing a time window.

## Notes

`p05` reads Excel price files (IBEX 35 constituents and prices, gold) that belong to the course and are not included, so that notebook will not run without them. `p03` downloads its data from the internet when run. `p05` is group work; the notebook has been cleaned of names and ids.
