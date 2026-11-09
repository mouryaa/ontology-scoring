# A Methodology for Benchmarking Ontologies

### Proposal for the AI-Ready Data Team — Ontology Quality & AI-Readiness Scorecard (OQRS)

**Prepared by:** AI-Ready Data Team, Central AI & Data Strategy
**Status:** Draft for review
**Scope:** A repeatable, evidence-based method to score the ontologies we help business and data teams create, publish, and maintain.

---

## 1. Executive summary

We are asked to help teams across the firm build ontologies and to provide a mechanism for scoring or benchmarking them. This document proposes that mechanism.

**The central finding of the research is a distinction that changes the design of the benchmark.** The paper we were pointed to — *OntoURL* [1] — is not a benchmark for measuring ontologies. It is a benchmark for measuring **large language models** on ontology-related tasks: it asks whether an LLM can recall a class definition, infer a superclass, or draft ontology content from 43 public ontologies across eight domains, scored with accuracy, Entity-F1, BERTScore and Triple-F1. OntoURL tells us how *capable a model* is when it touches ontological knowledge. It does not tell us whether an ontology is *well built*. Those are two different measurements, and we need the second one.

The ontology-engineering field has spent two decades building exactly what we need. Its evaluation approaches are well catalogued and mature [14][16][17], and its instruments — logical reasoners, pitfall scanners, structural metrics, FAIR validators, competency-question test suites and ISO-aligned quality models — are implemented and free to use. What is missing, and what this proposal supplies, is (a) a **synthesis** of that literature into one operational scorecard, and (b) a new **AI-Readiness dimension** that reflects the firm's actual objective, and for which the LLM-era benchmarks such as OntoURL and LLMs4OL [26] are the right raw material.

**Recommendation:** adopt a weighted, multi-dimensional scorecard — the **Ontology Quality & AI-Readiness Scorecard (OQRS)** — with seven dimensions, automated measurement wherever possible, expert review for judgment calls, hard gating rules for logical defects, and a five-level maturity scale. It plugs into the ontology lifecycle at four gates, runs in CI/CD, and is itself validated for reliability before firm-wide rollout.

| # | Dimension | Weight | Primary evidence | Automation |
|---|---|:--:|---|:--:|
| D1 | Logical & Formal Soundness | 18 | Reasoner, OOPS!, OntoClean | High |
| D2 | Semantic Content Quality | 15 | Coverage metrics + expert rubric | Mixed |
| D3 | Requirements Coverage / Fitness for Purpose | 16 | Competency-question test suite | Mixed |
| D4 | Structural & Architectural Quality | 12 | OntoQA / OntoMetrics | High |
| D5 | FAIR, Publication & Technical Quality | 12 | FOOPS!, O'FAIRe | High |
| D6 | Governance, Maintainability & Reuse | 12 | Metadata + expert review | Low |
| D7 | **AI-Readiness & Machine Consumability** | 15 | Downstream A/B + LLM probe | Mixed |
| | **Composite OQRS** | **100** | | |

---

## 2. Why OntoURL is not the benchmark we need (and why it still matters)

### 2.1 What OntoURL actually measures

OntoURL builds the **URL Taxonomy** — *Understanding*, *Reasoning*, *Learning* — and instantiates it as 15 tasks over 36,159 instances drawn from 43 formal ontologies [1]. Understanding and Reasoning tasks are multiple-choice and scored by accuracy; Learning tasks are generative and scored by Entity-F1 (term extraction), BERTScore (definition generation) and Triple-F1 (hierarchy, property and constraint construction). It then evaluates 20 LLMs and reports how they vary by scale, task and domain.

Every one of those scores is a property of the **model**, not of the ontology. Change the model and the score changes; the ontology is held fixed as an input. The authors say as much in their own limitations section: their automatic metrics "do not fully capture semantic adequacy, logical consistency, ontology-design quality, or downstream usefulness," and because the source ontologies are public, the benchmark "should be interpreted as a benchmark of ontology-oriented behavior rather than a perfectly leakage-free test of unseen knowledge" [1].

### 2.2 What we actually need to measure

Our mandate is to help teams *create* ontologies and to judge whether what they produce is fit for purpose. That is the question of **ontology quality and fitness for purpose**, and it is a distinct, older, and better-instrumented research area. Its governing idea is that an ontology is an artefact with several independent quality facets: is it logically sound, is it structurally sound, does it say enough, does it say the right things, is it usable, is it reusable, and does it actually do the job it was built for [17][18].

Two further practical points sharpen the requirement:

