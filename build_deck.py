"""Build the OQRS proposal deck (Situation - Complication - Proposal).

Run: python3 build_deck.py
Output: ./out/oqrs-scp-deck.pptx
"""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

# ---------------------------------------------------------------- palette
NAVY = RGBColor(0x0B, 0x1F, 0x3A)
NAVY_LIGHT = RGBColor(0x16, 0x33, 0x57)
TEAL = RGBColor(0x1B, 0x7F, 0x79)
TEAL_PALE = RGBColor(0xE4, 0xF1, 0xEF)
AMBER = RGBColor(0xB4, 0x7E, 0x1F)
AMBER_PALE = RGBColor(0xFA, 0xF2, 0xE0)
RED = RGBColor(0xA3, 0x3A, 0x2E)
GRAY = RGBColor(0x5A, 0x64, 0x72)
GRAY_LIGHT = RGBColor(0x8A, 0x93, 0x9E)
RULE = RGBColor(0xD5, 0xDA, 0xE0)
BG = RGBColor(0xF7, 0xF8, 0xFA)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

FONT = "Arial"

SW, SH = 13.333, 7.5
M = 0.62  # left/right margin

prs = Presentation()
prs.slide_width = Inches(SW)
prs.slide_height = Inches(SH)
BLANK = prs.slide_layouts[6]

NO_STYLE_NO_GRID = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"


# ---------------------------------------------------------------- helpers
def txt(slide, x, y, w, h, text, size=14, bold=False, color=NAVY,
        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=1.0,
        italic=False, font=FONT, space_after=0):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    lines = text.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        p.space_after = Pt(space_after)
        r = p.add_run()
        r.text = line
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = color
        r.font.name = font
    return box


def rect(slide, x, y, w, h, fill=None, line=None, shape=MSO_SHAPE.RECTANGLE,
         line_w=0.75):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(line_w)
    s.shadow.inherit = False
    if s.has_text_frame:
        s.text_frame.text = ""
    return s


def base_slide(tag, title, sub=None):
    slide = prs.slides.add_slide(BLANK)
    rect(slide, 0, 0, SW, SH, fill=WHITE)
    # section tag + rule
    txt(slide, M, 0.42, 6.0, 0.24, tag.upper(), size=10.5, bold=True, color=TEAL)
    txt(slide, M, 0.72, SW - 2 * M, 0.75, title, size=25, bold=True, color=NAVY,
        spacing=0.95)
    rect(slide, M, 1.62, 1.1, 0.045, fill=TEAL)
    if sub:
        txt(slide, M, 1.78, SW - 2 * M, 0.55, sub, size=13.5, color=GRAY,
            spacing=1.12)
    return slide


def footer(slide, num):
    rect(slide, M, 6.98, SW - 2 * M, 0.012, fill=RULE)
    txt(slide, M, 7.06, 6.0, 0.22, "OQRS  ·  AI-Ready Data Team  ·  Draft for review",
        size=9, color=GRAY_LIGHT)
    txt(slide, SW - M - 1.2, 7.06, 1.2, 0.22, str(num), size=9, color=GRAY_LIGHT,
        align=PP_ALIGN.RIGHT)


def so_what(slide, text, y=6.28):
    rect(slide, M, y, 0.045, 0.44, fill=AMBER)
    txt(slide, M + 0.22, y + 0.02, SW - 2 * M - 0.3, 0.44, text, size=12.5,
        bold=True, color=NAVY, spacing=1.05)


def card(slide, x, y, w, h, head, body, accent=TEAL, head_size=13.5,
         body_size=11.5, fill=BG):
    rect(slide, x, y, w, h, fill=fill, line=RULE)
    rect(slide, x, y, w, 0.055, fill=accent)
    txt(slide, x + 0.22, y + 0.24, w - 0.44, 0.5, head, size=head_size,
        bold=True, color=NAVY, spacing=1.0)
    txt(slide, x + 0.22, y + 0.78, w - 0.44, h - 0.95, body, size=body_size,
        color=GRAY, spacing=1.16)


def section_slide(num, letter, title, count):
    slide = prs.slides.add_slide(BLANK)
    rect(slide, 0, 0, SW, SH, fill=NAVY)
    rect(slide, 0, 0, 0.14, SH, fill=TEAL)
    txt(slide, M + 0.3, 1.55, 2.0, 0.3, f"SECTION {num}", size=11, bold=True,
        color=TEAL)
    txt(slide, M + 0.25, 1.9, 2.2, 2.4, letter, size=150, bold=True,
        color=NAVY_LIGHT)
    txt(slide, M + 2.05, 2.35, 9.4, 1.5, title, size=34, bold=True, color=WHITE,
        spacing=1.02)
    txt(slide, M + 2.1, 4.0, 9.0, 0.4, count, size=12.5, color=GRAY_LIGHT)
    return slide


