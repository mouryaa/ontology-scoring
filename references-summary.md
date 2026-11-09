# Reference Summaries — A Methodology for Benchmarking Ontologies

One-paragraph summaries of the 40 sources cited in `ontology-benchmark-proposal.md`, with the role each plays in the proposed Ontology Quality & AI-Readiness Scorecard (OQRS).

**Provenance note.** OntoURL [1] and the CEUR benchmark papers [8][27][28][29][30] were read in full. The remaining summaries are built from the proposal's own citations plus each paper's title, venue and publisher metadata — they state what the work is and what the proposal uses it for, not a page-level reading of every argument. Where a summary is title-level only, it says so.

---

## Core reference

**[1] OntoURL — Zhang, Lai, Meng & Bos (2026).** *OntoURL: A benchmark for evaluating large language models on symbolic ontological understanding, reasoning and learning.* Journal of Web Semantics 91, 100886. Read in full.

Introduces the **URL Taxonomy** — Understanding, Reasoning, Learning — and instantiates it as 15 tasks and 36,159 instances drawn from 43 ontologies across eight domains. Understanding and Reasoning tasks are multiple-choice scored by accuracy; Learning tasks are generative scored by Entity-F1, BERTScore and Triple-F1. Evaluates 20 open-source LLMs and reports variation by model scale, task and domain: models do well on explicit understanding and constrained reasoning, and struggle on structured construction (property-mediated relations, constraint-level outputs). A human baseline shows LLMs competitive or stronger on closed-form tasks, while humans remain better at property- and constraint-level construction.

*Role in OQRS:* the framing reference. Its key property for us is that **every score is a property of the model, not of the ontology** — the ontology is a fixed input. The authors concede their automatic metrics "do not fully capture semantic adequacy, logical consistency, ontology-design quality, or downstream usefulness," and that public source ontologies mean the benchmark is "a benchmark of ontology-oriented behavior rather than a perfectly leakage-free test of unseen knowledge." Those admissions define the gap OQRS fills. Its understanding and reasoning subtasks are reused as the D7 machine-legibility probe.

**[26] LLMs4OL — Babaei Giglou, D'Souza & Auer (2023).** *LLMs4OL: Large Language Models for Ontology Learning.* ISWC 2023, LNCS, pp. 408–427.

Frames ontology learning as a set of nine distinct task types spanning term typing, taxonomy discovery and non-taxonomic relation extraction, and benchmarks LLMs across them. Establishes that "ontology learning" is not one task but a family, each with its own evaluation protocol.

*Role in OQRS:* supplies the task decomposition used to design the D7 legibility probe — and the discipline of not treating "LLM on ontologies" as a single capability.

**[27] Garijo et al. (2024).** *LLMs for Ontology Engineering: A landscape of Tasks and Benchmarking challenges.* ISWC 2024 (HGAIS), CEUR-WS Vol-3953, paper 364. Read in full.

Maps the LLM-for-ontology-engineering literature onto the industrial **LOT** lifecycle. Finds that work clusters around conceptualisation and encoding, while **ontology evaluation is essentially unaddressed** — "no approaches cover ontology evaluation so far." Also catalogues the benchmarking challenges that follow from that absence.

*Role in OQRS:* the gap statement in §2.3. It is the evidence that no integrated, deployable quality scorecard exists to adopt off the shelf.

**[28] Rebboud, Lisena, Tailhardat & Troncy (2024).** *Benchmarking LLM-based Ontology Conceptualization: A Proposal.* ISWC 2024 (HGAIS), CEUR-WS Vol-3953, paper 365. Read in full.

Proposes a benchmark for the conceptualisation stage — how well an LLM turns requirements or source material into candidate classes, relations and axioms — including how to score generated verbalisations for fidelity rather than fluency.

*Role in OQRS:* the D7 *verbalisation robustness* criterion, scored with BERTScore plus review.