- **Metrics alone are not quality.** Structural metrics such as class count, depth or relationship richness are cheap but easy to game, and a large ontology is not a good one [14][15]. Any credible method must pair automated metrics with semantic review and, critically, with **requirements-based validation** — does the ontology answer the questions it exists to answer [3][23][29].
- **The AI-readiness angle is real but must be measured carefully.** Since our goal is to make data AI-ready, a genuinely new question arises that pre-2020 frameworks do not address: *is this ontology a good substrate for AI systems — retrieval, grounding, agentic reasoning, analytics?* That is where the LLM-era work [1][26][27][28] earns its place — not as the scorecard, but as one dimension of it.

### 2.3 Where the field stands, and the gap we fill

A systematic mapping of LLM work to the industrial **LOT** ontology-engineering lifecycle found that tasks cluster around conceptualisation and encoding, while **ontology evaluation is essentially unaddressed** — "no approaches cover ontology evaluation so far" [27]. Complementary work proposes benchmarks for competency-question generation [29], ontology conceptualisation [28] and leakage-free evaluation [30], but none offers an integrated, deployable quality scorecard. That gap is precisely the artefact this proposal delivers.

---

## 3. Research synthesis: how ontologies are measured

The literature converges on a small number of evaluation *families* (McDaniel & Storey identify five [14]; earlier surveys group them similarly [16][17][18][32]). We reuse them as the raw material for the scorecard. Throughout, an ontology is taken in its standard sense — a formal, explicit specification of a shared conceptualisation [4], typically expressed in OWL [5] and serving as the schema layer of a knowledge graph [36].

**1. Golden-standard / comparative evaluation.** Compare the ontology against a reference ontology or a gold standard, measuring precision, recall and F1 over classes, properties and axioms [18]. *Used in:* D2, D3.

**2. Logical / formal evaluation.** Feed the ontology to a DL reasoner (HermiT, ELK, Pellet) to check consistency, satisfiability, coherence and unintended entailments; check meta-property correctness with **OntoClean**'s rigidity/identity/unity/dependence analysis [6]; and detect modelling anti-patterns with **OOPS!**, a catalogue of 41 pitfalls in Structural, Functional and Usability-Profiling dimensions, each graded critical/important/minor [7]. *Used in:* D1.

**3. Structural / metric-based evaluation.** Compute graph and schema metrics — **OntoQA**'s relationship richness, inheritance richness and attribute richness, plus instance metrics of class richness, cohesion and importance [12], extended by **OntoMetrics** [13]. Also covered: the **semiotic metrics suite** (syntactic, semantic, pragmatic, social) [11], operationalised in tools such as OntoKeeper [33]. *Used in:* D4, D2.

**4. Requirements-based / fitness-for-purpose evaluation.** *Competency questions* (CQs) state the ontology's functional requirements as questions it must be able to answer [3]; validation executes them as SPARQL against the data. **Test-driven development of ontologies** turns that into unit tests run in CI [23], and tools such as **Themis** validate an ontology against its requirements. *Used in:* D3.

**5. Quality-model evaluation.** **OQuaRE** adapts the ISO/IEC 25000 SQuaRE software-quality standard to ontologies, scoring characteristics including structural, functional adequacy, maintainability, operability, reliability and transferability on a 0–5 scale [9][10]; **OntoQualitas** applies a similar lens to information interchange between heterogeneous systems [25]; **ONTOMETRIC** scores suitability against a system's requirements [19]. *Used in:* the scoring model (D1–D6 rubric).

**6. FAIR / publication evaluation.** The FAIR principles [20] adapted to semantic artefacts, operationalised by **FOOPS!** (24 automated checks across Findable, Accessible, Interoperable, Reusable) [8] and by the metadata-driven **O'FAIRe** [21]. *Used in:* D5.

**7. Application- and data-driven evaluation.** Measure whether the ontology improves a downstream task (retrieval, annotation, integration, QA) or fits the data it is meant to describe [14][15]. *Used in:* D7.

**8. LLM-era evaluation (new).** OntoURL's understanding/reasoning/learning probe [1], LLMs4OL's nine ontology-learning task types [26], the benchmark proposals for conceptualisation [28] and CQs [29], and adjacent work on axiom identification [34], LLM-driven verification of ontology restrictions [39] and OntoClean-based refinement with LLMs [40]. Two methodological cautions from this literature are built into our design: **test-data leakage** — public ontologies are in model training data, so public-ontology scores are optimistic [30] — and **format/parse sensitivity**, where an unparsed answer is silently scored as wrong [1]. *Used in:* D7.

---

## 4. The proposed methodology: OQRS

### 4.1 Design principles

