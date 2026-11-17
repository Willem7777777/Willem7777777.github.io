# Data science (TU Delft BSc, TB142Ic / TB242IA)

Python notebooks from two Data Science courses in my bachelor Technology, Policy and Management. Some notebooks are adapted from the course teams' material (credited inside the notebook); the practicum assignments and the obesity analysis are the ones where I did the analysis myself. Outputs are cleared.

## What is in here

| Notebook | What it does | Main tools |
|---|---|---|
| `practicum1-pandas-and-exploratory-analysis` | Load a dataset, handle missing values, explore it with summary statistics, boxplots, histograms and a correlation heatmap (Dutch) | pandas, seaborn |
| `practicum2-statistical-tests-and-bootstrapping` | Model selection, a full regression analysis and statistical tests, with bootstrapping (Dutch) | scipy.stats, scikit-learn |
| `lecture2-grouping-aggregating-joining` | Aggregates per group, quantiles, finding the largest values, joining tables | pandas |
| `lecture2-mean-std-median-quartiles` | Summary statistics and how to plot them | numpy, seaborn |
| `week3-sampling-and-visualizing-distributions` | Sampling distributions and confidence intervals | scipy.stats |
| `week3-penguin-sampling-and-testing` | Parametric confidence intervals and a t-test on penguin measurements | scipy.stats (`ttest_ind`) |
| `week3-linear-regression-and-bootstrapping` | Least squares solved analytically, train/test split, bootstrapping to show how much a model varies, feature engineering | numpy, matplotlib |
| `week4-multiple-linear-regression` | Regression with formulas: dummy variables, standardised predictors, per-group slopes and intercepts (interaction terms), residual checks | statsmodels |
| `lecture5-text-data` | Turning text into TF-IDF vectors and clustering documents with k-means | scikit-learn |
| `lecture5-graphs-and-networks` | A first look at graphs and shortest paths | networkx |
| `obesity-data-analysis` | My own analysis of an obesity dataset: averages, correlation matrix, dummy variables and a logistic regression (Dutch comments) | pandas, scikit-learn |

## What I learned

- **Look at the data before modelling.** Check missing values, distributions and outliers first (describe, boxplots, histograms, correlation heatmap), because every later step depends on them.
- **Statistics by simulation.** A confidence interval or a test result is easier to trust once you have seen it come out of repeated sampling and bootstrapping, and compared the parametric estimate with the bootstrapped one.
- **Regression from the inside.** I solved least squares by hand before using a library, then used `statsmodels` formulas for multiple regression, which made it clear what dummy coding, standardising and an interaction term actually change in the coefficients.
- **Check assumptions, not just the fit.** I plotted residuals against fitted values and made Q-Q plots, and noted heteroskedasticity in one model instead of only reading the R-squared.
- **Text and groups as data.** Documents can be turned into numbers (TF-IDF) and clustered, and grouped aggregates and joins answer many questions without a model at all.
- **Asking a question first.** In the obesity analysis the useful step was choosing which variables could answer which question (for example, which factors relate to obesity type) before picking a method.

The two small datasets used here (penguins and obesity) are in `data/`. Other course datasets are not included.