**[29] Alharbi, de Berardinis, Grasso, Payne & Tamma (2024).** *Characteristics and Desiderata for Competency Question Benchmarks.* ISWC 2024 (HGAIS), CEUR-WS Vol-3953, paper 369. Read in full.

Sets out what a competency-question benchmark must satisfy to be useful — coverage, discriminative power, reproducibility — and why CQ quality is the binding constraint on requirements-based ontology evaluation.

*Role in OQRS:* hardens D3. The desiderata became the design rules for our CQ test suite, and the paper is part of the evidence that requirements coverage is the decisive usefulness test.

**[30] Paulheim (2025).** *Towards Evaluating Knowledge Graph Construction and Ontology Learning with LLMs without Test Data Leakage.* KBC-LM/LM-KBC @ ISWC 2025, CEUR-WS Vol-4041, paper 2. Read in full.

Argues that public ontologies and public benchmarks sit inside LLM training data, so scores on them are optimistic, and sets out a *generate–evaluate–thrash* discipline for evaluation that does not leak the gold answer.

*Role in OQRS:* the leakage-control rule in D7. It is why we prefer internal or synthetic ontologies as probe subjects and treat public-ontology results as an upper bound.

**[8] FOOPS! — Garijo, Corcho & Poveda-Villalón (2021).** *FOOPS!: An Ontology Pitfall Scanner for the FAIR Principles.* CEUR-WS Vol-2980, paper 321. Read in full.

Automated FAIR-compliance scanner for ontologies: 24 checks across Findable, Accessible, Interoperable and Reusable, run against a live ontology URI and returning per-check results.

*Role in OQRS:* the engine for D5. Because it is fully automated and returns structured results, D5 runs on every commit and its output doubles as the FAIR gate (G4).

## Ontology quality and evaluation frameworks

**[2] Noy & McGuinness (2001).** *Ontology Development 101: A Guide to Creating Your First Ontology.* Stanford KSL Technical Report KSL-01-05.

The canonical practitioner guide. Presents an iterative development process — determine scope, consider reuse, enumerate terms, define classes and properties, define facets, create instances — and the genus–differentia pattern for writing class definitions.

*Role in OQRS:* the rubric anchor for *definition quality* in D2 (Aristotelian form, unambiguous) and the reference process for scope statements in D3.

**[3] Grüninger & Fox (1995).** *The Role of Competency Questions in Enterprise Engineering.* IFIP WG5.7 Workshop, Springer.

Origin of the competency-question idea: an ontology's requirements are stated as the questions it must be able to answer, and the ontology is judged by whether it can answer them.

*Role in OQRS:* the conceptual basis of D3 and of the G3 purpose gate. An ontology that cannot answer its own CQs is not fit for purpose, however clean its axioms.

**[4] Gruber (1993).** *A translation approach to portable ontology specifications.* Knowledge Acquisition 5(2):199–220.

The paper that gave the field its working definition: an ontology is "an explicit specification of a conceptualisation." Also sets out the portability and commitment issues that follow from making that specification formal.

*Role in OQRS:* definitional framing in §3 — the sense in which "ontology" is used throughout the scorecard.

**[5] McGuinness & van Harmelen (2004).** *OWL Web Ontology Language Overview.* W3C Recommendation.

The normative overview of OWL: its three species (Lite, DL, Full), the class/property/individual constructs, and what each buys in expressivity and reasoning cost.

*Role in OQRS:* the conformance target for D1 *language/profile conformance* and D7 *machine-actionable formality*.

**[6] Guarino & Welty (2002).** *Evaluating ontological decisions with OntoClean.* Communications of the ACM 45(2):61–65. DOI: 10.1145/503124.503150.

Introduces meta-properties — rigidity, identity, unity, dependence — and shows how they expose modelling errors that a reasoner cannot catch: a subclass that is not really a subclass, a role mistaken for a type. OntoClean's contribution is that taxonomic correctness is a semantic judgement, not a logical one.