def set_cell(cell, text, size=11.5, bold=False, color=NAVY,
             align=PP_ALIGN.LEFT, fill=None):
    cell.margin_left = Inches(0.1)
    cell.margin_right = Inches(0.08)
    cell.margin_top = Inches(0.04)
    cell.margin_bottom = Inches(0.04)
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    if fill is not None:
        cell.fill.solid()
        cell.fill.fore_color.rgb = fill
    tf = cell.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = 0.95
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    r.font.name = FONT


def table(slide, x, y, col_w, rows, row_h=0.36, head_h=0.42, size=11.5,
          aligns=None, emphasis_last=False, head_size=None):
    n_rows, n_cols = len(rows), len(col_w)
    shp = slide.shapes.add_table(
        n_rows, n_cols, Inches(x), Inches(y),
        Inches(sum(col_w)), Inches(head_h + row_h * (n_rows - 1)))
    tbl = shp.table
    tblPr = tbl._tbl.tblPr
    for el in tblPr.findall(qn("a:tableStyleId")):
        tblPr.remove(el)
    sid = tblPr.makeelement(qn("a:tableStyleId"), {})
    sid.text = NO_STYLE_NO_GRID
    tblPr.append(sid)
    tbl.first_row = False
    tbl.horz_banding = False
    tbl.vert_banding = False

    for i, w in enumerate(col_w):
        tbl.columns[i].width = Inches(w)
    for r in range(n_rows):
        tbl.rows[r].height = Inches(head_h if r == 0 else row_h)

    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = tbl.cell(r, c)
            al = aligns[c] if aligns else PP_ALIGN.LEFT
            if r == 0:
                set_cell(cell, val, size=head_size or size, bold=True,
                         color=WHITE, align=al, fill=NAVY)
            else:
                last = emphasis_last and r == n_rows - 1
                fill = TEAL_PALE if last else (WHITE if r % 2 else BG)
                set_cell(cell, val, size=size, bold=last, color=NAVY,
                         align=al, fill=fill)
    return tbl


def pill(slide, x, y, w, h, text, fill=TEAL_PALE, color=TEAL, size=10):
    s = rect(slide, x, y, w, h, fill=fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    s.adjustments[0] = 0.25
    tf = s.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_right = Inches(0.12)
    tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = True
    r.font.color.rgb = color
    r.font.name = FONT


# ================================================================ 1. cover
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, SW, SH, fill=NAVY)
rect(s, 0, 0, 0.16, SH, fill=TEAL)
txt(s, M + 0.35, 1.15, 8.0, 0.28, "AI-READY DATA TEAM  ·  CENTRAL AI & DATA STRATEGY",
    size=11, bold=True, color=TEAL)
txt(s, M + 0.35, 1.62, 10.6, 2.1,
    "Benchmarking Ontologies\nfor AI Readiness", size=42, bold=True, color=WHITE,
    spacing=1.0)
rect(s, M + 0.35, 3.62, 1.6, 0.05, fill=TEAL)
txt(s, M + 0.35, 3.92, 9.6, 0.5,
    "The Ontology Quality & AI-Readiness Scorecard (OQRS)", size=21,
    color=RGBColor(0xD8, 0xDE, 0xE6))
txt(s, M + 0.35, 4.55, 9.6, 0.9,
    "A repeatable, evidence-based method to score the ontologies we help business\n"
    "and data teams create, publish and maintain.", size=13.5,
    color=GRAY_LIGHT, spacing=1.25)
# SCP rail
for i, (letter, label) in enumerate([("S", "Situation"), ("C", "Complication"),
                                     ("P", "Proposal")]):
    x = 10.55
    y = 1.95 + i * 0.72
    txt(s, x, y, 0.42, 0.42, letter, size=19, bold=True, color=TEAL)
    txt(s, x + 0.42, y + 0.06, 2.0, 0.3, label, size=11.5, color=GRAY_LIGHT)
txt(s, M + 0.35, 6.45, 9.0, 0.28, "Draft for review  ·  November 2026", size=10.5,
    color=GRAY_LIGHT)

# ============================================== 2. the answer in one page
s = base_slide("Summary", "One scorecard, seven dimensions, four hard gates",
               "The pyramid, stated up front — then the evidence for each step.")
