# Group project: factors behind obesity types

Group report for TB242IA Intelligent Data Analysis (TU Delft BSc TPM, 2023), written in Dutch. It asks which lifestyle and external factors have the most influence on obesity and on the type of obesity.

## How the report is built

- Literature study, a description of the problem domain, stakeholders, the problem space and the solution space.
- Operationalisation: the main question is split into sub-questions, and the variables of the UCI "Estimation of obesity levels" dataset (age, height, weight, eating and activity habits) are linked to them.
- Experimental set-up and results with regression analysis and one-sample t-tests in Python, followed by conclusions and recommendations.

An individual analysis notebook on the same dataset is in [`../data-science-tb/obesity-data-analysis.ipynb`](../data-science-tb/obesity-data-analysis.ipynb).

## What I learned

- **Turning a broad problem into testable questions.** Splitting "what influences obesity" into sub-questions with a variable and a method each is what made the analysis possible.
- **Choosing a method that fits the question.** Regression for the strength of relationships, t-tests for whether an average differs from a reference value.
- **Being careful with conclusions.** A dataset of survey answers shows association, not cause, and the report states those limits.
- **Writing for stakeholders.** The report starts from who is affected by the problem before it gets to the data.