*Role in OQRS:* the *subsumption correctness* criterion in D1, and the reason D1 is scored "Mixed" rather than "Auto" — a reasoner will happily accept a taxonomically wrong hierarchy.

**[7] OOPS! — Poveda-Villalón, Gómez-Pérez & Suárez-Figueroa (2014).** *OOPS! (OntOlogy Pitfall Scanner!): An On-line Tool for Ontology Evaluation.* International Journal on Semantic Web and Information Systems 10(2):7–34. DOI: 10.4018/ijswis.2014040102.

A catalogue of 41 ontology pitfalls organised into Structural, Functional and Usability-Profiling dimensions, each graded critical, important or minor, implemented as an online scanner that takes an ontology URI and returns per-pitfall findings.

*Role in OQRS:* the anti-pattern engine in D1 and the model for gating by severity — G2 caps an ontology at L2 if any *critical* pitfall is present. Also the template for "gate, don't just score."

**[9] Duque-Ramos et al. (2013).** *Evaluation of the OQuaRE framework for ontology quality.* Expert Systems with Applications 40(7):2696–2703. DOI: 10.1016/j.eswa.2012.11.004.

Adapts the ISO/IEC 25000 SQuaRE software-quality standard to ontologies, defining characteristics (structural, functional adequacy, maintainability, operability, reliability, transferability) and scoring them on a 0–5 scale. Reports on applying the framework to real ontologies.

*Role in OQRS:* the strongest single precedent for a multi-characteristic, ISO-aligned ontology quality model, and the anchor for D1–D6 rubric language.

**[10] Duque-Ramos et al. (2014).** *Evaluating the Good Ontology Design Guideline (GoodOD) with the Ontology Quality Requirements and Evaluation Method and Metrics (OQuaRE).* PLoS ONE 9(8):e104463. DOI: 10.1371/journal.pone.0104463.

Uses OQuaRE to evaluate whether following the GoodOD design guideline actually improves ontology quality — evidence that design discipline shows up in measurable quality characteristics.

*Role in OQRS:* supports the weighting logic (process discipline in D6 is not decorative) and the D2 definition-quality anchors.

**[11] Burton-Jones, Storey, Sugumaran & Ahluwalia (2005).** *A semiotic metrics suite for assessing the quality of ontologies.* Data & Knowledge Engineering 55(1):84–102. DOI: 10.1016/j.datak.2004.11.010.

Applies semiotics to ontology quality with four metric families — syntactic, semantic, pragmatic and social — arguing that an ontology's quality is partly a property of how well it communicates to its users, not only of its formal structure.

*Role in OQRS:* anchors the lexical-quality and documentation criteria in D2, D5 and D6, and justifies treating "understandable to people" as a quality dimension separate from "logically correct."

**[12] OntoQA — Tartir & Arpinar (2007).** *Ontology Evaluation and Ranking using OntoQA.* IEEE ICSC 2007. DOI: 10.1109/icsc.2007.19.

Defines computable schema and knowledge-base metrics — relationship richness, inheritance richness, attribute richness, and instance-level class richness, cohesion and importance — and uses them to rank ontologies.

*Role in OQRS:* the metric definitions behind D4 *hierarchy health*, *relationship richness* and *attribute richness*, and part of D2 *semantic richness*.

**[13] OntoMetrics — Lantow (2016).** *OntoMetrics: Putting Metrics into Use for Ontology Evaluation.* KEOD/IC3K 2016. DOI: 10.5220/0006084601860191.

Packages ontology metrics into a usable evaluation platform, extending the OntoQA family with additional schema and knowledge-base measures.

*Role in OQRS:* the practical implementation we compute D4 against, and a second source for D2 richness.

**[14] McDaniel & Storey (2019).** *Evaluating Domain Ontologies: Clarifying the Landscape.* ACM Computing Surveys 52(2). DOI: 10.1145/3329124.

Systematic review that sorts the evaluation literature into five approaches and argues that no single approach is sufficient — structural metrics in particular are cheap but do not establish quality.