rows = [
    ("S", "Situation", "Ontologies are the schema layer of AI-ready data. The firm is already\n"
     "commissioning them across business and data teams.", TEAL),
    ("C", "Complication", "The benchmark we were handed measures LLMs, not ontologies — and the\n"
     "evaluation literature is mature but fragmented, with no deployable scorecard.", RED),
    ("P", "Proposal", "Adopt OQRS: a weighted, evidence-anchored scorecard with AI-readiness as a\n"
     "first-class dimension, hard gates, and validation before firm-wide rollout.", NAVY),
]
y = 2.02
for letter, label, body, col in rows:
    rect(s, M, y, SW - 2 * M, 1.16, fill=BG, line=RULE)
    rect(s, M, y, 0.06, 1.16, fill=col)
    txt(s, M + 0.28, y + 0.16, 0.5, 0.4, letter, size=22, bold=True, color=col)
    txt(s, M + 0.78, y + 0.16, 2.0, 0.3, label.upper(), size=10.5, bold=True,
        color=col)
    txt(s, M + 2.55, y + 0.16, SW - 2 * M - 2.8, 0.9, body, size=13.5,
        color=NAVY, spacing=1.2)
    y += 1.30
so_what(s, "Decision requested: approve Phase 0 — the dimension set, weights and gates.")
footer(s, 2)

# ============================================================ section S
section_slide(1, "S", "Why AI readiness depends on\nontology quality", "3 slides")

# S1 — why ontologies matter
s = base_slide("Situation", "AI readiness is a semantic problem before it is a model problem",
               "Four ways an ontology decides whether an AI system works — or only appears to.")
