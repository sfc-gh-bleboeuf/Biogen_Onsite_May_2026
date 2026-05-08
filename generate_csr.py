"""
generate_csr.py
Generates a realistic mock Clinical Study Report (CSR) PDF for
Biogen × Snowflake Document AI demo — May 13, 2026 onsite.

Output: STUDY-2024-001_CSR_Final.pdf
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import ListFlowable, ListItem
import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "STUDY-2024-001_CSR_Final.pdf")

# ── Brand Colors ──────────────────────────────────────────────
BIOGEN_NAVY   = colors.HexColor("#1B2B4B")
BIOGEN_TEAL   = colors.HexColor("#00A0AF")
SF_BLUE       = colors.HexColor("#29B5E8")
LIGHT_GRAY    = colors.HexColor("#F5F5F5")
MID_GRAY      = colors.HexColor("#CCCCCC")
DARK_GRAY     = colors.HexColor("#555555")
RED_ALERT     = colors.HexColor("#C0392B")
AMBER         = colors.HexColor("#E67E22")
GREEN_OK      = colors.HexColor("#27AE60")

# ── Style Setup ───────────────────────────────────────────────
styles = getSampleStyleSheet()

def style(name, parent="Normal", **kwargs):
    return ParagraphStyle(name, parent=styles[parent], **kwargs)

title_style = style("CsrTitle", parent="Title",
    fontSize=22, textColor=BIOGEN_NAVY, spaceAfter=6,
    alignment=TA_CENTER, fontName="Helvetica-Bold")

subtitle_style = style("CsrSubtitle",
    fontSize=13, textColor=BIOGEN_TEAL, spaceAfter=4,
    alignment=TA_CENTER, fontName="Helvetica-Bold")

conf_style = style("Confidential",
    fontSize=9, textColor=RED_ALERT, alignment=TA_CENTER,
    fontName="Helvetica-Bold", spaceAfter=2)

h1_style = style("H1",
    fontSize=14, textColor=BIOGEN_NAVY, spaceBefore=18, spaceAfter=6,
    fontName="Helvetica-Bold", borderPad=4)

h2_style = style("H2",
    fontSize=11, textColor=BIOGEN_TEAL, spaceBefore=12, spaceAfter=4,
    fontName="Helvetica-Bold")

h3_style = style("H3",
    fontSize=10, textColor=BIOGEN_NAVY, spaceBefore=8, spaceAfter=3,
    fontName="Helvetica-Bold")

body_style = style("Body",
    fontSize=9.5, textColor=colors.black, spaceBefore=4, spaceAfter=4,
    leading=14, alignment=TA_JUSTIFY)

small_style = style("Small",
    fontSize=8.5, textColor=DARK_GRAY, spaceBefore=2, spaceAfter=2,
    leading=12)

footer_style = style("Footer",
    fontSize=7.5, textColor=DARK_GRAY, alignment=TA_CENTER)

label_style = style("Label",
    fontSize=8.5, textColor=BIOGEN_NAVY, fontName="Helvetica-Bold")

mono_style = style("Mono",
    fontSize=8.5, fontName="Courier", textColor=DARK_GRAY,
    spaceBefore=2, spaceAfter=2, leading=12)

# ── Page Header/Footer ───────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    w, h = letter
    # Header bar
    canvas.setFillColor(BIOGEN_NAVY)
    canvas.rect(0, h - 0.55*inch, w, 0.55*inch, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(0.4*inch, h - 0.35*inch, "BIOGEN INC.")
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(w/2, h - 0.35*inch,
        "CLINICAL STUDY REPORT — STUDY-2024-001  |  CONFIDENTIAL")
    canvas.drawRightString(w - 0.4*inch, h - 0.35*inch, "Final Version 1.0")
    # Teal accent line
    canvas.setFillColor(BIOGEN_TEAL)
    canvas.rect(0, h - 0.58*inch, w, 0.04*inch, fill=1, stroke=0)
    # Footer
    canvas.setFillColor(LIGHT_GRAY)
    canvas.rect(0, 0, w, 0.45*inch, fill=1, stroke=0)
    canvas.setFillColor(MID_GRAY)
    canvas.rect(0, 0.43*inch, w, 0.015*inch, fill=1, stroke=0)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(DARK_GRAY)
    canvas.drawString(0.4*inch, 0.18*inch,
        "Biogen Inc. | 225 Binney Street, Cambridge MA 02142  |  Confidential and Proprietary")
    canvas.drawCentredString(w/2, 0.18*inch, f"Page {doc.page}")
    canvas.drawRightString(w - 0.4*inch, 0.18*inch,
        "ICH E3 Clinical Study Report Format")
    canvas.restoreState()

def title_page(canvas, doc):
    """First page has no running header."""
    canvas.saveState()
    w, h = letter
    # Footer only
    canvas.setFillColor(LIGHT_GRAY)
    canvas.rect(0, 0, w, 0.45*inch, fill=1, stroke=0)
    canvas.setFillColor(MID_GRAY)
    canvas.rect(0, 0.43*inch, w, 0.015*inch, fill=1, stroke=0)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(DARK_GRAY)
    canvas.drawString(0.4*inch, 0.18*inch,
        "Biogen Inc. | 225 Binney Street, Cambridge MA 02142  |  Confidential and Proprietary")
    canvas.drawCentredString(w/2, 0.18*inch, "Page 1")
    canvas.drawRightString(w - 0.4*inch, 0.18*inch, "ICH E3 Clinical Study Report Format")
    canvas.restoreState()


def hr():
    return HRFlowable(width="100%", thickness=1, color=MID_GRAY, spaceAfter=8, spaceBefore=4)

def teal_hr():
    return HRFlowable(width="100%", thickness=2, color=BIOGEN_TEAL, spaceAfter=6, spaceBefore=2)

def section_header(text):
    return [teal_hr(), Paragraph(text, h1_style), Spacer(1, 4)]

def table_style_base(header_rows=1):
    return TableStyle([
        ("BACKGROUND",   (0,0), (-1, header_rows-1), BIOGEN_NAVY),
        ("TEXTCOLOR",    (0,0), (-1, header_rows-1), colors.white),
        ("FONTNAME",     (0,0), (-1, header_rows-1), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 8.5),
        ("ROWBACKGROUNDS",(0, header_rows), (-1,-1), [colors.white, LIGHT_GRAY]),
        ("GRID",         (0,0), (-1,-1), 0.4, MID_GRAY),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING",   (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ("ALIGN",        (0,0), (-1, header_rows-1), "CENTER"),
    ])


# ── Build Document ───────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.8*inch, bottomMargin=0.65*inch,
        title="Clinical Study Report — STUDY-2024-001",
        author="Biogen Clinical Development",
        subject="Phase 2a Randomized Controlled Trial — Drug A in Relapsing MS",
    )

    story = []

    # ── TITLE PAGE ──────────────────────────────────────────
    story += [
        Spacer(1, 0.6*inch),
        Paragraph("BIOGEN INC.", subtitle_style),
        Spacer(1, 0.1*inch),
        Paragraph("CLINICAL STUDY REPORT", title_style),
        Spacer(1, 0.15*inch),
        HRFlowable(width=3*inch, thickness=3, color=BIOGEN_TEAL,
                   spaceAfter=16, spaceBefore=4, hAlign="CENTER"),
        Paragraph("Study Number: STUDY-2024-001", style("TitleMeta",
            fontSize=12, alignment=TA_CENTER, textColor=BIOGEN_NAVY,
            fontName="Helvetica-Bold")),
        Spacer(1, 0.1*inch),
        Paragraph(
            "A Phase 2a, Randomized, Double-Blind, Placebo-Controlled,<br/>"
            "Dose-Ranging Study of Drug A (BIO-4421) in Adult Patients<br/>"
            "with Relapsing Multiple Sclerosis",
            style("TitleLong", fontSize=13, alignment=TA_CENTER,
                  textColor=DARK_GRAY, leading=20)),
        Spacer(1, 0.5*inch),
    ]

    meta = [
        ["IND Number:", "IND 123456"],
        ["EudraCT Number:", "2023-001234-56"],
        ["Protocol Version:", "v3.0, dated 15 Nov 2023"],
        ["Report Version:", "Final v1.0"],
        ["Report Date:", "14 April 2026"],
        ["Sponsor:", "Biogen Inc., 225 Binney Street, Cambridge MA 02142"],
        ["Coordinating Investigator:", "Prof. Annette Weber, MD PhD — Charité Berlin"],
        ["CRO:", "PharmaLink Clinical Research (Global)"],
        ["Regulatory Authority:", "FDA (IND) / EMA (CTA)"],
    ]
    meta_tbl = Table([[Paragraph(k, label_style), Paragraph(v, body_style)]
                       for k,v in meta],
                     colWidths=[2.0*inch, 4.5*inch])
    meta_tbl.setStyle(TableStyle([
        ("GRID",          (0,0),(-1,-1), 0.4, MID_GRAY),
        ("ROWBACKGROUNDS",(0,0),(-1,-1), [colors.white, LIGHT_GRAY]),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
    ]))
    story += [meta_tbl, Spacer(1, 0.4*inch)]

    story += [
        Paragraph("CONFIDENTIAL AND PROPRIETARY", conf_style),
        Paragraph(
            "This document contains confidential information belonging to Biogen Inc. "
            "It is intended solely for use by the individuals or entities to whom it is "
            "addressed. Any review, use, disclosure, or distribution by others is strictly "
            "prohibited without prior written consent of Biogen Inc.",
            style("ConfBody", fontSize=8, textColor=DARK_GRAY, alignment=TA_CENTER,
                  leading=12)),
        PageBreak(),
    ]

    # ── TABLE OF CONTENTS ───────────────────────────────────
    story += section_header("Table of Contents")
    toc_entries = [
        ("1", "Synopsis", "3"),
        ("2", "Introduction and Study Rationale", "4"),
        ("3", "Study Objectives", "4"),
        ("4", "Investigational Plan (Study Design)", "5"),
        ("5", "Study Population", "6"),
        ("6", "Efficacy Results", "7"),
        ("7", "Safety Results", "9"),
        ("8", "Protocol Deviations", "13"),
        ("9", "Discussion and Conclusions", "14"),
        ("10", "References", "15"),
        ("Appendix A", "Listing of Serious Adverse Events", "16"),
        ("Appendix B", "Laboratory Values — Markedly Abnormal", "16"),
    ]
    for sec, title, pg in toc_entries:
        story.append(Paragraph(
            f'<b>{sec}</b> &nbsp;&nbsp; {title} '
            f'<font color="#AAAAAA">{"." * max(1, 60 - len(sec) - len(title))}</font> {pg}',
            style("TOC", fontSize=9.5, textColor=DARK_GRAY, spaceBefore=3, spaceAfter=3)))
    story.append(PageBreak())

    # ── SECTION 1: SYNOPSIS ──────────────────────────────────
    story += section_header("1. Synopsis")

    synopsis_data = [
        ["Title", "A Phase 2a Randomized Double-Blind Placebo-Controlled Dose-Ranging Study of Drug A (BIO-4421) in Adult Patients with Relapsing Multiple Sclerosis"],
        ["Protocol Number", "STUDY-2024-001 v3.0"],
        ["Phase", "Phase 2a"],
        ["Study Design", "Randomized, double-blind, placebo-controlled, parallel-group, 3-arm, dose-ranging"],
        ["Duration", "12 weeks treatment + 4 weeks safety follow-up"],
        ["Primary Endpoint", "Change from baseline in annualized relapse rate (ARR) at Week 12"],
        ["Key Secondary Endpoint", "Change from baseline in T2 lesion volume on brain MRI at Week 12"],
        ["Population", "Adult patients (18–75 years) with relapsing MS, EDSS 0–5.5, ≥1 relapse in prior 12 months"],
        ["Treatment Arms", "Placebo (n=30) | Drug A 10 mg QD (n=30) | Drug A 20 mg QD (n=30)"],
        ["Primary Efficacy Result",
         "Drug A 20 mg demonstrated a statistically significant 52.3% reduction in ARR vs placebo "
         "(ARR: 0.41 vs 0.86; RR=0.477; 95% CI 0.312–0.729; p=0.0008). Drug A 10 mg showed a "
         "non-significant 28.4% reduction (ARR: 0.62; p=0.0921)."],
        ["Key Safety Finding",
         "Drug A 20 mg was associated with increased incidence of hepatic enzyme elevations: "
         "ALT >3× ULN observed in 3/30 subjects (10%) vs 0/30 placebo. One subject discontinued "
         "due to ALT >8× ULN (SAE). No cases of Hy's Law criteria met. LFT monitoring protocol "
         "amendment implemented."],
        ["Conclusion",
         "Drug A 20 mg QD demonstrated clinically meaningful and statistically significant reduction "
         "in relapse rate with an acceptable benefit-risk profile. Hepatic monitoring protocol "
         "strengthened. Data support advancement to Phase 2b dose-confirmation study."],
        ["Report Date", "14 April 2026"],
        ["Sponsor Medical Responsible", "Dr. Sarah Chen, MD, VP Clinical Development Neurology"],
    ]
    syn_tbl = Table([[Paragraph(k, label_style), Paragraph(v, small_style)]
                     for k,v in synopsis_data],
                    colWidths=[1.8*inch, 4.7*inch])
    syn_tbl.setStyle(TableStyle([
        ("GRID",          (0,0),(-1,-1), 0.4, MID_GRAY),
        ("ROWBACKGROUNDS",(0,0),(-1,-1), [colors.white, LIGHT_GRAY]),
        ("LEFTPADDING",   (0,0),(-1,-1), 6),
        ("RIGHTPADDING",  (0,0),(-1,-1), 6),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("BACKGROUND",    (0,7),(1,7), colors.HexColor("#FFF3E0")),  # primary endpoint row
        ("BACKGROUND",    (0,8),(1,8), colors.HexColor("#E8F8F0")),  # safety row
    ]))
    story += [syn_tbl, PageBreak()]

    # ── SECTION 2: INTRODUCTION ──────────────────────────────
    story += section_header("2. Introduction and Study Rationale")
    story.append(Paragraph(
        "Multiple sclerosis (MS) is a chronic, inflammatory, demyelinating disease of the central "
        "nervous system affecting approximately 2.9 million individuals worldwide. Relapsing forms "
        "of MS, including relapsing-remitting MS (RRMS), account for roughly 85% of initial "
        "diagnoses and are characterized by discrete episodes of neurological dysfunction followed "
        "by partial or complete recovery.",
        body_style))
    story.append(Paragraph(
        "Despite the availability of approved disease-modifying therapies (DMTs), a significant "
        "proportion of patients experience inadequate disease control, tolerability issues, or "
        "safety concerns necessitating treatment switches. There remains a substantial unmet need "
        "for therapies that combine meaningful efficacy with a favorable safety profile.",
        body_style))
    story.append(Paragraph(
        "Drug A (BIO-4421) is a selective oral sphingosine-1-phosphate receptor 1 (S1P1) modulator "
        "with enhanced receptor subtype selectivity compared to first-generation agents. Preclinical "
        "studies demonstrated potent lymphocyte sequestration with reduced off-target effects on "
        "cardiac S1P3 receptors. Phase 1 studies confirmed favorable pharmacokinetics with once-daily "
        "oral dosing and no clinically significant cardiac adverse effects at doses up to 40 mg.",
        body_style))

    # ── SECTION 3: OBJECTIVES ────────────────────────────────
    story += section_header("3. Study Objectives")
    story.append(Paragraph("<b>Primary Objective</b>", h3_style))
    story.append(Paragraph(
        "To evaluate the efficacy of Drug A 10 mg and 20 mg once daily versus placebo on annualized "
        "relapse rate (ARR) in adult patients with relapsing multiple sclerosis over 12 weeks of treatment.",
        body_style))
    story.append(Paragraph("<b>Secondary Objectives</b>", h3_style))
    secondary_obj = [
        "To assess the effect of Drug A on new or enlarging T2 lesion volume on brain MRI at Week 12.",
        "To evaluate the effect of Drug A on Expanded Disability Status Scale (EDSS) score change from baseline.",
        "To characterize the safety and tolerability of Drug A in the study population.",
        "To evaluate pharmacokinetic parameters of Drug A at steady state (Week 4 and Week 12).",
    ]
    for obj in secondary_obj:
        story.append(Paragraph(f"• {obj}", style("Bullet", parent="Normal",
            fontSize=9.5, leftIndent=16, spaceBefore=2, spaceAfter=2, leading=14)))
    story.append(PageBreak())

    # ── SECTION 4: STUDY DESIGN ──────────────────────────────
    story += section_header("4. Investigational Plan — Study Design")
    story.append(Paragraph(
        "This was a multicenter, randomized, double-blind, placebo-controlled, parallel-group, "
        "dose-ranging Phase 2a study conducted at 12 investigational sites in the United States, "
        "Germany, and the Netherlands.",
        body_style))
    story.append(Paragraph("<b>Study Schema</b>", h3_style))

    schema_data = [
        ["Period", "Duration", "Activities"],
        ["Screening", "Up to 28 days", "Eligibility assessment, baseline MRI, laboratory tests, informed consent"],
        ["Randomization (Day 1)", "1 day", "1:1:1 allocation to Placebo / Drug A 10mg / Drug A 20mg (IVRS)"],
        ["Treatment Period", "12 weeks (84 days)", "Study drug QD dosing; clinic visits at Weeks 2, 4, 8, 12"],
        ["Safety Follow-Up", "4 weeks (28 days)", "Post-treatment safety assessments; LFT monitoring"],
        ["Final Visit / EOS", "Week 16", "End-of-study assessments, final MRI, pharmacokinetics"],
    ]
    schema_tbl = Table(schema_data,
        colWidths=[1.3*inch, 1.3*inch, 3.9*inch])
    schema_tbl.setStyle(table_style_base())
    story += [schema_tbl, Spacer(1, 10)]
    story.append(Paragraph(
        "<b>Randomization and Blinding:</b> Subjects were randomized in a 1:1:1 ratio using "
        "permuted block randomization stratified by site and baseline EDSS score (≤2.5 vs >2.5). "
        "The study was double-blind; subjects, investigators, and the sponsor study team were "
        "blinded to treatment assignment throughout the treatment period.",
        body_style))

    # ── SECTION 5: STUDY POPULATION ─────────────────────────
    story += section_header("5. Study Population")
    story.append(Paragraph("<b>Disposition of Subjects</b>", h3_style))
    disp_data = [
        ["", "Placebo\n(n=30)", "Drug A 10 mg\n(n=30)", "Drug A 20 mg\n(n=30)", "Total\n(N=90)"],
        ["Randomized", "30", "30", "30", "90"],
        ["Completed treatment", "29 (96.7%)", "28 (93.3%)", "26 (86.7%)", "83 (92.2%)"],
        ["Discontinued", "1 (3.3%)", "2 (6.7%)", "4 (13.3%)", "7 (7.8%)"],
        ["  — Adverse event", "0", "1", "2", "3"],
        ["  — Withdrawal by subject", "1", "1", "1", "3"],
        ["  — Lost to follow-up", "0", "0", "1", "1"],
        ["Completed follow-up", "29 (96.7%)", "27 (90.0%)", "25 (83.3%)", "81 (90.0%)"],
    ]
    disp_tbl = Table(disp_data, colWidths=[2.1*inch, 1.1*inch, 1.1*inch, 1.1*inch, 1.1*inch])
    disp_tbl.setStyle(table_style_base())
    story += [disp_tbl, Spacer(1, 10)]

    story.append(Paragraph("<b>Baseline Demographics and Characteristics</b>", h3_style))
    demo_data = [
        ["Characteristic", "Placebo\n(n=30)", "Drug A 10 mg\n(n=30)", "Drug A 20 mg\n(n=30)"],
        ["Age, mean (SD), years", "48.2 (10.4)", "46.8 (11.2)", "49.1 (9.8)"],
        ["Female, n (%)", "19 (63.3%)", "18 (60.0%)", "20 (66.7%)"],
        ["Disease duration, mean (SD), years", "8.4 (5.2)", "7.9 (4.8)", "8.7 (5.5)"],
        ["Baseline EDSS, median (range)", "2.5 (0–5.5)", "2.5 (0–5.0)", "3.0 (0–5.5)"],
        ["ARR in prior 12 months, mean (SD)", "1.8 (0.9)", "1.7 (0.8)", "1.9 (1.0)"],
        ["Prior DMT use, n (%)", "18 (60.0%)", "17 (56.7%)", "19 (63.3%)"],
        ["Baseline T2 lesion volume (mL), mean", "11.2 (8.4)", "10.8 (7.9)", "12.1 (9.3)"],
    ]
    demo_tbl = Table(demo_data, colWidths=[2.5*inch, 1.3*inch, 1.3*inch, 1.3*inch])
    demo_tbl.setStyle(table_style_base())
    story += [demo_tbl, PageBreak()]

    # ── SECTION 6: EFFICACY ──────────────────────────────────
    story += section_header("6. Efficacy Results")
    story.append(Paragraph("<b>6.1 Primary Endpoint: Annualized Relapse Rate</b>", h2_style))
    story.append(Paragraph(
        "The primary efficacy endpoint was the annualized relapse rate (ARR) at Week 12. "
        "A relapse was defined as new or worsening neurological symptoms lasting ≥24 hours, "
        "accompanied by an objective change in neurological examination, in the absence of fever "
        "or infection.",
        body_style))

    eff_data = [
        ["Parameter", "Placebo\n(n=29)", "Drug A 10 mg\n(n=28)", "Drug A 20 mg\n(n=26)"],
        ["ARR, estimated mean (95% CI)", "0.86 (0.62–1.18)", "0.62 (0.43–0.89)", "0.41 (0.27–0.62)"],
        ["Rate Ratio vs Placebo (95% CI)", "Reference", "0.716 (0.483–1.062)", "0.477 (0.312–0.729)"],
        ["% Reduction vs Placebo", "—", "28.4%", "52.3%"],
        ["p-value (vs Placebo)", "—", "0.0921", "0.0008*"],
        ["Subjects relapse-free, n (%)", "17 (58.6%)", "20 (71.4%)", "22 (84.6%)"],
    ]
    eff_tbl = Table(eff_data, colWidths=[2.5*inch, 1.3*inch, 1.3*inch, 1.3*inch])
    s = table_style_base()
    s.add("BACKGROUND", (3,2), (3,2), colors.HexColor("#E8F5E9"))
    s.add("BACKGROUND", (3,4), (3,4), colors.HexColor("#E8F5E9"))
    s.add("TEXTCOLOR",  (3,4), (3,4), GREEN_OK)
    s.add("FONTNAME",   (3,4), (3,4), "Helvetica-Bold")
    eff_tbl.setStyle(s)
    story += [eff_tbl, Spacer(1, 6)]
    story.append(Paragraph(
        "* Statistically significant at pre-specified α=0.05. Analysis performed using negative "
        "binomial regression model with log-time on study as offset, treatment arm as factor, "
        "and baseline ARR + EDSS stratum as covariates.",
        style("Footnote", fontSize=8, textColor=DARK_GRAY, spaceBefore=2)))

    story.append(Paragraph("<b>6.2 Secondary Endpoints</b>", h2_style))
    sec_eff_data = [
        ["Endpoint", "Placebo", "Drug A 10 mg", "Drug A 20 mg", "p-value\n(20 mg vs PBO)"],
        ["Change in T2 lesion vol (mL), mean", "+1.8", "+0.4", "−1.2", "0.0124*"],
        ["New/enlarging T2 lesions, median", "2.0", "1.0", "0.0", "0.0031*"],
        ["EDSS change from baseline, mean", "+0.14", "+0.07", "+0.03", "0.3812"],
        ["9-HPT change (seconds), mean", "+0.4", "−0.3", "−0.6", "0.2144"],
        ["MSIS-29 total score change, mean", "−1.2", "−3.4", "−5.8", "0.0412*"],
    ]
    sec_tbl = Table(sec_eff_data, colWidths=[2.3*inch, 1.1*inch, 1.1*inch, 1.1*inch, 0.9*inch])
    sec_tbl.setStyle(table_style_base())
    story += [sec_tbl, Spacer(1, 6)]
    story.append(Paragraph(
        "* Statistically significant. MSIS-29: Multiple Sclerosis Impact Scale-29. "
        "9-HPT: Nine-Hole Peg Test. MRI endpoints analyzed by central blinded reading center.",
        style("Footnote", fontSize=8, textColor=DARK_GRAY, spaceBefore=2)))
    story.append(PageBreak())

    # ── SECTION 7: SAFETY ────────────────────────────────────
    story += section_header("7. Safety Results")
    story.append(Paragraph(
        "Safety was evaluated in all subjects who received at least one dose of study medication "
        "(Safety Population, N=90). Adverse events were coded using MedDRA Version 27.0.",
        body_style))

    story.append(Paragraph("<b>7.1 Overview of Adverse Events</b>", h2_style))
    ae_overview = [
        ["Safety Parameter", "Placebo\n(n=30)", "Drug A 10 mg\n(n=30)", "Drug A 20 mg\n(n=30)"],
        ["Any TEAE, n (%)", "18 (60.0%)", "22 (73.3%)", "25 (83.3%)"],
        ["TEAEs related to study drug", "7 (23.3%)", "14 (46.7%)", "18 (60.0%)"],
        ["TEAE Grade ≥3", "1 (3.3%)", "2 (6.7%)", "5 (16.7%)"],
        ["Serious AE (SAE)", "0 (0.0%)", "1 (3.3%)", "3 (10.0%)"],
        ["AE leading to discontinuation", "0 (0.0%)", "1 (3.3%)", "2 (6.7%)"],
        ["AE leading to death", "0", "0", "0"],
    ]
    ae_tbl = Table(ae_overview, colWidths=[2.5*inch, 1.3*inch, 1.3*inch, 1.3*inch])
    s2 = table_style_base()
    s2.add("BACKGROUND", (3,4), (3,4), colors.HexColor("#FFF3E0"))
    s2.add("BACKGROUND", (3,5), (3,5), colors.HexColor("#FFF3E0"))
    ae_tbl.setStyle(s2)
    story += [ae_tbl, Spacer(1, 8)]

    story.append(Paragraph("<b>7.2 TEAEs by System Organ Class and Preferred Term (≥5% in any arm)</b>", h2_style))
    soc_data = [
        ["System Organ Class / Preferred Term", "Placebo\nn=30\nn(%)", "Drug A 10mg\nn=30\nn(%)", "Drug A 20mg\nn=30\nn(%)"],
        ["GASTROINTESTINAL DISORDERS", "", "", ""],
        ["  Nausea", "1 (3.3%)", "4 (13.3%)", "6 (20.0%)"],
        ["  Diarrhoea", "1 (3.3%)", "2 (6.7%)", "3 (10.0%)"],
        ["  Vomiting", "0", "1 (3.3%)", "2 (6.7%)"],
        ["NERVOUS SYSTEM DISORDERS", "", "", ""],
        ["  Headache", "4 (13.3%)", "5 (16.7%)", "6 (20.0%)"],
        ["  Dizziness", "1 (3.3%)", "3 (10.0%)", "4 (13.3%)"],
        ["  Fatigue", "2 (6.7%)", "5 (16.7%)", "7 (23.3%)"],
        ["INVESTIGATIONS", "", "", ""],
        ["  ALT increased", "0 (0.0%)", "1 (3.3%)", "4 (13.3%)"],
        ["  AST increased", "0 (0.0%)", "1 (3.3%)", "3 (10.0%)"],
        ["  GGT increased", "0 (0.0%)", "0 (0.0%)", "2 (6.7%)"],
        ["VASCULAR DISORDERS", "", "", ""],
        ["  Hypertension", "1 (3.3%)", "1 (3.3%)", "2 (6.7%)"],
        ["RESPIRATORY DISORDERS", "", "", ""],
        ["  Dyspnoea", "0 (0.0%)", "0 (0.0%)", "2 (6.7%)"],
        ["SKIN DISORDERS", "", "", ""],
        ["  Rash", "1 (3.3%)", "1 (3.3%)", "1 (3.3%)"],
    ]
    soc_tbl = Table(soc_data, colWidths=[2.9*inch, 1.2*inch, 1.1*inch, 1.1*inch])
    s3 = table_style_base()
    for i in [1,5,9,13,15,17]:
        if i < len(soc_data):
            s3.add("BACKGROUND",  (0,i),(-1,i), colors.HexColor("#EBF5FB"))
            s3.add("FONTNAME",    (0,i),(-1,i), "Helvetica-Bold")
            s3.add("TEXTCOLOR",   (0,i),(-1,i), BIOGEN_NAVY)
    # Highlight hepatic AEs
    s3.add("TEXTCOLOR", (3,11),(3,13), RED_ALERT)
    s3.add("FONTNAME",  (3,11),(3,13), "Helvetica-Bold")
    soc_tbl.setStyle(s3)
    story += [soc_tbl, PageBreak()]

    story.append(Paragraph("<b>7.3 Hepatic Safety — Liver Enzyme Elevations</b>", h2_style))
    story.append(Paragraph(
        "Hepatic enzyme elevations represented the most clinically significant safety finding "
        "observed with Drug A 20 mg and prompted a protocol amendment (v3.0) to strengthen "
        "liver function monitoring.",
        body_style))

    hep_data = [
        ["ALT Elevation", "Placebo\n(n=30)", "Drug A 10 mg\n(n=30)", "Drug A 20 mg\n(n=30)"],
        ["Any ALT elevation above ULN", "2 (6.7%)", "3 (10.0%)", "8 (26.7%)"],
        ["ALT >1× to ≤3× ULN", "2 (6.7%)", "2 (6.7%)", "4 (13.3%)"],
        ["ALT >3× to ≤5× ULN", "0 (0.0%)", "1 (3.3%)", "1 (3.3%)"],
        ["ALT >5× to ≤10× ULN", "0 (0.0%)", "0 (0.0%)", "2 (6.7%)"],
        ["ALT >10× ULN", "0 (0.0%)", "0 (0.0%)", "1 (3.3%)"],
        ["ALT >3× ULN + Bili >2× ULN (Hy's Law)", "0 (0.0%)", "0 (0.0%)", "0 (0.0%)"],
    ]
    hep_tbl = Table(hep_data, colWidths=[2.5*inch, 1.3*inch, 1.3*inch, 1.3*inch])
    s4 = table_style_base()
    s4.add("TEXTCOLOR",  (3,5),(3,5), RED_ALERT)
    s4.add("FONTNAME",   (3,5),(3,5), "Helvetica-Bold")
    s4.add("BACKGROUND", (3,5),(3,5), colors.HexColor("#FDEDEC"))
    s4.add("TEXTCOLOR",  (3,6),(3,6), GREEN_OK)
    s4.add("FONTNAME",   (3,6),(3,6), "Helvetica-Bold")
    s4.add("BACKGROUND", (3,6),(3,6), colors.HexColor("#E8F8F0"))
    hep_tbl.setStyle(s4)
    story += [hep_tbl, Spacer(1, 8)]

    story.append(Paragraph(
        "<b>Subject STUDY-001-001-003 (SAE narrative):</b> A 61-year-old male randomized to "
        "Drug A 20 mg presented with asymptomatic ALT elevation to 412 U/L (8.2× ULN) at the "
        "Week 8 visit. The subject had no symptoms of hepatitis. Study drug was immediately "
        "interrupted. The subject was hospitalized for observation and further hepatological "
        "evaluation. Viral hepatitis serology was negative. Liver biopsy was not performed. "
        "ALT declined to 2.1× ULN by Day 70. The event was reported as a serious adverse event "
        "and assessed as related to study drug. The subject was withdrawn from the study. "
        "No cases meeting Hy's Law criteria (ALT or AST >3× ULN plus total bilirubin >2× ULN) "
        "were observed in this study.",
        style("Narrative", fontSize=9, textColor=DARK_GRAY, leftIndent=12, rightIndent=12,
              spaceBefore=6, spaceAfter=6, leading=13,
              borderPad=8, borderColor=AMBER, borderWidth=1, backColor=colors.HexColor("#FFFDE7"))),
    )

    story.append(Paragraph("<b>7.4 Serious Adverse Events</b>", h2_style))
    sae_data = [
        ["Subject ID", "Age/Sex", "Arm", "SAE Term", "Severity", "Relationship", "Outcome"],
        ["STUDY-001-001-003", "61/M", "Drug A 20mg", "ALT increased", "Grade 3", "Related", "Recovering"],
        ["STUDY-001-002-003", "68/F", "Drug A 20mg", "Hypertension", "Grade 3", "Possible", "Recovering"],
        ["STUDY-001-003-003", "72/M", "Drug A 20mg", "Dyspnoea", "Grade 2", "Related", "Recovering"],
        ["STUDY-001-002-002", "43/M", "Drug A 10mg", "MS relapse requiring hospitalisation", "Grade 3", "Not Related", "Recovered"],
    ]
    sae_tbl = Table(sae_data,
        colWidths=[1.3*inch, 0.65*inch, 0.85*inch, 1.4*inch, 0.65*inch, 0.7*inch, 0.7*inch])
    s5 = table_style_base()
    for row in [1,2,3]:
        s5.add("TEXTCOLOR", (2,row),(2,row), RED_ALERT)
    sae_tbl.setStyle(s5)
    story += [sae_tbl, PageBreak()]

    # ── SECTION 8: PROTOCOL DEVIATIONS ───────────────────────
    story += section_header("8. Protocol Deviations")
    story.append(Paragraph(
        "A total of 12 protocol deviations were documented across the study. Four were classified "
        "as major deviations per the protocol deviation management plan.",
        body_style))
    dev_data = [
        ["Subject", "Site", "Deviation Category", "Description", "Major?"],
        ["STUDY-001-001-002", "SITE-001", "Dosing/Administration", "Study drug taken with food on Day 25 (fasting required)", "No"],
        ["STUDY-001-002-003", "SITE-002", "Prohibited Medication", "Self-initiated ibuprofen (NSAID) for 3 days; not disclosed until Week 10 visit", "Yes"],
        ["STUDY-001-003-001", "SITE-003", "Informed Consent", "Re-consent for amendment v2.0 obtained 3 days outside required window", "No"],
        ["STUDY-001-003-003", "SITE-003", "Visit Window", "Week 12 visit ±7 day window exceeded by 4 days; PK sample not collected", "Yes"],
    ]
    dev_tbl = Table(dev_data, colWidths=[1.2*inch, 0.7*inch, 1.2*inch, 2.8*inch, 0.55*inch])
    s6 = table_style_base()
    s6.add("TEXTCOLOR", (4,2),(4,5), RED_ALERT)
    dev_tbl.setStyle(s6)
    story += [dev_tbl, Spacer(1, 10)]
    story.append(PageBreak())

    # ── SECTION 9: CONCLUSIONS ───────────────────────────────
    story += section_header("9. Discussion and Conclusions")
    story.append(Paragraph("<b>Summary of Findings</b>", h2_style))
    story.append(Paragraph(
        "This Phase 2a study met its primary endpoint, demonstrating that Drug A 20 mg once daily "
        "produced a statistically significant and clinically meaningful 52.3% reduction in "
        "annualized relapse rate compared to placebo (p=0.0008). This magnitude of ARR reduction "
        "is consistent with that observed for approved S1P modulators and supports the mechanism "
        "of action of Drug A.",
        body_style))
    story.append(Paragraph(
        "The 10 mg dose showed a numerically lower ARR (28.4% reduction) that did not reach "
        "statistical significance (p=0.0921), suggesting the 10 mg dose may be sub-therapeutic "
        "in the majority of patients, though some patients may respond adequately.",
        body_style))
    story.append(Paragraph(
        "Key secondary endpoints supported the primary finding: Drug A 20 mg demonstrated "
        "significant reductions in new/enlarging T2 lesion count (p=0.0031) and T2 lesion volume "
        "(p=0.0124), as well as improvement in patient-reported outcomes (MSIS-29, p=0.0412).",
        body_style))
    story.append(Paragraph("<b>Safety Assessment</b>", h2_style))
    story.append(Paragraph(
        "The safety profile of Drug A was generally consistent with the S1P modulator class. "
        "The most notable safety concern is hepatic enzyme elevation, particularly in the 20 mg arm. "
        "Although no cases met Hy's Law criteria, the occurrence of one subject with ALT >8× ULN "
        "requiring hospitalization and study discontinuation warrants careful hepatic monitoring "
        "in future studies. The protocol has been amended to include mandatory LFT monitoring at "
        "Weeks 1, 2, 4, 8, and 12, with pre-specified stopping rules.",
        body_style))
    story.append(Paragraph("<b>Conclusion and Recommendation</b>", h2_style))
    story.append(Paragraph(
        "Based on the totality of evidence from STUDY-2024-001, Drug A 20 mg once daily "
        "demonstrated a compelling efficacy profile in relapsing MS with an acceptable benefit-risk "
        "balance. These data support the advancement of Drug A 20 mg (with enhanced hepatic "
        "monitoring) into a Phase 2b, larger-scale, dose-confirmation study. Consideration should "
        "also be given to biomarker-driven patient stratification to identify subjects at elevated "
        "hepatic risk prior to enrollment.",
        body_style))
    story.append(Spacer(1, 0.3*inch))

    sig_data = [
        ["Prepared by:", "Dr. Marcus Holloway, MD\nClinical Program Lead, Neurology\nBiogen Inc.", "Date: 14 April 2026"],
        ["Medical Review:", "Dr. Sarah Chen, MD\nVP Clinical Development, Neurology\nBiogen Inc.", "Date: 14 April 2026"],
        ["Biostatistics:", "Dr. Lin Wei, PhD\nDirector, Biostatistics\nBiogen Inc.", "Date: 12 April 2026"],
    ]
    sig_tbl = Table([[Paragraph(k, label_style), Paragraph(v, small_style),
                      Paragraph(d, small_style)] for k,v,d in sig_data],
                    colWidths=[1.2*inch, 3.8*inch, 1.5*inch])
    sig_tbl.setStyle(TableStyle([
        ("GRID",         (0,0),(-1,-1), 0.5, MID_GRAY),
        ("ROWBACKGROUNDS",(0,0),(-1,-1), [colors.white, LIGHT_GRAY]),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("TOPPADDING",   (0,0),(-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
    ]))
    story += [sig_tbl, PageBreak()]

    # ── SECTION 10: REFERENCES ───────────────────────────────
    story += section_header("10. References")
    refs = [
        "1. Thompson AJ et al. Diagnosis of multiple sclerosis: 2017 revisions of the McDonald criteria. Lancet Neurol. 2018;17(2):162–173.",
        "2. Kappos L et al. Siponimod versus placebo in secondary progressive MS. Lancet. 2018;391(10127):1263–1273.",
        "3. Lublin FD et al. Defining the clinical course of multiple sclerosis. Neurology. 2014;83(3):278–286.",
        "4. ICH E3: Structure and Content of Clinical Study Reports. International Council for Harmonisation. 1995.",
        "5. FDA Guidance: Drug-Induced Liver Injury: Premarketing Clinical Evaluation. 2009.",
        "6. Polman CH et al. Diagnostic criteria for multiple sclerosis: 2010 revisions to the McDonald criteria. Ann Neurol. 2011;69(2):292–302.",
    ]
    for ref in refs:
        story.append(Paragraph(ref, style("Ref", fontSize=9, textColor=DARK_GRAY,
            leftIndent=16, firstLineIndent=-16, spaceBefore=4, spaceAfter=4, leading=13)))

    story.append(Spacer(1, 0.3*inch))
    story.append(HRFlowable(width="100%", thickness=1, color=MID_GRAY))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(
        "End of Clinical Study Report — STUDY-2024-001 — Final Version 1.0 — 14 April 2026<br/>"
        "© 2026 Biogen Inc. All rights reserved. Confidential and Proprietary.",
        style("EndDoc", fontSize=8, textColor=DARK_GRAY, alignment=TA_CENTER)))

    # ── BUILD ────────────────────────────────────────────────
    doc.build(
        story,
        onFirstPage=title_page,
        onLaterPages=on_page,
    )
    print(f"CSR PDF written to: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    build()
