# Reports and papers

Individual papers and reflections, plus one group presentation from my MSc Complex Systems Engineering and Management (TU Delft) that sit at the technology side of my studies. Both PDFs are the versions I handed in, without my student number.

## Literature review: architectural requirements for the Digital Product Passport

[`dpp-architecture-literature-review.pdf`](dpp-architecture-literature-review.pdf) · SEN131B CoSEM Research Challenges · June 2025 · 11 pages

The EU is making Digital Product Passports (DPPs) mandatory for product groups such as electronics, textiles and batteries, but the technical side lags behind the regulation. This is a structured review of 12 peer-reviewed articles (2023-2025) on four architecture aspects: modular and layered design, interoperability, governance and scalability.

**Main findings (from the abstract):** most studies agree on modularity and standardisation, none cover all four aspects in depth, governance differs between blockchain-based and federated approaches, and the field moves towards hybrid systems that combine semantic data models with flexible control structures.

**What it shows:** a systematic literature search and selection (with a PRISMA-style approach), a comparison framework built on architecture concepts, and the link between a regulation and the system architecture needed to meet it. It also connects to the BattCycle platform report in [`../digital-platform-design`](../digital-platform-design), where the upcoming Digital Product Passport for batteries is part of the regulatory context.

## User-centred security: MFA fatigue in Zero Trust environments

[`mfa-fatigue-zero-trust-user-centred-security.pdf`](mfa-fatigue-zero-trust-user-centred-security.pdf) · TPM025B User-Centred Security · January 2026 · 10 pages

Zero Trust asks users to confirm their identity again and again. The paper treats MFA fatigue as a user-cost problem: authentication is a secondary task, and repeated prompts lead to habituation, so people approve reflexively and the protection MFA is meant to give disappears.

**The proposal:** a *Security Copilot*, an agentic security component in the user's daily environment. It keeps a dynamic trust state per session from signals such as device posture, session continuity, network context and timing, stays quiet while trust is high, and asks for a deliberately high-salience step-up verification only when the context deviates. The paper also covers target behaviour, an intervention framework, deployment, monitoring, maintenance, and conditions for success or failure (for example high false-positive rates, over-trust in automation, and privacy risks of the signals it uses).

**What it shows:** analysing a security problem through human behaviour and cost instead of only technology, designing an intervention with a plan to deploy and monitor it, and thinking about agentic AI in an authentication setting. The same interest drives my MSc thesis on privacy threats in the agentic AI protocols MCP and A2A.

## Digital sovereignty: multi/hybrid cloud architectures (research proposal)

[`hybrid-cloud-digital-sovereignty-research-proposal.pdf`](hybrid-cloud-digital-sovereignty-research-proposal.pdf) · SEN232A Master Thesis Research Design · January 2026 · 13 pages

My first thesis proposal, before I changed topic to privacy threats in MCP and A2A. European organisations depend heavily on a few non-European cloud providers, and multi- and hybrid cloud are often presented as the answer. The proposal asks how these architectures can be designed and governed to support digital sovereignty in the EU while reducing vendor lock-in. It links the EU Data Act, Gaia-X and the EU cloud certification scheme to concrete architecture and governance choices, and plans a design-oriented study: regulatory and literature analysis, a qualitative case study, and a framework to be evaluated. It is a proposal only; the study was not carried out.

**What it shows:** framing a technical architecture question with regulation and governance, and a clear research design (sub-questions, methods, data sources, planning).

## Policy and technology: Chat Control

[`chat-control-collaborative-governance.pdf`](chat-control-collaborative-governance.pdf) · SEN1141 Managing Multi-actor Decision-making · January 2025 · 9 pages

An individual paper on the EU's proposed Chat Control legislation, which would introduce client-side scanning to detect child sexual abuse material. It uses collaborative governance to analyse how stakeholders such as the EU institutions, tech companies, privacy advocates and child protection organisations see the trade-off between privacy and child protection, and what practical options could resolve the tension. An AI statement in the paper explains how a language model was used for structure only.

**What it shows:** a security and privacy technology (end-to-end encryption versus scanning) analysed through stakeholders and governance, which is the same angle I use in my thesis work.

## Design science reflection: the Smart Matter smart-home platform

[`smart-matter-service-design-reflection.pdf`](smart-matter-service-design-reflection.pdf) · SEN1622 I&C Service Design · January 2025 · 4 pages

My individual reflection on a group project to design an open-source, universal platform for managing smart-home IoT devices. It uses the design science research framework of Gregor and Hevner (2013) and looks at three things: the artifact, the theory behind the design, and the design process, including stakeholder feedback. The paper contains an AI statement. It is a reflection on a group project, not the group's report.

## Data and algorithms: the childcare benefits scandal (Dutch)

[`toeslagenschandaal-data-algorithms-essay.pdf`](toeslagenschandaal-data-algorithms-essay.pdf) · Data Science, TU Delft BSc TB · 2023 · 3 pages · in Dutch

An essay on what data and algorithms did and did not contribute to the harm in the Dutch toeslagenaffaire. It describes the double role of the technology: efficient decisions and fraud detection on one side, and the effects of biased, opaque decision-making on the other.

## Law and technology: the WGS opinion article (Dutch)

[`wgs-opinion-article-governance.pdf`](wgs-opinion-article-governance.pdf) · TB321 Governance, TU Delft BSc TB · 2024 · 2 pages with references · in Dutch

An opinion article on the Wet Gegevensverwerking door Samenwerkingsverbanden (WGS), the law that regulates how public and private parties share data to fight serious crime. It argues for the law while weighing privacy against security, and ends with the advice to look beyond legislation alone.

## Group presentation: digital infrastructure and cyberattacks

[`cybercrime-science-group-presentation.pdf`](cybercrime-science-group-presentation.pdf) · Cybercrime Science, TU Delft · November 2025 · 11 slides · group project (group 1)

*"To what extent does digital infrastructure quality explain cross-country variation in cyberattack frequency?"* The group combined the GSMA connectivity index (network coverage, network performance, spectrum availability) with a cyber event database. Because the attack counts were heavily skewed, with the United States dominating, they log-transformed the data and ran the analysis with and without the US. Pearson correlations showed that the infrastructure variables correlate with each other, so the models used OLS, Lasso and Ridge. OLS explained about 31% of the variance, and spectrum availability was the only infrastructure variable that predicted attack frequency consistently. The slides also cover limitations (connectivity as a proxy for security, reporting bias, one country dominating) and recommendations at policy, technical and institutional level.

This is group work, shown here as a PDF without names or student numbers. **My part:** *(to be filled in: which part of the analysis and presentation I did)*

## MSc thesis defence slides

[`thesis-defence-slides.pdf`](thesis-defence-slides.pdf) · 22 June 2026 · 49 slides (25 main slides and 24 backup slides)

The slides of my graduation defence on *Privacy Threats in MCP and A2A, Agentic AI Communication Protocols*. They give the fastest overview of the thesis: why privacy is exposed as agentic AI scales, how MCP and A2A work, the LINDDUN analysis of a financial fraud-detection scenario (54 threat entries, narrowed to 8), the validation with seven practitioners, and the conclusion that privacy has to move into the protocols themselves. The backup slides hold the data flows, scoring rubric, governance recommendations and anticipated questions. The full report is linked from the Research section of my site.

## Not included

Group reports with other authors, exam material and summaries are not included. The quantum-safe PKI paper that appears in my coursework folders was written by another student and is therefore not mine to publish.