cards = [
    ("Grounding", "Retrieval, RAG and answer generation inherit whatever the concept layer "
     "says. Ambiguous classes produce confident, citable nonsense."),
    ("Interoperability", "Cross-domain integration only works when two systems mean the same "
     "thing by the same term — which requires a shared, formal definition."),
    ("Agentic use", "Tool selection and multi-step planning need machine-readable types, "
     "relations and constraints, not prose documentation."),
    ("Analytics", "Measures, entities and dimensions defined once and formally stop every "
     "report from re-inventing its own definition."),
]
for i, (h, b) in enumerate(cards):
    x = M + (i % 2) * ((SW - 2 * M) / 2 + 0.12)
    y = 2.02 + (i // 2) * 1.62
    card(s, x, y, (SW - 2 * M) / 2 - 0.06, 1.45, h, b)
so_what(s, "The ontology is the contract between the business and the AI system. "
        "When the contract is vague, the model is confidently wrong.")
footer(s, 3)

# S2 — the method exists
s = base_slide("Situation", "Twenty years of evaluation method already exists",
               "The literature converges on five families of evaluation — all of them implemented in free tools.")
fams = [
    ("Golden standard", "Precision / recall / F1 against a reference ontology", "D2 · D3"),
    ("Logical / formal", "Reasoners, OntoClean meta-properties, OOPS! pitfalls", "D1"),
    ("Structural / metrics", "OntoQA and OntoMetrics: richness, depth, cohesion", "D2 · D4"),
    ("Requirements", "Competency questions run as SPARQL tests; TDD for ontologies", "D3"),
    ("Quality models", "OQuaRE (ISO 25000) and FAIR scanners (FOOPS!, O'FAIRe)", "D5 · D6"),
]
for i, (h, b, d) in enumerate(fams):
    x = M + i * ((SW - 2 * M) / 5 + 0.02)
    rect(s, x, 2.02, (SW - 2 * M) / 5 - 0.12, 2.0, fill=BG, line=RULE)
    txt(s, x + 0.16, 2.20, (SW - 2 * M) / 5 - 0.44, 0.2, f"0{i+1}", size=10,
        bold=True, color=TEAL)
    txt(s, x + 0.16, 2.48, (SW - 2 * M) / 5 - 0.44, 0.7, h, size=13, bold=True,
        color=NAVY, spacing=1.0)
    txt(s, x + 0.16, 3.18, (SW - 2 * M) / 5 - 0.44, 0.66, b, size=10.5, color=GRAY,
        spacing=1.15)
    pill(s, x + 0.16, 3.62, 1.05, 0.26, d)
so_what(s, "The instruments exist and are free. What is missing is the synthesis — and a "
        "dimension for the AI-readiness question none of them answer.")
footer(s, 4)

# ============================================================ section C
section_slide(2, "C", "The benchmark we were handed\nmeasures the wrong object", "4 slides")

# C1 — what OntoURL is
s = base_slide("Complication", "OntoURL measures the model, not the ontology",
               "It is the first joint benchmark of LLM capability on ontological tasks — and that is a different question.")
# left panel: what it is
rect(s, M, 1.98, 6.05, 3.35, fill=BG, line=RULE)
txt(s, M + 0.24, 2.14, 5.6, 0.28, "WHAT ONTOURL IS", size=10.5, bold=True, color=TEAL)
txt(s, M + 0.24, 2.46, 5.6, 0.5, "URL Taxonomy — Understanding · Reasoning · Learning",
    size=13.5, bold=True, color=NAVY)
facts = [("15", "tasks across three capability families"),
         ("36,159", "benchmark instances"),
         ("43", "public ontologies, eight domains"),
         ("20", "open-source LLMs evaluated")]
fy = 2.98
for num, lab in facts:
    txt(s, M + 0.24, fy, 1.35, 0.34, num, size=17, bold=True, color=NAVY)
    txt(s, M + 1.62, fy + 0.06, 4.2, 0.34, lab, size=11.5, color=GRAY)
    fy += 0.56
# right panel: the shift
rect(s, M + 6.35, 1.98, SW - 2 * M - 6.35, 1.55, fill=AMBER_PALE, line=RULE)
txt(s, M + 6.59, 2.12, 5.2, 0.28, "WHAT ITS SCORES ARE A PROPERTY OF", size=10.5,
    bold=True, color=AMBER)
txt(s, M + 6.59, 2.44, 5.4, 0.9, "The model. The ontology is held fixed as an input;\nchange the model and every score moves.",
    size=13, color=NAVY, spacing=1.2)
rect(s, M + 6.35, 3.68, SW - 2 * M - 6.35, 1.65, fill=TEAL_PALE, line=RULE)
txt(s, M + 6.59, 3.82, 5.2, 0.28, "WHAT IT THEREFORE CANNOT TELL US", size=10.5,
    bold=True, color=TEAL)
txt(s, M + 6.59, 4.14, 5.4, 1.05, "Whether an ontology is well built — the question our\nmandate actually asks.",
    size=13, color=NAVY, spacing=1.2)
so_what(s, "We were pointed at a model leaderboard and asked to grade the artefact. "
        "Those are two different measurements.")
footer(s, 5)

# C2 — quote slide
s = base_slide("Complication", "The authors concede the gap in their own limitations section",
               "Two admissions from the OntoURL paper define the design brief for OQRS.")
rect(s, M, 1.98, 0.055, 2.2, fill=AMBER)
txt(s, M + 0.35, 1.98, SW - 2 * M - 0.7, 0.95,
    "“Our automatic metrics do not fully capture semantic adequacy, logical\n"
    "consistency, ontology-design quality, or downstream usefulness.”",
    size=20, italic=True, color=NAVY, spacing=1.18)
txt(s, M + 0.35, 3.02, 6.0, 0.3, "— OntoURL, limitations section [1]", size=11.5,
    color=GRAY)
rect(s, M, 4.42, 0.055, 1.55, fill=AMBER)
txt(s, M + 0.35, 4.42, SW - 2 * M - 0.7, 0.95,
    "“Should be interpreted as a benchmark of ontology-oriented behavior rather\n"
    "than a perfectly leakage-free test of unseen knowledge.”",
    size=20, italic=True, color=NAVY, spacing=1.18)
txt(s, M + 0.35, 5.42, 6.0, 0.3, "— OntoURL, limitations section [1]", size=11.5,
    color=GRAY)
so_what(s, "The first gap is the four things a quality scorecard must cover. The second is "
        "the evaluation-hygiene rule we build into D7.")
footer(s, 6)

# C3 — four complications
s = base_slide("Complication", "Four complications make “just adopt a benchmark” untenable",
               "Each one is a design constraint, not an argument against measuring.")
comps = [
    ("Metrics are gameable", "Class count and relationship richness rise trivially with padding. "
     "A large ontology is not a good one [14][15].", "→ pair metrics with semantic review and requirements tests"),
    ("Evaluation is unaddressed", "The LLM-era lifecycle literature clusters on conceptualisation and "
     "encoding: “no approaches cover ontology evaluation so far” [27].", "→ supply the missing artefact"),
    ("Public data leaks", "Public ontologies sit in training data, so scores on them are optimistic [1][30]. "
     "Internal ontologies are the better probe.", "→ hold the model fixed; prefer unseen ontologies"),
    ("Format sensitivity", "An unparsed answer is silently scored as wrong, so the score conflates "
     "ontology quality with output formatting [1].", "→ separate parse failures from wrong answers"),
]
for i, (h, b, fix) in enumerate(comps):
    x = M + (i % 2) * ((SW - 2 * M) / 2 + 0.12)
    y = 1.98 + (i // 2) * 1.95
    w = (SW - 2 * M) / 2 - 0.06
    rect(s, x, y, w, 1.78, fill=BG, line=RULE)
    rect(s, x, y, 0.05, 1.78, fill=RED)
    txt(s, x + 0.26, y + 0.16, w - 0.5, 0.4, h, size=14, bold=True, color=NAVY)
    txt(s, x + 0.26, y + 0.56, w - 0.5, 0.75, b, size=11.5, color=GRAY, spacing=1.15)
    txt(s, x + 0.26, y + 1.36, w - 0.5, 0.32, fix, size=10.5, bold=True, color=TEAL)
so_what(s, "None of these is fatal. All four are cheap to design around — if they are designed around.")
footer(s, 7)

# C4 — cost of status quo
s = base_slide("Complication", "The cost of staying undecided",
               "Without a scorecard, the decision moves to whoever reviews the ontology last.")
costs = [
    ("Pretty but useless\nreaches the AI tier", "An elegant, well-structured ontology that cannot answer "
     "the questions it was commissioned for gets certified by eye."),
    ("No comparability\nacross teams", "Two ontologies of the same type cannot be ranked, so build-versus-reuse "
     "and vendor decisions are made on anecdote."),
    ("Rework at the gate", "Defects surface at publication or, worse, in a downstream AI launch — when the "
     "cost of change is highest."),
]
for i, (h, b) in enumerate(costs):
    x = M + i * ((SW - 2 * M) / 3 + 0.08)
    w = (SW - 2 * M) / 3 - 0.12
    rect(s, x, 1.98, w, 2.55, fill=BG, line=RULE)
    txt(s, x + 0.22, 2.16, w - 0.44, 0.2, "COST 0%d" % (i + 1), size=10, bold=True,
        color=RED)
    txt(s, x + 0.22, 2.44, w - 0.44, 0.95, h, size=15, bold=True, color=NAVY, spacing=1.05)
    txt(s, x + 0.22, 3.42, w - 0.44, 1.0, b, size=11.5, color=GRAY, spacing=1.16)
rect(s, M, 4.75, SW - 2 * M, 1.15, fill=AMBER_PALE, line=RULE)
txt(s, M + 0.28, 4.92, SW - 2 * M - 0.56, 0.85,
    "The binding constraint is not effort — it is the absence of a shared definition of “good enough”.\n"
    "Today that definition varies by reviewer, by team and by week.",
    size=13, color=NAVY, spacing=1.2)
footer(s, 8)

# ============================================================ section P
section_slide(3, "P", "OQRS — one scorecard,\nseven dimensions, four gates", "7 slides")

# P1 — dimensions table
s = base_slide("Proposal", "Seven dimensions, weighted to the work that matters",
               "Weights are policy: set once, versioned, tuned per ontology type.")
rows = [
    ["#", "Dimension", "Weight", "Primary evidence", "Automation"],
    ["D1", "Logical & Formal Soundness", "18", "Reasoner, OOPS!, OntoClean", "High"],
    ["D2", "Semantic Content Quality", "15", "Coverage metrics + expert rubric", "Mixed"],
    ["D3", "Requirements Coverage / Fitness for Purpose", "16", "Competency-question test suite", "Mixed"],
    ["D4", "Structural & Architectural Quality", "12", "OntoQA / OntoMetrics", "High"],
    ["D5", "FAIR, Publication & Technical Quality", "12", "FOOPS!, O'FAIRe", "High"],
    ["D6", "Governance, Maintainability & Reuse", "12", "Metadata + expert review", "Low"],
    ["D7", "AI-Readiness & Machine Consumability", "15", "Downstream A/B + LLM probe", "Mixed"],
    ["", "Composite OQRS", "100", "", ""],
]
table(s, M, 1.98, [0.7, 4.5, 0.95, 3.55, 1.55], rows, row_h=0.44, head_h=0.42,
      size=11.5, aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER,
                         PP_ALIGN.LEFT, PP_ALIGN.CENTER], emphasis_last=True)
so_what(s, "Formal soundness and fitness for purpose carry the most weight — a pristine "
        "but useless ontology cannot score well.", y=6.22)
footer(s, 10)

# P2 — scoring and gates
s = base_slide("Proposal", "Score 0–4, then gate — some defects cannot be averaged away",
               "Each criterion is scored against written anchors; four conditions override the composite.")
# left: scale
txt(s, M, 1.98, 3.4, 0.28, "THE 0–4 ANCHOR SCALE", size=10.5, bold=True, color=TEAL)
scale = [("4", "Exemplary — meets or exceeds domain best practice"),
         ("3", "Substantial — sound, with minor gaps"),
         ("2", "Partial — present with material gaps"),
         ("1", "Minimal — present but a serious weakness"),
         ("0", "Absent, or not assessable")]
yy = 2.30
for n, d in scale:
    txt(s, M, yy, 0.4, 0.32, n, size=14, bold=True, color=TEAL)
    txt(s, M + 0.42, yy + 0.02, 3.2, 0.34, d, size=10.5, color=GRAY)
    yy += 0.42
txt(s, M, 4.60, 3.9, 0.75,
    "OQRS = 100 · Σd wd · (mean of normalised\ncriterion scores in dimension d)",
    size=11.5, color=NAVY, spacing=1.2)
# right: gates table
rows = [
    ["Gate", "Condition", "Effect"],
    ["G1 · Logical", "Inconsistent, or any unsatisfiable class", "FAIL at every level"],
    ["G2 · Pitfalls", "Any OOPS! pitfall graded critical", "Cap at L2"],
    ["G3 · Purpose", "D3 < 2/4", "AI-Ready withheld"],
    ["G4 · Publication", "D5 < 50%", "Cannot publish or reuse"],
]
table(s, M + 4.35, 1.98, [1.55, 3.35, 2.35], rows, row_h=0.56, head_h=0.4,
      size=10.5, aligns=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT])