*Role in OQRS:* the overall framing of §3 and the justification for a multi-dimensional scorecard rather than a metrics-only one. Also the source of the "metrics alone are not quality" caution.

**[15] McDaniel, Storey & Sugumaran (2018).** *Assessing the quality of domain ontologies: Metrics and an automated ranking system.* Data & Knowledge Engineering 115:32–47. DOI: 10.1016/j.datak.2018.02.001.

Builds an automated ranking system from quality metrics for domain ontologies and tests whether the ranking agrees with expert judgement.

*Role in OQRS:* precedent for automated composite scoring, and the caution that a large ontology is not a good one — which is why D4 carries only weight 12.

**[16] Raad & Cruz (2015).** *A Survey on Ontology Evaluation Methods.* KEOD/IC3K 2015. DOI: 10.5220/0005591001790186.

Survey that groups ontology evaluation methods by what they assess and how, and notes the field's lack of convergence on a single standard.

*Role in OQRS:* corroborates the five-family grouping in §3 and the claim that the field is mature but fragmented.

**[17] Vrandečić (2009).** *Ontology Evaluation.* In: Handbook on Ontologies, Springer, pp. 293–313. DOI: 10.1007/978-3-540-92673-3_13.

Handbook chapter that lays out the evaluation problem systematically: what can be checked automatically, what requires a human, and why "fitness for purpose" is the governing criterion rather than correctness alone.

*Role in OQRS:* the intellectual spine of the "several independent quality facets" argument in §2.2 and the automated/expert split in the design principles.

**[18] Gómez-Pérez (2004).** *Ontology Evaluation.* In: Handbook on Ontologies, Springer. DOI: 10.1007/978-3-540-24750-0_13.

Earlier handbook treatment centred on comparing an ontology to a golden standard — precision, recall and F1 over classes, properties and axioms — plus consistency checking.

*Role in OQRS:* the golden-standard / comparative family in §3, used in D2 and D3.

**[19] ONTOMETRIC — Lozano-Tello & Gómez-Pérez (2004).** *ONTOMETRIC: A Method to Choose the Appropriate Ontology.* Journal of Database Management 15(2). DOI: 10.4018/jdm.2004040101.

A multi-criteria decision method for choosing among candidate ontologies, scoring each against a system's requirements rather than in the abstract.

*Role in OQRS:* supports the "fit for purpose first" principle and the idea that weights are policy set against intended use, not universal constants.

**[25] OntoQualitas — Rico, Caliusco, Chiotti & Galli (2014).** *OntoQualitas: A framework for ontology quality assessment in information interchanges between heterogeneous systems.* Computers in Industry 65(9):1290–1300. DOI: 10.1016/j.compind.2014.07.010.

A quality framework aimed at the practical case of exchanging information between heterogeneous systems — quality judged by whether the ontology supports the interchange it was built for.

*Role in OQRS:* anchors D2 and D6 criteria and reinforces the requirements-first stance: quality is relative to a task, not absolute.

**[32] Brank, Grobelnik & Mladenić (2005).** *A Survey of Ontology Evaluation Techniques.* Proc. SiKDD 2005.

Early survey grouping evaluation techniques into golden-standard comparison, application-based evaluation, data-driven evaluation and structural/metric approaches.

*Role in OQRS:* the historical taxonomy behind the five families in §3; also a title-level citation used for the claim that earlier surveys group the field similarly.

**[33] OntoKeeper — Amith et al. (2018).** *OntoKeeper: Semiotic-driven Ontology Evaluation Tool for Biomedical Ontologists.* IEEE BIBM 2018. DOI: 10.1109/bibm.2018.8621458.

A tool that operationalises semiotic metrics for biomedical ontologists — an example of turning an evaluation theory into a scanner practitioners actually run.

*Role in OQRS:* evidence that semiotic metrics are implementable and usable by non-specialists; a reference point for the "automate the objective" principle.

