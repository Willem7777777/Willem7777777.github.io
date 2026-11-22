# Coursework portfolio

Python and Java projects, and reports from my studies at TU Delft (BSc Technology, Policy and Management; MSc Complex Systems Engineering and Management) and an exchange at Universidad Pontificia Comillas. Experience, research, the full list of courses and links to my theses are on the [portfolio page](https://willem7777777.github.io/).

Every folder has its own README with what I built and what I learned. The portfolio page has the same split in two tabs: **Reports** and **Code**.

## Courses by category

All courses from my TU Delft BSc and MSc, grouped by category. Where a course produced code or a report that is in this repository, it is linked; the other courses had no code or report that I have published here.

### Data & Analytics

| Course | In this repository |
|---|---|
| Responsible Data Analytics | [`responsible-data-analytics/`](responsible-data-analytics/) |
| Statistical Analysis of Choice Behaviour | – |
| Data Science in Technische Bestuurskunde | [`data-science-tb/`](data-science-tb/), [`data-science-group-project-obesity/`](data-science-group-project-obesity/), [`reports-papers/`](reports-papers/) (toeslagenaffaire essay) |
| Multivariate Data Analysis | – |
| Statistics and Data Analysis | – |
| Research and Data Analysis | – |

### Cybersecurity & Privacy

| Course | In this repository |
|---|---|
| Cybersecurity: Actors, Incentives, Interventions | – |
| Cyber Crime Science | [`reports-papers/`](reports-papers/) (group presentation) |
| User-Centred Security | [`reports-papers/`](reports-papers/) (MFA fatigue and Zero Trust paper) |

### Systems & Architecture

| Course | In this repository |
|---|---|
| I and C Architecture Design | – |
| I and C Service Design | [`reports-papers/`](reports-papers/) (smart-home service design reflection) |
| ICT System Engineering and Rapid Prototyping | – |
| Interconnected Engineering Systems | – |
| Introduction to Design in Complex Systems | – |
| Design in Networked Systems | [`network-science-lectures/`](network-science-lectures/), [`network-accessibility-helsinki/`](network-accessibility-helsinki/) |
| Digital Platform Design | [`digital-platform-design/`](digital-platform-design/) |
| Complex Systems Engineering | – |
| Design Project | – |
| Computer and Information Systems | – |
| Introduction to Programming with Python | – |

### Mathematics & Modelling

| Course | In this repository |
|---|---|
| Differential Equations and Linear Algebra | – |
| Multivariable Analysis and Linear Algebra | – |
| Systems Modelling 1: Modelling Principles | – |
| Systems Modelling 2 | – |
| System Modelling 3: Simulation Methods | – |
| System Modelling 4: Project Simulation Methods | – |

### Management & Organisation

| Course | In this repository |
|---|---|
| Managing Multi-actor Decision-making | [`reports-papers/`](reports-papers/) (Chat Control paper) |
| Organisation and Management | – |
| Analysis of Multi-Actor Systems | – |
| CoSEM Research Challenges | [`reports-papers/`](reports-papers/) (Digital Product Passport literature review) |
| Problem Analysis | – |

### Economics & Finance

| Course | In this repository |
|---|---|
| Micro and Market Economy | – |
| Economy of Infrastructures | – |
| Operational Research | – |
| Foundations of Finance | – |
| Engineering Economy | – |
| Economics Analysis for Business Decisions | – |
| Management Accounting | – |

### Governance, Law & Policy

| Course | In this repository |
|---|---|
| Governance Specialisatie (I and C) | – |
| Governance van sociotechnische systemen | – |
| I&C in a socio-technical context | – |
| Institutional Economics for Designing in Socio-technical Systems | – |
| Government and Law 1 | – |
| Governance and Law 2 | – |
| Law and Institutions | – |
| Ethics and Safety | – |

### Research & Thesis

| Course | In this repository |
|---|---|
| Master Thesis Research Design | [`reports-papers/`](reports-papers/) (hybrid cloud sovereignty proposal, thesis defence slides) |
| Bachelor Final Project | [`bachelor-thesis-digid-eidas/`](bachelor-thesis-digid-eidas/) |
| Internship TPM | – |
| Sustainable Development | – |

**Also in this repository, from outside the course list above:** [`finance-python-comillas/`](finance-python-comillas/) (Python for finance, exchange at Universidad Pontificia Comillas), [`graph-theory-besliskunde/`](graph-theory-besliskunde/) (BSc Besliskunde), the WGS governance essay in [`reports-papers/`](reports-papers/) (TB321 Governance) and [`java/`](java/) (first-year Java course).

## Reports

| Folder | Content |
|---|---|
| `bachelor-thesis-digid-eidas/` | Bachelor thesis on aligning DigiD with eIDAS and the EU Data Act |
| `reports-papers/` | Papers and reflections: Digital Product Passport architecture, MFA fatigue in Zero Trust, Chat Control, a hybrid cloud sovereignty proposal, a smart-home platform reflection, and two Dutch essays on the toeslagenaffaire and the WGS |
| `digital-platform-design/` | Reports: BattCycle battery-sharing platform design and a comparison of European data spaces |
| `data-science-group-project-obesity/` | Group report on factors behind obesity types (Dutch) |

## Code: recent (APIs and payments, Mollie test mode)

| Folder | Content |
|---|---|
| `mollie-api-postman/` | Postman collection with automated tests for the Mollie Payments API (test mode): payments, mandates, subscriptions, webhooks, idempotency |
| `mollie-webhook-receiver/` | Python (Flask) service that receives Mollie webhooks in test mode: fetches the payment, ignores duplicates, logs status changes, with tests |
| `mollie-yoga-studio-poc/` | Proof of concept for a fictional yoga studio: one-off payment, first payment and mandate, monthly subscription from the webhook, with tests |

## Code: older coursework (TU Delft and Comillas)

| Folder | Content |
|---|---|
| `data-science-tb/` | Data science with pandas, seaborn, statsmodels and scikit-learn: exploratory analysis, sampling, hypothesis testing, regression, bootstrapping, text clustering, and an obesity data analysis |
| `finance-python-comillas/` | Python for finance: NPV and IRR, bond pricing and duration, yield curve calibration, portfolio optimisation |
| `network-accessibility-helsinki/` | Network analysis of accessibility in Helsinki districts with networkx and geopandas |
| `network-science-lectures/` | Graph representations, random and scale-free networks with networkx |
| `responsible-data-analytics/` | Data preprocessing and correlation analysis, and a group project predicting travel mode with scikit-learn, XGBoost and SHAP |
| `graph-theory-besliskunde/` | Graph algorithms for decision problems: matching, shortest routes, Euler circuits (Dutch) |
| `java/` | Java: a number guessing game and a two-player dice game |

**Note:** these are course assignments and exercises. Some notebooks are based on material from the course teams (credited inside the notebooks where applicable). Outputs were cleared; datasets that belong to the course are not included. Code is shared to show how I work, not as a reference solution.

Other work: my MSc thesis on privacy threats in the agentic AI protocols MCP and A2A is in the [TU Delft repository](https://repository.tudelft.nl/record/uuid:d33074a3-a233-4b39-a9c6-69b48d8ec0f9).