txt(s, M + 4.35, 4.62, 7.4, 0.6,
    "Maturity: L1 Ad hoc <40 · L2 Developing 40–59 · L3 Defined 60–74 ·\nL4 Managed 75–89 · L5 Optimised ≥90",
    size=10.5, color=GRAY, spacing=1.2)
so_what(s, "Gates are what stop a structurally tidy, formally sound, and completely useless "
        "ontology from being certified.", y=5.62)
footer(s, 11)

# P3 — automation split
s = base_slide("Proposal", "Automate the objective; review the subjective",
               "The split is designed so a full pass costs about two hours of expert time per ontology.")
cols = [
    ("AUTOMATED", TEAL, "Runs on every commit",
     ["Consistency & satisfiability (HermiT, ELK, Pellet)",
      "Pitfall scanning (OOPS!, 41 pitfalls)",
      "Structural metrics (OntoQA, OntoMetrics)",
      "FAIR checks (FOOPS!, 24 checks)",
      "CQ test suite as SPARQL (Themis, SHACL)",
      "LLM legibility probe, model fixed"]),
    ("MIXED", AMBER, "Automated evidence, expert verdict",
     ["Subsumption correctness (OntoClean)",
      "Definition coverage → quality",
      "CQ pass rate → requirements breadth",
      "Grounding utility (downstream A/B)",
      "Verbalisation fidelity (BERTScore)"]),
    ("EXPERT", RED, "Written rubric, sampled review",
     ["Definition quality (genus–differentia)",
      "Lexical quality and naming",
      "Traceability and ORSD",
      "Governance and ownership",
      "Licence and IP clarity"]),
]
for i, (h, col, sub, items) in enumerate(cols):
    x = M + i * ((SW - 2 * M) / 3 + 0.12)
    w = (SW - 2 * M) / 3 - 0.16
    rect(s, x, 1.98, w, 3.75, fill=BG, line=RULE)
    rect(s, x, 1.98, w, 0.06, fill=col)
    txt(s, x + 0.22, 2.16, w - 0.44, 0.28, h, size=11, bold=True, color=col)
    txt(s, x + 0.22, 2.44, w - 0.44, 0.28, sub, size=10, italic=True, color=GRAY)
    by = 2.80
    for it in items:
        txt(s, x + 0.22, by, 0.16, 0.3, "·", size=12, bold=True, color=col)
        txt(s, x + 0.40, by, w - 0.62, 0.44, it, size=10.5, color=NAVY, spacing=1.12)
        by += 0.56 if len(it) < 48 else 0.62