1. **Multi-dimensional and weighted.** Quality is not one number; it is several, combined transparently.
2. **Evidence-anchored.** Every score must cite an artefact — a reasoner log, a metric value, a test result, a reviewer note. No free-text scores.
3. **Automate the objective, review the subjective.** Reasoners, scanners and metric calculators run in CI; definition quality, coverage and governance are expert-reviewed against a written rubric.
4. **Gate, don't just score.** Certain defects block regardless of the composite, exactly as OOPS! treats *critical* pitfalls and as reasoners treat inconsistency [7].
5. **Fit-for-purpose first.** Requirements coverage carries weight comparable to formal soundness, so a pristine but useless ontology cannot score well.
6. **Reproducible and versioned.** Scores are produced by pinned tool versions against a pinned ontology release, so a score can be regenerated and audited.
7. **Bounded cost.** A full pass must be feasible for a real team: target ≤ 2 hours of expert time per ontology, with everything else automated.

### 4.2 Scoring scale and composite

Each criterion is scored **0–4**:

| Score | Anchor |
|:--:|---|
| 0 | Absent, or not assessable |
| 1 | Minimal — present but a serious weakness |
| 2 | Partial — present with material gaps |
| 3 | Substantial — sound, with minor gaps |
| 4 | Exemplary — meets or exceeds domain best practice |

Criterion scores are normalised to a fraction of 4 and averaged within a dimension to give a dimension score in `[0, 1]`; the composite is the weight-weighted sum, scaled to 100:

```
OQRS = 100 · Σ_d  w_d · ( mean of normalised criterion scores in d )
```

**Maturity levels:**

| Level | Composite | Meaning |
|:--:|:--:|---|
| **L1 — Ad hoc** | < 40 | Not fit for reuse; rebuild or restrict scope |
| **L2 — Developing** | 40–59 | Usable internally with caveats; gated from publication |
| **L3 — Defined** | 60–74 | Fit for internal semantic use; publishable |
| **L4 — Managed** | 75–89 | Fit for cross-domain reuse and AI grounding |
| **L5 — Optimised** | ≥ 90 | Reference-grade; candidate for firm standard |

### 4.3 Gating rules (override the composite)

| Gate | Condition | Effect |
|---|---|---|
| **G1 — Logical** | Ontology inconsistent, or any unsatisfiable class | **FAIL.** Cannot certify at any level until resolved |
| **G2 — Critical pitfalls** | Any OOPS! pitfall graded *critical* | Cap at **L2** |
| **G3 — Purpose** | D3 (Fitness for Purpose) < 2/4 | Not **AI-Ready certified** (L4/L5 withheld) |
| **G4 — Publication** | D5 (FAIR) < 50% | Cannot be registered/published or reused firm-wide |

Weights and gates are **policy**, not physics: they are set once, versioned, and tuned per ontology *type* (foundational/reference, domain, or application ontology), since a lightweight application ontology and a firm reference ontology should not be judged by identical thresholds.

---

## 5. The seven dimensions in detail

### D1 · Logical & Formal Soundness — weight 18

*Is the ontology logically correct?* The foundation of everything else, and the most automatable.

| Criterion | 0–4 anchors | Evidence / tool | Mode |
|---|---|---|---|
| Consistency & satisfiability | 4 = no unsatisfiable classes/individuals; 0 = outright inconsistency | HermiT / ELK / Pellet [1] | Auto |
| Coherence & no unintended entailments | 4 = no incoherent classes; domain/range axioms do not silently force other classes under a class | Reasoner explanations | Auto |
| Subsumption correctness (OntoClean) | 4 = no rigidity/identity/unity/dependence violations; 0 = pervasive anti-patterns | OntoClean meta-properties [6] | Mixed |
| Anti-pattern hygiene | 4 = no critical/important OOPS! pitfalls | OOPS! (41 pitfalls) [7] | Auto |
| Language/profile conformance | 4 = valid OWL 2 DL (or declared profile); no punning; no subClassOf cycles | ROBOT + OWL 2 validator | Auto |
| Axiom-level correctness | 4 = sample axioms semantically correct vs. domain intent | Expert sample review | Expert |

### D2 · Semantic Content Quality — weight 15

*Does it say enough, and is what it says clear?* Addresses the "semantic adequacy" gap OntoURL explicitly leaves open [1].

| Criterion | Evidence | Mode |
|---|---|---|
| Definition coverage (% classes & properties with a textual definition) | Coverage metric | Auto |
| Definition quality (genus–differentia / Aristotelian form, unambiguous) | Rubric sample review [2] | Expert |
| Label & synonym coverage (rdfs:label, skos:altLabel) | Coverage metric [8] | Auto |
| Semantic richness (axioms per class; non-taxonomic relations present) | OntoQA/OntoMetrics [12][13] | Auto |
| Lexical quality (naming conventions, no ambiguous or inconsistent labels) | Rubric | Expert |
| Domain coverage vs. stated scope | Scope/organisational mapping | Expert |

### D3 · Requirements Coverage / Fitness for Purpose — weight 16

*Does it answer the questions it exists to answer?* The literature is unambiguous that this is the decisive test of usefulness [3][14][23][29].