## Requirements, testing and FAIR

**[20] Wilkinson et al. (2016).** *The FAIR Guiding Principles for scientific data management and stewardship.* Scientific Data 3:160018. DOI: 10.1038/sdata.2016.18.

The FAIR principles — Findable, Accessible, Interoperable, Reusable — stated as data-management requirements rather than quality judgements.

*Role in OQRS:* the definition of the D5 criteria. FAIR is necessary but not sufficient for ontology quality, which is why D5 carries weight 12 rather than more.

**[21] O'FAIRe — Amdouni, Bouazzouni & Jonquet (2022).** *O'FAIRe: Ontology FAIRness Evaluator in the AgroPortal Semantic Resource Repository.* ESWC 2022, LNCS. DOI: 10.1007/978-3-031-11609-4_17.

A metadata-driven FAIRness evaluator for ontologies hosted in AgroPortal, producing a FAIR score from the repository's metadata rather than from the ontology file.

*Role in OQRS:* a second, metadata-based D5 instrument, complementing FOOPS!'s URI-based checks.

**[22] LOT — Poveda-Villalón, Fernández-Izquierdo, Fernández-López & García-Castro (2022).** *LOT: An industrial oriented ontology engineering framework.* Engineering Applications of Artificial Intelligence 111:104755. DOI: 10.1016/j.engappai.2022.104755.

An industrial ontology-engineering framework that defines a lifecycle from requirements specification through implementation, publication and maintenance, with explicit deliverables and roles.

*Role in OQRS:* the lifecycle skeleton for §7. Our four gates (G-A to G-D) are mapped onto LOT's phases, which also makes the scorecard legible to teams already following LOT.

**[23] Keet & Ławrynowicz (2016).** *Test-Driven Development of Ontologies.* ESWC 2016, LNCS, pp. 642–657. DOI: 10.1007/978-3-319-34129-3_39.

Applies test-driven development to ontologies: write competency questions as executable unit tests first, then build the ontology until the tests pass. Makes requirements coverage a CI artefact rather than a review opinion.

*Role in OQRS:* the design pattern for D3's automated side — CQs as SPARQL tests run on every commit.

**[24] Themis — Fernández-Izquierdo & García-Castro (2019).** *Themis: A Tool for Validating Ontologies through Requirements.* SEKE 2019.

A tool that checks an ontology against its stated requirements and reports which are satisfied and which are not — requirements validation as a repeatable operation rather than a one-off review.

*Role in OQRS:* the reference implementation for D3 traceability and test-suite presence.

**[37] SHACL — Knublauch & Kontokostas (2017).** *Shapes Constraint Language (SHACL).* W3C Recommendation.

A W3C language for expressing constraints over RDF graphs as shapes, with validation reports that name the offending node and constraint.

*Role in OQRS:* the constraint-validation layer in D3 (test-suite presence) and D7 (machine-actionable formality) — SHACL shapes are how "the ontology's rules are executable" becomes a checkable fact.

**[38] SKOS — Miles & Bechhofer (2009).** *SKOS Simple Knowledge Organization System Reference.* W3C Recommendation.

The W3C standard for publishing concept schemes — labels, alternative labels, broader/narrower relations, definitions — as lightweight, linked vocabulary.

*Role in OQRS:* the reference for D2 *label and synonym coverage* (skos:altLabel) and for judging lexical quality in vocabularies that are not full OWL ontologies.

## LLM-era and application-specific work

**[31] Bennett (2013).** *The Financial Industry Business Ontology: Best practice for big data.* Journal of Banking Regulation 14:255–268. DOI: 10.1057/jbr.2013.13.

Describes FIBO, the financial-industry reference ontology: its scope, its development as an industry standard, and its use as best practice for big-data semantics in finance.

*Role in OQRS:* the public reference ontology used in the worked example and in calibration (§8–9) — and, because it is public and therefore likely in training data, a deliberate example of the leakage caveat in D7.