so_what(s, "Nothing that needs judgement is scored by a tool; nothing that can be measured "
        "is left to judgement.", y=5.95)
footer(s, 12)

# P4 — lifecycle gates
s = base_slide("Proposal", "Four gates on the ontology lifecycle",
               "Mapped to LOT — the industrial framework teams already follow.")
gates = [
    ("G-A", "Requirements\nspecification", "Purpose gate",
     "Scope, non-functional requirements and a signed-off CQ set exist"),
    ("G-B", "Implementation", "Soundness gate",
     "Reasoner clean; no critical OOPS! pitfalls; CI lint green"),
    ("G-C", "Publication", "FAIR gate",
     "D5 ≥ 50%; resolvable URI, licence and documentation present"),
    ("G-D", "Maintenance", "Drift gate",
     "Scorecard re-run per release; no regression without a signed waiver"),
]
for i, (g, phase, gate, cond) in enumerate(gates):
    x = M + i * ((SW - 2 * M) / 4 + 0.08)
    w = (SW - 2 * M) / 4 - 0.12
    rect(s, x, 1.98, w, 2.6, fill=BG, line=RULE)
    txt(s, x + 0.2, 2.14, w - 0.4, 0.34, g, size=20, bold=True, color=TEAL)
    txt(s, x + 0.2, 2.56, w - 0.4, 0.62, phase, size=12.5, bold=True, color=NAVY,
        spacing=1.05)
    txt(s, x + 0.2, 3.20, w - 0.4, 0.28, gate.upper(), size=9.5, bold=True, color=AMBER)
    txt(s, x + 0.2, 3.48, w - 0.4, 0.95, cond, size=10.5, color=GRAY, spacing=1.14)