| Criterion | Evidence | Mode |
|---|---|---|
| Competency-question pass rate | CQs executed as SPARQL; % returning correct results | Mixed |
| Requirements breadth | # distinct CQs / requirements covered | Expert |
| Traceability | Each requirement mapped to ontology elements; ORSD maintained | Expert |
| Downstream task validation | Which business questions/capabilities it enables, evidenced | Expert |
| Test-suite presence | CQs + SHACL shapes + unit tests published and runnable | Auto |

A verdict of "AI-ready" requires D3 ≥ 3/4 **and** passing G3: an ontology that cannot answer the questions for which it was commissioned is not a semantic layer for AI, however elegant its axioms.

### D4 · Structural & Architectural Quality — weight 12

*Is it well shaped?* Cheap to compute, useful for diagnosing drift, but deliberately under-weighted because structure is not quality [14][15].

| Criterion | Evidence | Mode |
|---|---|---|
| Hierarchy health (no orphans, no tangled taxonomy, sensible depth/breadth) | OntoQA / OntoMetrics [12][13] | Auto |
| Relationship richness (ontological vs. purely taxonomic) | OntoQA relation richness [12] | Auto |
| Attribute richness (data properties) | OntoQA attribute richness [12] | Auto |
| Modularity (intra-module cohesion, inter-module coupling) | Module analysis | Auto |
| Reuse of upper ontologies / design patterns | Metadata + review | Mixed |
| IRI & naming conventions | Lint rules | Auto |

### D5 · FAIR, Publication & Technical Quality — weight 12

*Can others find, reach, understand and legally reuse it?* Directly operationalised by existing scanners [8][21].

| Criterion | Evidence | Mode |
|---|---|---|
| Findable (persistent, resolvable URI; version IRI; registry presence) | FOOPS! checks [8] | Auto |
| Accessible (content negotiation; open protocol; ≥1 RDF + HTML serialisation) | FOOPS! [8] | Auto |
| Interoperable (reuses external vocabularies; aligns to standards) | FOOPS! [8] | Auto |
| Reusable (documentation, licence, provenance, rich metadata) | FOOPS! / O'FAIRe [8][21] | Auto |
| Documentation quality (human-readable, WIDOCO-style) | Review | Mixed |

### D6 · Governance, Maintainability & Reuse — weight 12

*Will it survive contact with the firm?* A dimension that the academic frameworks name [9][16] but that only our internal process can actually evidence.

| Criterion | Evidence | Mode |
|---|---|---|
| Versioning & release discipline | Repo history, changelogs | Expert |
| Change & issue management | Issue tracker, review trail | Expert |
| Ownership & stewardship | Named owner, support model | Expert |
| Extensibility | Points of extension, modularity, pattern use | Expert |
| Licence clarity & IP | Licence metadata | Expert |
| Reuse signal (internal consumers, cross-team uptake) | Adoption register; LOV-style usage [35] | Expert |

### D7 · AI-Readiness & Machine Consumability — weight 15

*Is this ontology a good substrate for AI systems?* This is the firm's distinctive requirement and the one the classical frameworks do not cover. It is also where the LLM-era literature is used, carefully.

| Criterion | Evidence | Mode |
|---|---|---|
| Grounding utility | A/B: does the ontology measurably improve a real task (retrieval/RAG, entity resolution, analytics, agent tool-use) vs. no ontology? | Mixed |
| Machine-actionable formality | OWL 2 conformance, SHACL shapes for constraint validation, machine-readable metadata | Auto |
| Machine legibility probe | LLM accuracy on ontology-derived understanding/reasoning items (OntoURL-style [1]); higher scores under ceteris paribus indicate clearer, better-structured knowledge | Auto |
| Verbalisation robustness | Generated definitions/verbalisations scored for fidelity (BERTScore) and by review [28] | Mixed |
| Semantic separability | Do classes map to distinguishable vector regions / survive embedding-based clustering? | Auto |

**Two cautions we build in.** First, the legibility probe is a **comparative diagnostic of the ontology**, not a model leaderboard — we hold the model fixed and compare ontologies, and we use ontology-derived items that do not leak the gold answer. Second, **leakage control**: public ontologies (FIBO, schema.org) are in model training data, so scores on them are optimistic. Our internal ontologies are the opposite — genuinely unseen — and are therefore the *better* probe subjects, exactly as the leakage-aware proposal argues [30]. Where we do use public ontologies, we follow the *generate–evaluate–thrash* discipline: preferentially test on internal or synthetic ontologies, and treat public-ontology results as an upper bound [30].

---

## 6. Measurement instruments & tooling stack

