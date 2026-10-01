"""
PDF Report Generation Service for AGRI-MITRA
Uses ReportLab to produce high-quality agricultural advisory reports.
"""

from io import BytesIO
from typing import Optional
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

from models.database_models import User, CropPrediction, FertilizerPrediction


def _get_styles():
    styles = getSampleStyleSheet()
    
    # Custom palette
    primary_color = colors.HexColor('#1b4332')    # Deep Forest Green
    secondary_color = colors.HexColor('#2d6a4f')  # Emerald Green
    accent_color = colors.HexColor('#40916c')     # Soft Leaf Green
    dark_text = colors.HexColor('#1f2937')        # Slate Dark

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        alignment=0,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#52b788'),
        spaceAfter=15
    )

    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=secondary_color,
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=dark_text
    )

    highlight_style = ParagraphStyle(
        'HighlightBox',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#081c15'),
        alignment=1
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=dark_text
    )

    return {
        'title': title_style,
        'subtitle': subtitle_style,
        'section': section_style,
        'body': body_style,
        'highlight': highlight_style,
        'th': table_header_style,
        'td': table_cell_style,
        'primary': primary_color,
        'secondary': secondary_color,
        'accent': accent_color
    }


def generate_crop_report_pdf(prediction: CropPrediction, user: Optional[User] = None) -> bytes:
    """Generates an official Crop Prediction Report as PDF bytes."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    st = _get_styles()
    story = []

    # Title & Branding Banner
    story.append(Paragraph("AGRI-MITRA | Precision Agriculture Advisory", st['subtitle']))
    story.append(Paragraph("Official Crop Prediction Report", st['title']))
    story.append(HRFlowable(width="100%", thickness=2, color=st['primary'], spaceAfter=15))

    # Metadata Block
    user_name = user.full_name if user else (prediction.user.full_name if prediction.user else 'Valued Farmer')
    user_email = user.email if user else (prediction.user.email if prediction.user else 'N/A')
    user_loc = getattr(user, 'location', 'Regional Farming Zone') or 'Regional Farming Zone'
    date_str = prediction.created_at.strftime('%B %d, %Y - %I:%M %p') if prediction.created_at else datetime.utcnow().strftime('%B %d, %Y')

    meta_data = [
        [
            Paragraph("<b>Report ID:</b>", st['td']),
            Paragraph(f"CP-{prediction.id:06d}", st['td']),
            Paragraph("<b>Generated On:</b>", st['td']),
            Paragraph(date_str, st['td'])
        ],
        [
            Paragraph("<b>Farmer / User:</b>", st['td']),
            Paragraph(user_name, st['td']),
            Paragraph("<b>Email:</b>", st['td']),
            Paragraph(user_email, st['td'])
        ],
        [
            Paragraph("<b>Location:</b>", st['td']),
            Paragraph(user_loc, st['td']),
            Paragraph("<b>System:</b>", st['td']),
            Paragraph("AGRI-MITRA AI Core (RandomForest)", st['td'])
        ]
    ]

    t_meta = Table(meta_data, colWidths=[90, 160, 90, 175])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 15))

    # Primary Highlight: Predicted Crop
    story.append(Paragraph("Recommended Optimal Crop", st['section']))
    pred_crop_title = prediction.predicted_crop.title()
    crop_banner_data = [[
        Paragraph(f"OPTIMAL CROP: <font color='#2d6a4f'>{pred_crop_title.upper()}</font>", st['highlight'])
    ]]
    t_crop_banner = Table(crop_banner_data, colWidths=[515])
    t_crop_banner.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#d8f3dc')),
        ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#52b788')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_crop_banner)
    story.append(Spacer(1, 15))

    # Environmental & Soil Diagnostics Table
    story.append(Paragraph("Soil & Environmental Input Diagnostics", st['section']))
    param_data = [
        [Paragraph("Parameter", st['th']), Paragraph("Tested Value", st['th']), Paragraph("Standard Reference Range", st['th'])],
        [Paragraph("Nitrogen (N)", st['td']), Paragraph(f"{prediction.N} kg/ha", st['td']), Paragraph("0 - 140 kg/ha", st['td'])],
        [Paragraph("Phosphorus (P)", st['td']), Paragraph(f"{prediction.P} kg/ha", st['td']), Paragraph("5 - 145 kg/ha", st['td'])],
        [Paragraph("Potassium (K)", st['td']), Paragraph(f"{prediction.K} kg/ha", st['td']), Paragraph("5 - 205 kg/ha", st['td'])],
        [Paragraph("Temperature", st['td']), Paragraph(f"{prediction.temperature} °C", st['td']), Paragraph("10 - 45 °C", st['td'])],
        [Paragraph("Relative Humidity", st['td']), Paragraph(f"{prediction.humidity} %", st['td']), Paragraph("15 - 100 %", st['td'])],
        [Paragraph("Soil pH", st['td']), Paragraph(f"{prediction.ph}", st['td']), Paragraph("3.5 - 9.5 (Neutral 6.0-7.5)", st['td'])],
        [Paragraph("Rainfall", st['td']), Paragraph(f"{prediction.rainfall} mm", st['td']), Paragraph("20 - 300 mm", st['td'])],
    ]
    t_params = Table(param_data, colWidths=[160, 160, 195])
    t_params.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), st['primary']),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_params)
    story.append(Spacer(1, 15))

    # Basic Fertilizer Suggestion
    story.append(Paragraph("Baseline Agronomic Fertilizer Advisory", st['section']))
    fert_text = prediction.fertilizer_suggestion or "Follow balanced NPK schedule in accordance with local soil health card guidelines."
    story.append(Paragraph(fert_text, st['body']))
    story.append(Spacer(1, 10))

    # Farm Management Notes
    story.append(Paragraph("Field Best Practices", st['section']))
    notes = (
        f"1. <b>Land Preparation:</b> Ensure field leveling and deep ploughing before sowing {pred_crop_title}.<br/>"
        "2. <b>Water Management:</b> Maintain optimal moisture during critical vegetative stages; avoid waterlogging.<br/>"
        "3. <b>Integrated Pest Management:</b> Scout regularly for early pest and disease symptoms; use bio-pesticides when feasible."
    )
    story.append(Paragraph(notes, st['body']))
    story.append(Spacer(1, 20))

    # Footer note
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#9ca3af'), spaceAfter=8))
    footer_text = "AGRI-MITRA Smart Agriculture Platform | Confidential & Certified AI Advisory | Powered by Google Antigravity & Scikit-Learn"
    story.append(Paragraph(footer_text, ParagraphStyle('Foot', parent=st['body'], fontSize=8, textColor=colors.HexColor('#6b7280'), alignment=1)))

    doc.build(story)
    return buffer.getvalue()


def generate_fertilizer_report_pdf(prediction: FertilizerPrediction, user: Optional[User] = None) -> bytes:
    """Generates an official Fertilizer Recommendation Report as PDF bytes."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    st = _get_styles()
    story = []

    # Title & Header
    story.append(Paragraph("AGRI-MITRA | Precision Agriculture Advisory", st['subtitle']))
    story.append(Paragraph("Fertilizer Recommendation Diagnostic Report", st['title']))
    story.append(HRFlowable(width="100%", thickness=2, color=st['primary'], spaceAfter=15))

    # Metadata Block
    user_name = user.full_name if user else (prediction.user.full_name if prediction.user else 'Valued Farmer')
    user_email = user.email if user else (prediction.user.email if prediction.user else 'N/A')
    user_loc = getattr(user, 'location', 'Regional Farming Zone') or 'Regional Farming Zone'
    date_str = prediction.created_at.strftime('%B %d, %Y - %I:%M %p') if prediction.created_at else datetime.utcnow().strftime('%B %d, %Y')

    meta_data = [
        [
            Paragraph("<b>Report ID:</b>", st['td']),
            Paragraph(f"FR-{prediction.id:06d}", st['td']),
            Paragraph("<b>Generated On:</b>", st['td']),
            Paragraph(date_str, st['td'])
        ],
        [
            Paragraph("<b>Farmer / User:</b>", st['td']),
            Paragraph(user_name, st['td']),
            Paragraph("<b>Email:</b>", st['td']),
            Paragraph(user_email, st['td'])
        ],
        [
            Paragraph("<b>Target Crop:</b>", st['td']),
            Paragraph(prediction.crop_type or 'General Crop', st['td']),
            Paragraph("<b>Soil Type:</b>", st['td']),
            Paragraph(prediction.soil_type or 'Standard Loam', st['td'])
        ]
    ]

    t_meta = Table(meta_data, colWidths=[90, 160, 90, 175])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 15))

    # Highlight: Recommended Fertilizer
    story.append(Paragraph("Prescribed Fertilizer Recommendation", st['section']))
    fert_name = prediction.recommended_fertilizer
    fert_banner_data = [[
        Paragraph(f"RECOMMENDED FERTILIZER: <font color='#1b4332'>{fert_name}</font>", st['highlight'])
    ]]
    t_fert_banner = Table(fert_banner_data, colWidths=[515])
    t_fert_banner.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e0f2fe')),
        ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#0284c7')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_fert_banner)
    story.append(Spacer(1, 15))

    # Soil Diagnostics
    story.append(Paragraph("Soil Analysis Parameters", st['section']))
    param_data = [
        [Paragraph("Parameter", st['th']), Paragraph("Field Measurement", st['th']), Paragraph("Typical Soil Status", st['th'])],
        [Paragraph("Nitrogen (N)", st['td']), Paragraph(f"{prediction.N} kg/ha", st['td']), Paragraph("Vegetative growth promoter", st['td'])],
        [Paragraph("Phosphorus (P)", st['td']), Paragraph(f"{prediction.P} kg/ha", st['td']), Paragraph("Root development promoter", st['td'])],
        [Paragraph("Potassium (K)", st['td']), Paragraph(f"{prediction.K} kg/ha", st['td']), Paragraph("Stress resilience & grain filling", st['td'])],
        [Paragraph("Soil Moisture", st['td']), Paragraph(f"{prediction.moisture} %", st['td']), Paragraph("Available water capacity", st['td'])],
        [Paragraph("Temperature", st['td']), Paragraph(f"{prediction.temperature} °C", st['td']), Paragraph("Root nutrient uptake range", st['td'])],
        [Paragraph("Humidity", st['td']), Paragraph(f"{prediction.humidity} %", st['td']), Paragraph("Evapotranspiration factor", st['td'])],
    ]
    t_params = Table(param_data, colWidths=[160, 160, 195])
    t_params.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0369a1')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f9ff')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_params)
    story.append(Spacer(1, 15))

    # Agronomic Rationale (WHY)
    story.append(Paragraph("Agronomic Rationale & Scientific Justification (WHY)", st['section']))
    why_text = prediction.explanation or f"{fert_name} provides targeted macro-nutrients aligned with your soil test results."
    story.append(Paragraph(why_text, st['body']))
    story.append(Spacer(1, 10))

    # Application Best Practices
    story.append(Paragraph("Application & Soil Health Guidelines", st['section']))
    guide_text = (
        "1. <b>Timing:</b> Apply fertilizers during early morning or late afternoon when soil moisture is adequate.<br/>"
        "2. <b>Placement:</b> Place fertilizer 5 cm below seed depth; avoid direct contact with seed embryo.<br/>"
        "3. <b>Split Application:</b> Split nitrogenous fertilizers into multiple doses to reduce leaching losses."
    )
    story.append(Paragraph(guide_text, st['body']))
    story.append(Spacer(1, 20))

    # Footer note
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#9ca3af'), spaceAfter=8))
    footer_text = "AGRI-MITRA Smart Agriculture Platform | Confidential & Certified AI Advisory | Powered by Google Antigravity & Scikit-Learn"
    story.append(Paragraph(footer_text, ParagraphStyle('Foot', parent=st['body'], fontSize=8, textColor=colors.HexColor('#6b7280'), alignment=1)))

    doc.build(story)
    return buffer.getvalue()