so_what(s, "The scorecard is not a report written after the fact — it is the gate condition "
        "at each lifecycle phase.")
footer(s, 13)

# P5 — worked example
s = base_slide("Proposal", "Worked example: IPRO scores 58.1 — L2, not AI-ready",
               "A mid-development internal reference ontology aligned to FIBO.")
rows = [
    ["Dimension", "Raw /4", "Norm.", "Weight", "Contrib."],
    ["D1 Logical & Formal", "2.8", "0.70", "18", "12.6"],
    ["D2 Semantic Content", "2.2", "0.55", "15", "8.3"],
    ["D3 Fitness for Purpose", "1.6", "0.40", "16", "6.4"],
    ["D4 Structural", "3.2", "0.80", "12", "9.6"],
    ["D5 FAIR", "3.0", "0.75", "12", "9.0"],
    ["D6 Governance", "1.8", "0.45", "12", "5.4"],
    ["D7 AI-Readiness", "1.8", "0.45", "15", "6.8"],
    ["Composite", "", "", "100", "58.1"],
]
table(s, M, 1.98, [2.75, 0.95, 0.95, 0.95, 1.0], rows, row_h=0.42, head_h=0.38,
      size=10.5, aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER,
                         PP_ALIGN.CENTER, PP_ALIGN.CENTER], emphasis_last=True)
# verdict panel
px = M + 7.35
rect(s, px, 1.98, SW - M - px, 3.55, fill=BG, line=RULE)
rect(s, px, 1.98, SW - M - px, 0.06, fill=RED)
txt(s, px + 0.26, 2.16, SW - M - px - 0.52, 0.28, "VERDICT", size=10.5, bold=True, color=RED)
txt(s, px + 0.26, 2.46, SW - M - px - 0.52, 0.9, "L2 Developing · G3 triggered\nNot AI-Ready certified",
    size=15, bold=True, color=NAVY, spacing=1.15)
txt(s, px + 0.26, 3.42, SW - M - px - 0.52, 0.28, "TOP THREE REMEDIATION ITEMS", size=9.5,
    bold=True, color=GRAY)
items = ["1. Complete the CQ set and wire it to SPARQL tests",
         "2. Lift definition coverage from ~40% to target",
         "3. Close two important OOPS! pitfalls"]
iy = 3.70
for it in items:
    txt(s, px + 0.26, iy, SW - M - px - 0.52, 0.42, it, size=10.5, color=NAVY, spacing=1.12)
    iy += 0.42
so_what(s, "Structurally tidy but not yet useful enough to certify — and the scorecard says so "
        "plainly, with the three things to fix.", y=5.75)
footer(s, 14)

# P6 — validation of the benchmark
s = base_slide("Proposal", "Validated before it is used to certify anything",
               "A benchmark that has not been evaluated is a liability. Four axes, mirroring the source literature.")