| Need | Instrument | Dimension | Notes |
|---|---|---|---|
| Reasoning / consistency | HermiT, ELK, Pellet | D1 | Pin versions |
| Pitfall detection | OOPS! [7] | D1 | Gating by criticality |
| Meta-property analysis | OntoClean [6] | D1 | Semi-automated; expert-assisted |
| OWL validation & build | ROBOT, OWL 2 validators | D1, D4, D5 | CI-friendly |
| Structural metrics | OntoQA [12], OntoMetrics [13] | D2, D4 | Compute to a pinned report |
| Requirements testing | CQs + SPARQL, Themis [24], TDDontologies [23], SHACL [37] | D3 | The differentiator |
| FAIR validation | FOOPS! [8], O'FAIRe [21] | D5 | Fully automated |
| Documentation | WIDOCO | D5, D6 | Human-readable docs |
| LLM legibility probe | Harness adapted from OntoURL [1] / LLMs4OL [26] | D7 | Model fixed; ontology varied |
| Downstream A/B | Existing retrieval/QA/analytics benchmarks | D7 | Highest validity, highest cost |

The pipeline is standard **CI/CD for ontologies**: commit → build with ROBOT → reason → scan with OOPS!/FOOPS! → compute metrics → run CQ test suite → publish scorecard JSON + human-readable report. Every score is stored with the tool versions and the ontology release hash.

---

## 7. Operating model: where the scorecard plugs in

Mapped to the LOT lifecycle [22], which the LLM literature also uses as the reference frame [27]:

| Phase | Gate | What must pass |
|---|---|---|
| **Requirements specification** | **G-A: Purpose gate** | Scope, non-functional requirements and a written CQ set exist and are signed off by the business owner |
| **Implementation** | **G-B: Soundness gate** | Reasoner clean; no critical OOPS! pitfalls; CI lint green |
| **Publication** | **G-C: FAIR gate** | D5 ≥ 50%; resolvable URI, licence, documentation present |
| **Maintenance** | **G-D: Drift gate** | Scorecard re-run on each release; composite may not regress beyond a set tolerance without an owner-signed waiver |

**Who does what.** The ontology owner produces evidence and runs the automated pipeline. The AI-Ready Data team owns the rubric, the tool configuration and the certification. Domain experts supply CQs and perform the semantic-review criteria. A lightweight **Ontology Review Board** arbitrates borderline cases and approves waivers.

**Cadence.** Full scorecard at each major release; automated dimensions (D1, D4, D5, parts of D7) on every commit; expert dimensions (D2, D3, D6) at least twice a year and on material change.

**Certification output.** A one-page scorecard: composite, maturity level, dimension radar, gating status, and the top three remediation items with owners. This is the artefact leadership sees.

---

## 8. Worked example (illustrative)

A hypothetical internal **"Instrument & Product Reference Ontology (IPRO)"** aligned to FIBO [31], mid-development:

| Dimension | Raw /4 | Normalised | Weight | Contribution |
|---|:--:|:--:|:--:|:--:|
| D1 Logical & Formal | 2.8 | 0.70 | 18 | 12.6 |
| D2 Semantic Content | 2.2 | 0.55 | 15 | 8.3 |
| D3 Fitness for Purpose | 1.6 | 0.40 | 16 | 6.4 |
| D4 Structural | 3.2 | 0.80 | 12 | 9.6 |
| D5 FAIR | 3.0 | 0.75 | 12 | 9.0 |
| D6 Governance | 1.8 | 0.45 | 12 | 5.4 |
| D7 AI-Readiness | 1.8 | 0.45 | 15 | 6.8 |
| **Composite** | | | **100** | **58.1** |

**Result:** composite 58.1 → **L2 (Developing)**; gate **G3 triggered** (D3 = 0.40 < 0.50) → **not AI-Ready certified**. Top remediation: (1) complete the competency-question set and wire it to SPARQL tests; (2) lift definition coverage from ~40% to target; (3) close two important OOPS! pitfalls. Governance is upgraded to a named owner before the next release.

This example shows the intended behaviour: structurally tidy but not yet *useful enough to be certified* — and the scorecard says so plainly, with the three things to fix.

---

## 9. Validating the benchmark itself

A benchmark that has not been evaluated is a liability. Before firm-wide rollout, OQRS is validated on four axes, mirroring the discipline of the source benchmarks:

- **Content validity** — every dimension and criterion traces to a cited framework [6][7][8][12][14][16][17][23]; nothing is invented.
- **Inter-rater reliability** — two or three reviewers independently score a stratified sample; require Fleiss' κ ≥ 0.80 on expert-scored criteria, a bar the OntoURL authors themselves met (0.82–0.89 on syntax/semantics/quality) [1]. Criteria that fail reliability are rewritten or automated.
- **Discrimination & sensitivity** — the composite must separate ontologies a domain expert would call good from those they would not, and must move when a defect is fixed. Test on a spread of internal ontologies plus FIBO [31] and a deliberately broken control.
- **Predictive validity (the strongest test)** — does a higher OQRS score predict better performance on a downstream AI task (grounding, integration, retrieval)? If not, the weights are wrong and must be re-estimated against outcomes.