**[34] Bakker, Di Scala, de Boer & Raaijmakers (2025).** *Ontology Learning with LLMs: A Benchmark Study on Axiom Identification.* arXiv:2512.05594.

Benchmarks LLMs specifically on axiom identification — the hardest part of ontology learning, where the model must decide what logical constraint to assert, not just what class to name.

*Role in OQRS:* adjacent evidence for D7: it isolates a task where model capability and ontology clarity interact, supporting the "comparative diagnostic" framing of the legibility probe.

**[35] LOV — Vandenbussche, Atemezing, Poveda-Villalón & Vatant (2017).** *Linked Open Vocabularies (LOV): A gateway to reusable semantic vocabularies on the Web.* Semantic Web 8(3):437–452. DOI: 10.3233/sw-160213.

Describes LOV, a curated registry of reusable semantic vocabularies with usage statistics — a working model of how reuse is made visible and measurable.

*Role in OQRS:* the model for the D6 *reuse signal* criterion — an adoption register that shows who actually consumes the ontology, not just who published it.

**[36] Hogan et al. (2021).** *Knowledge Graphs.* ACM Computing Surveys 54(4). DOI: 10.1145/3447772.

A broad survey of knowledge graphs: their data models, schema layers, query languages, identities and applications. Establishes the ontology's place as the schema layer above instance data.

*Role in OQRS:* framing in §3 — an ontology is the schema layer of a knowledge graph, which is why structural and semantic quality both matter for downstream AI use.

**[39] Tsaneva, Vasic & Sabou (2024).** *LLM-driven Ontology Evaluation: Verifying Ontology Restrictions with ChatGPT.* ESWC 2024 Satellite Events.

Tests whether an LLM can verify that an ontology's restrictions (cardinalities, domains, ranges, disjointness) match the intended meaning — using the model as a reviewer of formal constraints.

*Role in OQRS:* evidence that LLMs can assist the expert-scored criteria in D1, and a caution that such checks need a fixed model and a controlled protocol to be comparable.

**[40] Zhao, Vetter & Aryan (2024).** *Using Large Language Models for OntoClean-based Ontology Refinement.* arXiv:2403.15864.

Uses an LLM to find and propose fixes for OntoClean meta-property violations — automating part of what is normally an expert-only taxonomic review.

*Role in OQRS:* supports scoring D1 subsumption correctness as "Mixed" rather than "Expert": LLM-assisted triage is feasible, with expert sign-off on the findings.

---

## How the 40 sources map to the seven dimensions

| Dimension | Principal sources |
|---|---|
| D1 Logical & Formal Soundness | [5] OWL, [6] OntoClean, [7] OOPS!, [9][10] OQuaRE, [39][40] LLM-assisted checks |
| D2 Semantic Content Quality | [2] Ontology 101, [11] semiotic metrics, [12] OntoQA, [13] OntoMetrics, [25] OntoQualitas, [33] OntoKeeper, [38] SKOS |
| D3 Requirements / Fitness for Purpose | [3] competency questions, [23] TDD ontologies, [24] Themis, [29] CQ benchmark desiderata, [37] SHACL |
| D4 Structural & Architectural Quality | [12] OntoQA, [13] OntoMetrics, [14][15] McDaniel, [33] OntoKeeper |
| D5 FAIR & Technical Quality | [8] FOOPS!, [20] FAIR, [21] O'FAIRe |
| D6 Governance, Maintainability & Reuse | [9][10] OQuaRE, [11] semiotic metrics, [22] LOT, [25] OntoQualitas, [35] LOV |
| D7 AI-Readiness & Machine Consumability | [1] OntoURL, [26] LLMs4OL, [28] conceptualisation benchmark, [30] leakage control, [34] axiom identification, [37] SHACL |
| Framing / synthesis | [4] Gruber, [14][16][17][18][32] surveys and handbook chapters, [19] ONTOMETRIC, [27] landscape, [31] FIBO, [36] knowledge graphs |
