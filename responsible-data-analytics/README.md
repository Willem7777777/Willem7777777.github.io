# Responsible Data Analytics (TU Delft MSc CoSEM)

Two notebooks from the course SEN163 (A and B). The datasets belong to the course and are not included, so the notebooks will not run without them. Outputs are cleared.

## Lab 3: preprocessing and correlation analysis (`lab3-preprocessing-regression-correlation.ipynb`)

Health and sleep datasets (pandas, seaborn, scipy).

- Quality checks: missing values, binning age into 10-year groups, impossible values such as children who smoke.
- Outlier handling with a function that finds outliers per variable (boxplots and an interquartile-range rule) and removes the rows.
- Correlation analysis: a Spearman correlation heatmap, and Pearson, Spearman and Kendall coefficients with p-values for variable pairs such as height and weight.

## Group project: predicting travel mode (`group-project-predictive-modelling.ipynb`)

A five-person project for SEN163B on the Mobility Panel Netherlands (MPN), predicting which mode of transport people use. I was one of the authors; teammates' names have been removed.

- **Data preparation.** Merging several SPSS files at person and household level, turning special codes such as 99 into missing values, dropping incomplete rows, and recategorising variables to keep the model small and easier to interpret.
- **Exploration.** Distribution of transport modes, mode choice by age and by income, and a Cramer's V matrix for associations between categorical variables.
- **Modelling.** One-hot encoding and standardising, a stratified train/validation/test split, and then multinomial logistic regression, a random forest with balanced class weights, XGBoost and a soft-voting ensemble, compared with k-fold cross-validation, classification reports and confusion matrices.
- **Explaining the model.** SHAP values on the random forest to see which variables drive the predictions.

## What I learned

- **Most of the work is data preparation.** Getting several survey files into one clean table took more thought than fitting the models.
- **Accuracy alone is misleading with unbalanced classes.** Class weights, stratified splits and per-class precision and recall change what "good" means.
- **Compare models on the same split.** A simple baseline (logistic regression) against tree-based models and an ensemble shows whether extra complexity pays off.
- **A prediction needs an explanation.** SHAP made it possible to check whether the model relied on sensible variables, which is the "responsible" part of the course.
- **Comparable results need a shared set-up.** The same cleaned data, random seed and train/validation/test split for every model, so the differences come from the models and not from the data.