axes = [
    ("Content validity", "Every dimension and criterion traces to a cited framework [6][7][8][12][14][16][17][23]. Nothing invented."),
    ("Inter-rater reliability", "Two or three reviewers score a stratified sample independently; require Fleiss' κ ≥ 0.80 on expert criteria — the bar OntoURL met at 0.82–0.89 [1]."),
    ("Discrimination & sensitivity", "The composite must separate ontologies an expert would call good from those they would not, and must move when a defect is fixed."),
    ("Predictive validity", "The strongest test: does a higher score predict better downstream AI performance? If not, the weights are wrong and must be re-estimated."),
]
for i, (h, b) in enumerate(axes):
    x = M + (i % 2) * ((SW - 2 * M) / 2 + 0.12)
    y = 1.98 + (i // 2) * 1.72
    w = (SW - 2 * M) / 2 - 0.06
    rect(s, x, y, w, 1.55, fill=BG, line=RULE)
    txt(s, x + 0.24, y + 0.16, 0.32, 0.3, str(i + 1), size=15, bold=True, color=TEAL)
    txt(s, x + 0.62, y + 0.16, w - 0.86, 0.3, h, size=13.5, bold=True, color=NAVY)
    txt(s, x + 0.62, y + 0.52, w - 0.86, 0.92, b, size=10.5, color=GRAY, spacing=1.15)
so_what(s, "We do not roll out a scorecard we have not scored ourselves.")
footer(s, 15)

# P7 — roadmap
s = base_slide("Proposal", "Roadmap: fourteen weeks to a calibrated pipeline",
               "Five phases, each with a deliverable that can be signed off.")
phases = [
    ("0", "Align", "Weeks 1–2", "Ratify dimensions, weights and gates;\nconfirm ontology types"),
    ("1", "Instrument", "Weeks 3–6", "CI pipeline: ROBOT, reasoner, OOPS!,\nFOOPS!, metrics; scorecard JSON"),
    ("2", "Calibrate", "Weeks 7–10", "Pilot on 6–10 internal ontologies\n+ FIBO; κ study; rubric v1.0"),
    ("3", "Validate", "Weeks 11–14", "Predictive-validity study against\n≥1 downstream AI task"),
    ("4", "Operationalise", "Quarter 2", "Gates in the lifecycle; trained owners;\ncertification register"),
]
rect(s, M, 3.02, SW - 2 * M, 0.035, fill=RULE)
for i, (n, name, when, deliv) in enumerate(phases):
    x = M + i * ((SW - 2 * M) / 5 + 0.04)
    w = (SW - 2 * M) / 5 - 0.12
    rect(s, x, 2.94, 0.22, 0.22, fill=TEAL if i < 4 else AMBER, shape=MSO_SHAPE.OVAL)
    txt(s, x, 2.14, w, 0.28, when.upper(), size=9.5, bold=True, color=GRAY)
    txt(s, x, 2.42, w, 0.4, f"{n} · {name}", size=13.5, bold=True, color=NAVY)
    txt(s, x, 3.30, w, 1.3, deliv, size=10.5, color=GRAY, spacing=1.16)
so_what(s, "Six weeks gets us a calibrated pipeline on a real ontology; fourteen gets it validated.",
        y=5.35)
footer(s, 16)

# ============================================================ next step
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, SW, SH, fill=NAVY)
rect(s, 0, 0, 0.16, SH, fill=TEAL)
txt(s, M + 0.35, 1.02, 9.0, 0.28, "DECISION REQUESTED", size=11, bold=True, color=TEAL)
txt(s, M + 0.35, 1.40, 10.4, 1.3, "Approve Phase 0 and we will have\na calibrated scorecard in six weeks",
    size=30, bold=True, color=WHITE, spacing=1.06)
asks = [("Ratify", "the seven dimensions, their weights and the four gates."),
        ("Nominate", "6–10 internal ontologies — plus FIBO — for calibration."),
        ("Name", "the Ontology Review Board that arbitrates borderline cases and waivers.")]
ay = 3.30
for i, (verb, rest) in enumerate(asks):
    txt(s, M + 0.35, ay, 0.42, 0.4, str(i + 1), size=15, bold=True, color=TEAL)
    txt(s, M + 0.82, ay - 0.02, 10.2, 0.6, verb, size=13.5, bold=True, color=WHITE)
    txt(s, M + 2.55, ay - 0.02, 9.4, 0.6, rest, size=13, color=GRAY_LIGHT)
    ay += 0.78
rect(s, M + 0.35, 5.95, SW - 2 * M - 0.7, 0.012, fill=NAVY_LIGHT)
txt(s, M + 0.35, 6.12, 10.0, 0.3, "Full proposal: ontology-benchmark-proposal.md  ·  Reference summaries: references-summary.md",
    size=10, color=GRAY_LIGHT)

out = Path("./out")
out.mkdir(exist_ok=True)
path = out / "oqrs-scp-deck.pptx"
prs.save(str(path))
print(f"saved {path} ({len(prs.slides.__iter__.__self__._sldIdLst)} slides)")