---

## 10. Implementation roadmap

| Phase | Timeline | Deliverables |
|---|---|---|
| **0 — Align** | Weeks 1–2 | Ratify dimensions, weights and gates with stakeholders; confirm ontology *types* and their thresholds |
| **1 — Instrument** | Weeks 3–6 | Stand up the CI pipeline (ROBOT + reasoner + OOPS! + FOOPS! + metrics); implement scorecard JSON + report template |
| **2 — Calibrate** | Weeks 7–10 | Pilot on 6–10 internal ontologies + FIBO; run inter-rater reliability; tune weights and anchors; publish rubric v1.0 |
| **3 — Validate** | Weeks 11–14 | Predictive-validity study against ≥ 1 downstream AI task; document results and limitations |
| **4 — Operationalise** | Quarter 2 | Wire gates into the ontology lifecycle; train owners; publish the certification register; begin quarterly re-scoring |

---

## 11. Limitations and risks

- **Metrics can be gamed.** Coverage and richness rise trivially with padding. Mitigated by the requirement gate (D3), expert review (D2/D6), and predictive validation (§9).
- **Subjectivity in expert dimensions.** Mitigated by written anchors, sample-based review and a κ ≥ 0.80 reliability bar.
- **LLM-probe interpretation.** An LLM's accuracy on ontology content is not a property of the ontology alone. We hold the model fixed, control for leakage [30], and treat the probe as comparative and diagnostic — never as the headline score.
- **Cost.** A full pass is real work. The automation split is designed to keep expert time near two hours per ontology.
- **Heterogeneity.** Foundational, domain and application ontologies differ in intent; one weight vector will not fit all, which is why weights are per-type and versioned.
- **Public-reference bias.** Scores calibrated on public ontologies inherit their conventions; internal calibration data must drive the final weights.

---

## 12. Recommendation

Adopt OQRS as the firm's ontology benchmark. It gives us three things OntoURL alone cannot: a defensible, multi-dimensional score of an ontology's **quality**; a hard requirement gate that keeps "pretty but useless" ontologies out of the AI-ready tier; and an **AI-Readiness** dimension that connects semantic quality directly to the AI outcomes we are chartered to deliver. It is built entirely from cited, established method — reasoners, OOPS!, FOOPS!, OntoQA/OntoMetrics, OQuaRE, competency questions and the FAIR principles — with the LLM-era benchmarks [1][26][28][29] used precisely where they add value, as a machine-legibility probe.

**Immediate next step:** approve Phase 0 (weights, gates and ontology types) so we can stand up the pipeline and calibrate on a real ontology in the next six weeks.

---

## Appendix A — How OntoURL's taxonomy maps onto OQRS

OntoURL's URL Taxonomy is a *capability* taxonomy for models; OQRS is a *quality* model for artefacts. They touch at exactly one point, D7.

| OntoURL capability | OntoURL tasks | OQRS use |
|---|---|---|
| Understanding (U1–U5) | Class definition, class relation, property semantics, instance class, instance description | Reused as the D7 machine-legibility probe (understanding subtasks) |
| Reasoning (R1–R5) | Inferred class relation, property constraint, inferred instance class, SWRL-style rules, DL satisfiability | Reused as the D7 probe (reasoning subtasks); DL satisfiability overlaps D1 |
| Learning (L1–L5) | Term extraction, definition generation, hierarchy/property/constraint construction | Not a quality measure of the ontology; useful separately as an *authoring-assist* evaluation, not part of OQRS |

## Appendix B — Source benchmarks and where they sit

| Benchmark / framework | Measures | Role in OQRS |
|---|---|---|
| OntoURL [1] | LLM capability on ontology tasks | D7 probe; framing distinction in §2 |
| LLMs4OL [26] | LLM ontology-learning tasks | D7 probe design |
| FOOPS! [8] | FAIR compliance of ontologies | D5, automated |
| OOPS! [7] | Ontology pitfalls | D1, gating |
| OQuaRE [9][10] | ISO 25000-aligned quality characteristics | D1–D6 rubric anchors |
| OntoQA [12] / OntoMetrics [13] | Structural metrics | D2, D4 |
| OntoClean [6] | Meta-property correctness | D1 |
| OntoQualitas [25] | Quality for heterogeneous interchange | D2, D6 anchors |
| Semantic metrics suite [11] | Syntactic/semantic/pragmatic/social quality | D2, D5, D6 anchors |
| McDaniel & Storey [14] | Five evaluation approaches | Overall framing (§3) |
| LOT [22] | Ontology lifecycle | Operating model (§7) |
| CQ benchmarks [29], TDD ontologies [23], Themis [24] | Requirements validation | D3 |
| Leakage-aware evaluation [30] | Evaluation hygiene | D7 method |

