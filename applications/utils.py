from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from django.http import HttpResponse
from io import BytesIO
import datetime


def generate_application_pdf(application):
    """Generate a comprehensive PDF for an application with lead-quality-based content"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles with TrikonED branding
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#ff9900'),  # Primary color
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#01764e'),  # Secondary color
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#181510'),
        spaceAfter=12,
        spaceBefore=16,
        fontName='Helvetica-Bold'
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 10
    normal_style.leading = 14
    
    # Header with TrikonED branding
    elements.append(Paragraph("TrikonED", title_style))
    elements.append(Paragraph("University Application Form", subtitle_style))
    
    # Application Type Header
    app_type_text = f"<b>{application.get_application_type_display()} Application</b>"
    elements.append(Paragraph(app_type_text, ParagraphStyle(
        'AppType',
        parent=normal_style,
        fontSize=12,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#01764e')
    )))
    elements.append(Spacer(1, 12))
    
    # Lead Quality Badge
    lead_colors = {
        'high': colors.HexColor('#10B981'),  # Green
        'medium': colors.HexColor('#F59E0B'),  # Orange
        'low': colors.HexColor('#EF4444'),  # Red
    }
    lead_color = lead_colors.get(application.lead_quality, colors.grey)
    
    lead_badge = Table([[f"Lead Quality: {application.get_lead_quality_display()}"]], colWidths=[6*inch])
    lead_badge.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), lead_color),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('ROUNDEDCORNERS', [5, 5, 5, 5]),
    ]))
    elements.append(lead_badge)
    elements.append(Spacer(1, 16))
    
    # Application ID and Status
    app_info_data = [
        ['Application ID:', f"#{application.application_id}"],
        ['Status:', application.get_status_display()],
        ['Submitted On:', application.applied_on.strftime('%B %d, %Y')],
    ]
    
    app_info_table = Table(app_info_data, colWidths=[2*inch, 4*inch])
    app_info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#181510')),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(app_info_table)
    elements.append(Spacer(1, 20))
    
    # Student Information Section
    elements.append(Paragraph("STUDENT INFORMATION", heading_style))
    
    student = application.student
    student_data = [
        ['Full Name', f"{student.first_name} {student.last_name}"],
        ['Email', student.email],
        ['Phone', student.phone or 'N/A'],
        ['Date of Birth', student.date_of_birth.strftime('%B %d, %Y') if student.date_of_birth else 'N/A'],
        ['Gender', student.get_gender_display() if student.gender else 'N/A'],
        ['Nationality', student.nationality or 'N/A'],
        ['Address', student.address or 'N/A'],
        ['Passport Number', student.passport_number or 'N/A'],
        ['Passport Expiry', student.passport_expiry.strftime('%B %d, %Y') if student.passport_expiry else 'N/A'],
    ]
    
    student_table = Table(student_data, colWidths=[2*inch, 4*inch])
    student_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f7f5')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#181510')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e7e2da')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(student_table)
    elements.append(Spacer(1, 20))
    
    # Program Information Section
    elements.append(Paragraph("PROGRAM INFORMATION", heading_style))
    program_data = [
        ['University', application.university.name],
        ['Location', application.university.get_location_display()],
        ['Program', application.program.name],
        ['Program Type', application.program.type.name],
        ['Program Level', application.program.type.level.name],
        ['Delivery Type', application.program.get_delivery_type_display()],
        ['Duration', f"{application.program.type.duration} {application.program.type.get_duration_unit_display()}"],
        ['Application Type', application.get_application_type_display()],
    ]
    
    # Add tuition fee if available
    if application.program.tuition_fees.exists():
        fee = application.program.tuition_fees.first()
        fee_text = f"{fee.currency} {fee.amount:,.0f}"
        if fee.max_amount:
            fee_text += f" - {fee.max_amount:,.0f}"
        fee_text += f" ({fee.get_per_display()})"
        program_data.append(['Tuition Fee', fee_text])
    
    program_table = Table(program_data, colWidths=[2*inch, 4*inch])
    program_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f7f5')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#181510')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e7e2da')),
    ]))
    elements.append(program_table)
    elements.append(Spacer(1, 20))
    
    # Lead-Quality-Based Content
    # HIGH LEAD: Show all information
    if application.lead_quality == 'high':
        # Documents Section
        elements.append(Paragraph("DOCUMENTS SUBMITTED", heading_style))
        documents = student.documents.all()
        if documents:
            doc_data = [['Document Type', 'File Name', 'Uploaded On']]
            for document in documents:
                doc_data.append([
                    document.get_doc_type_display(),
                    document.file_name[:40] + '...' if len(document.file_name) > 40 else document.file_name,
                    document.uploaded_at.strftime('%B %d, %Y')
                ])
            
            doc_table = Table(doc_data, colWidths=[2*inch, 2.5*inch, 1.5*inch])
            doc_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff9900')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e7e2da')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
            ]))
            elements.append(doc_table)
        else:
            elements.append(Paragraph("<i>No documents uploaded.</i>", normal_style))
        elements.append(Spacer(1, 20))
        
        # English Test Scores
        test_scores = student.test_scores.all()
        if test_scores:
            elements.append(Paragraph("ENGLISH PROFICIENCY TEST SCORES", heading_style))
            score_data = [['Test Type', 'Overall Score', 'Test Date', 'Expiry Date']]
            for score in test_scores:
                score_data.append([
                    score.test_type,
                    str(score.overall_score) if score.overall_score else 'N/A',
                    score.test_date.strftime('%B %d, %Y') if score.test_date else 'N/A',
                    score.expiry_date.strftime('%B %d, %Y') if score.expiry_date else 'N/A'
                ])
            
            score_table = Table(score_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            score_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff9900')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e7e2da')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
            ]))
            elements.append(score_table)
            elements.append(Spacer(1, 20))
    
    # MEDIUM LEAD: Show partial information
    elif application.lead_quality == 'medium':
        elements.append(Paragraph("DOCUMENTS & TEST SCORES", heading_style))
        
        # Show document count
        doc_count = student.documents.count()
        score_count = student.test_scores.count()
        
        info_text = f"<b>Documents Submitted:</b> {doc_count}<br/>"
        info_text += f"<b>Test Scores Submitted:</b> {score_count}<br/>"
        info_text += "<i>Note: Some information is incomplete. Please contact the student for additional details.</i>"
        
        elements.append(Paragraph(info_text, normal_style))
        elements.append(Spacer(1, 20))
    
    # LOW LEAD: Minimal information
    else:  # low lead
        elements.append(Paragraph("ADDITIONAL INFORMATION", heading_style))
        warning_text = "<b>⚠ Incomplete Application</b><br/>"
        warning_text += "<i>This is a low-quality lead. The student has not submitted required documents or test scores. "
        warning_text += "Follow up with the student to complete their application.</i>"
        
        warning_para = Paragraph(warning_text, ParagraphStyle(
            'Warning',
            parent=normal_style,
            textColor=colors.HexColor('#EF4444'),
            backColor=colors.HexColor('#FEE2E2'),
            borderPadding=10,
            borderWidth=1,
            borderColor=colors.HexColor('#EF4444'),
        ))
        elements.append(warning_para)
        elements.append(Spacer(1, 20))
    
    # Application Timeline (for all leads)
    elements.append(Paragraph("APPLICATION TIMELINE", heading_style))
    logs = application.logs.all().order_by('timestamp')
    if logs:
        timeline_data = [['Date & Time', 'Event', 'Details']]
        for log in logs:
            timeline_data.append([
                log.timestamp.strftime('%b %d, %Y %H:%M'),
                log.event,
                log.details[:50] + '...' if len(log.details) > 50 else log.details
            ])
        
        timeline_table = Table(timeline_data, colWidths=[1.5*inch, 2*inch, 2.5*inch])
        timeline_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff9900')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e7e2da')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ]))
        elements.append(timeline_table)
    else:
        elements.append(Paragraph("<i>No timeline events recorded.</i>", normal_style))
    
    # Remarks
    if application.remarks:
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("STUDENT REMARKS", heading_style))
        elements.append(Paragraph(application.remarks, normal_style))
    
    # Consent Information
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("CONSENT & TERMS", heading_style))
    
    consent_text = f"<b>Data Sharing Consent:</b> {'✓ Granted' if application.consent_given else '✗ Not Granted'}<br/>"
    if application.consent_given:
        consent_text += "<i>The student has agreed that TrikonED may store their details and share their profile with selected colleges and universities for the purpose of admissions, scholarships, and counselling.</i>"
    else:
        consent_text += "<i>The student has not provided consent for data sharing.</i>"
    
    consent_para = Paragraph(consent_text, ParagraphStyle(
        'Consent',
        parent=normal_style,
        backColor=colors.HexColor('#FFF8E1') if application.consent_given else colors.HexColor('#FEE2E2'),
        borderPadding=10,
        borderWidth=1,
        borderColor=colors.HexColor('#ff9900') if application.consent_given else colors.HexColor('#EF4444'),
    ))
    elements.append(consent_para)
    
    # Footer
    elements.append(Spacer(1, 30))
    footer_text = f"<i>Generated on {datetime.datetime.now().strftime('%B %d, %Y at %H:%M')}</i><br/>"
    footer_text += "<i>© TrikonED - Your Global University Application Platform</i>"
    elements.append(Paragraph(footer_text, ParagraphStyle(
        'Footer',
        parent=normal_style,
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )))
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and return it
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