---

## References

All references below were verified against publisher/Crossref metadata or read in full from the source; DOIs are given where assigned.

[1] X. Zhang, H. Lai, Q. Meng, J. Bos. *OntoURL: A benchmark for evaluating large language models on symbolic ontological understanding, reasoning and learning.* Journal of Web Semantics 91 (2026) 100886. DOI: 10.1016/j.websem.2026.100886. (Read in full.)

[2] N. F. Noy, D. L. McGuinness. *Ontology Development 101: A Guide to Creating Your First Ontology.* Stanford KSL Technical Report KSL-01-05, 2001.

[3] M. Grüninger, M. S. Fox. *The Role of Competency Questions in Enterprise Engineering.* IFIP WG5.7 Workshop, Springer, 1995.

[4] T. R. Gruber. *A translation approach to portable ontology specifications.* Knowledge Acquisition 5(2):199–220, 1993.

[5] D. L. McGuinness, F. van Harmelen. *OWL Web Ontology Language Overview.* W3C Recommendation, 2004.

[6] N. Guarino, C. Welty. *Evaluating ontological decisions with OntoClean.* Communications of the ACM 45(2):61–65, 2002. DOI: 10.1145/503124.503150.

[7] M. Poveda-Villalón, A. Gómez-Pérez, M. C. Suárez-Figueroa. *OOPS! (OntOlogy Pitfall Scanner!): An On-line Tool for Ontology Evaluation.* International Journal on Semantic Web and Information Systems 10(2):7–34, 2014. DOI: 10.4018/ijswis.2014040102.

[8] D. Garijo, O. Corcho, M. Poveda-Villalón. *FOOPS!: An Ontology Pitfall Scanner for the FAIR Principles.* CEUR-WS Vol-2980, paper 321, 2021.

[9] A. Duque-Ramos, J. T. Fernández-Breis, M. Iniesta, M. Dumontier, M. Egaña Aranguren. *Evaluation of the OQuaRE framework for ontology quality.* Expert Systems with Applications 40(7):2696–2703, 2013. DOI: 10.1016/j.eswa.2012.11.004.

[10] A. Duque-Ramos, M. Boeker, L. Jansen, S. Schulz, M. Iniesta, J. T. Fernández-Breis. *Evaluating the Good Ontology Design Guideline (GoodOD) with the Ontology Quality Requirements and Evaluation Method and Metrics (OQuaRE).* PLoS ONE 9(8):e104463, 2014. DOI: 10.1371/journal.pone.0104463.

[11] A. Burton-Jones, V. C. Storey, V. Sugumaran, P. Ahluwalia. *A semiotic metrics suite for assessing the quality of ontologies.* Data & Knowledge Engineering 55(1):84–102, 2005. DOI: 10.1016/j.datak.2004.11.010.

[12] S. Tartir, I. B. Arpinar. *Ontology Evaluation and Ranking using OntoQA.* IEEE International Conference on Semantic Computing (ICSC), 2007. DOI: 10.1109/icsc.2007.19.

[13] B. Lantow. *OntoMetrics: Putting Metrics into Use for Ontology Evaluation.* KEOD/IC3K, 2016. DOI: 10.5220/0006084601860191.

[14] M. McDaniel, V. C. Storey. *Evaluating Domain Ontologies: Clarifying the Landscape.* ACM Computing Surveys 52(2), 2019. DOI: 10.1145/3329124.

[15] M. McDaniel, V. C. Storey, V. Sugumaran. *Assessing the quality of domain ontologies: Metrics and an automated ranking system.* Data & Knowledge Engineering 115:32–47, 2018. DOI: 10.1016/j.datak.2018.02.001.

[16] J. Raad, C. Cruz. *A Survey on Ontology Evaluation Methods.* KEOD/IC3K, 2015. DOI: 10.5220/0005591001790186.

[17] D. Vrandečić. *Ontology Evaluation.* In: Handbook on Ontologies, Springer, 2009, pp. 293–313. DOI: 10.1007/978-3-540-92673-3_13.

[18] A. Gómez-Pérez. *Ontology Evaluation.* In: Handbook on Ontologies, Springer, 2004. DOI: 10.1007/978-3-540-24750-0_13.

[19] A. Lozano-Tello, A. Gómez-Pérez. *ONTOMETRIC: A Method to Choose the Appropriate Ontology.* Journal of Database Management 15(2), 2004. DOI: 10.4018/jdm.2004040101.

[20] M. D. Wilkinson et al. *The FAIR Guiding Principles for scientific data management and stewardship.* Scientific Data 3:160018, 2016. DOI: 10.1038/sdata.2016.18.

[21] E. Amdouni, S. Bouazzouni, C. Jonquet. *O'FAIRe: Ontology FAIRness Evaluator in the AgroPortal Semantic Resource Repository.* ESWC 2022, LNCS. DOI: 10.1007/978-3-031-11609-4_17.

[22] M. Poveda-Villalón, A. Fernández-Izquierdo, M. Fernández-López, R. García-Castro. *LOT: An industrial oriented ontology engineering framework.* Engineering Applications of Artificial Intelligence 111:104755, 2022. DOI: 10.1016/j.engappai.2022.104755.

[23] C. M. Keet, A. Ławrynowicz. *Test-Driven Development of Ontologies.* ESWC 2016, LNCS, pp. 642–657. DOI: 10.1007/978-3-319-34129-3_39.

[24] A. Fernández-Izquierdo, R. García-Castro. *Themis: A Tool for Validating Ontologies through Requirements.* SEKE, 2019.

[25] M. Rico, M. L. Caliusco, O. Chiotti, M. R. Galli. *OntoQualitas: A framework for ontology quality assessment in information interchanges between heterogeneous systems.* Computers in Industry 65(9):1290–1300, 2014. DOI: 10.1016/j.compind.2014.07.010.

[26] H. Babaei Giglou, J. D'Souza, S. Auer. *LLMs4OL: Large Language Models for Ontology Learning.* ISWC 2023, LNCS, pp. 408–427. DOI: 10.1007/978-3-031-47240-4_22.

[27] D. Garijo, M. Poveda-Villalón, E. Amador-Domínguez, Z. Wang, R. García-Castro, O. Corcho. *LLMs for Ontology Engineering: A landscape of Tasks and Benchmarking challenges.* ISWC 2024 (HGAIS), CEUR-WS Vol-3953, paper 364, 2024.

[28] Y. Rebboud, P. Lisena, L. Tailhardat, R. Troncy. *Benchmarking LLM-based Ontology Conceptualization: A Proposal.* ISWC 2024 (HGAIS), CEUR-WS Vol-3953, paper 365, 2024.

[29] R. Alharbi, J. de Berardinis, F. Grasso, T. R. Payne, V. Tamma. *Characteristics and Desiderata for Competency Question Benchmarks.* ISWC 2024 (HGAIS), CEUR-WS Vol-3953, paper 369, 2024.

[30] H. Paulheim. *Towards Evaluating Knowledge Graph Construction and Ontology Learning with LLMs without Test Data Leakage.* KBC-LM/LM-KBC @ ISWC 2025, CEUR-WS Vol-4041, paper 2, 2025.

[31] M. Bennett. *The Financial Industry Business Ontology: Best practice for big data.* Journal of Banking Regulation 14:255–268, 2013. DOI: 10.1057/jbr.2013.13.

[32] M. Brank, M. Grobelnik, D. Mladenić. *A Survey of Ontology Evaluation Techniques.* Proc. Conf. on Data Mining and Data Warehouses (SiKDD), 2005.

[33] M. Amith et al. *OntoKeeper: Semiotic-driven Ontology Evaluation Tool for Biomedical Ontologists.* IEEE BIBM, 2018. DOI: 10.1109/bibm.2018.8621458.

[34] R. M. Bakker, D. L. Di Scala, M. H. T. de Boer, S. A. Raaijmakers. *Ontology Learning with LLMs: A Benchmark Study on Axiom Identification.* arXiv:2512.05594, 2025.

[35] P.-Y. Vandenbussche, G. A. Atemezing, M. Poveda-Villalón, B. Vatant. *Linked Open Vocabularies (LOV): A gateway to reusable semantic vocabularies on the Web.* Semantic Web 8(3):437–452, 2017. DOI: 10.3233/sw-160213.

[36] A. Hogan et al. *Knowledge Graphs.* ACM Computing Surveys 54(4), 2021. DOI: 10.1145/3447772.

[37] H. Knublauch, D. Kontokostas. *Shapes Constraint Language (SHACL).* W3C Recommendation, 2017.

[38] A. Miles, S. Bechhofer. *SKOS Simple Knowledge Organization System Reference.* W3C Recommendation, 2009.

[39] S. Tsaneva, S. Vasic, M. Sabou. *LLM-driven Ontology Evaluation: Verifying Ontology Restrictions with ChatGPT.* ESWC 2024 Satellite Events, 2024.

[40] Y. Zhao, N. Vetter, K. Aryan. *Using Large Language Models for OntoClean-based Ontology Refinement.* arXiv:2403.15864, 2024.

---

*Prepared from primary sources; all citations verified. OntoURL read in full; CEUR benchmark papers [8][27][28][29][30] read in full; remaining frameworks verified via Crossref/publisher metadata.*
