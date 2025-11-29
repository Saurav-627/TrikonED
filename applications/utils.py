from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from django.http import HttpResponse
from io import BytesIO
import datetime


def generate_application_pdf(application):
    """Generate a comprehensive PDF for an application"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#d4a574'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#181510'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    normal_style = styles['Normal']
    
    # Title
    elements.append(Paragraph("APPLICATION FORM", title_style))
    elements.append(Spacer(1, 12))
    
    # Application ID and Status
    app_info = f"<b>Application ID:</b> #{application.application_id} | <b>Status:</b> {application.get_status_display()}"
    elements.append(Paragraph(app_info, normal_style))
    elements.append(Paragraph(f"<b>Submitted On:</b> {application.applied_on.strftime('%B %d, %Y')}", normal_style))
    elements.append(Spacer(1, 20))
    
    # Student Information
    elements.append(Paragraph("STUDENT INFORMATION", heading_style))
    student_data = [
        ['Full Name', f"{application.student.first_name} {application.student.last_name}"],
        ['Email', application.student.email],
        ['Phone', application.student.phone or 'N/A'],
        ['Date of Birth', application.student.date_of_birth.strftime('%B %d, %Y') if application.student.date_of_birth else 'N/A'],
        ['Gender', application.student.get_gender_display() if application.student.gender else 'N/A'],
        ['Nationality', application.student.nationality or 'N/A'],
        ['Passport Number', application.student.passport_number or 'N/A'],
        ['Passport Expiry', application.student.passport_expiry.strftime('%B %d, %Y') if application.student.passport_expiry else 'N/A'],
    ]
    
    student_table = Table(student_data, colWidths=[2*inch, 4*inch])
    student_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(student_table)
    elements.append(Spacer(1, 20))
    
    # Program Information
    elements.append(Paragraph("PROGRAM INFORMATION", heading_style))
    program_data = [
        ['University', application.university.name],
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
        fee_text = f"{fee.currency} {fee.amount}"
        if fee.max_amount:
            fee_text += f" - {fee.max_amount}"
        fee_text += f" ({fee.get_per_display()})"
        program_data.append(['Tuition Fee', fee_text])
    
    program_table = Table(program_data, colWidths=[2*inch, 4*inch])
    program_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(program_table)
    elements.append(Spacer(1, 20))
    
    # Documents Submitted
    elements.append(Paragraph("DOCUMENTS SUBMITTED", heading_style))
    documents = application.student.documents.all()
    if documents:
        doc_data = [['Document Type', 'File Name', 'Uploaded On']]
        for doc in documents:
            doc_data.append([
                doc.get_doc_type_display(),
                doc.file_name,
                doc.uploaded_at.strftime('%B %d, %Y')
            ])
        
        doc_table = Table(doc_data, colWidths=[2*inch, 2.5*inch, 1.5*inch])
        doc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d4a574')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ]))
        elements.append(doc_table)
    else:
        elements.append(Paragraph("No documents uploaded.", normal_style))
    
    elements.append(Spacer(1, 20))
    
    # Application Timeline
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
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d4a574')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ]))
        elements.append(timeline_table)
    
    # Remarks
    if application.remarks:
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("REMARKS", heading_style))
        elements.append(Paragraph(application.remarks, normal_style))
    
    # Footer
    elements.append(Spacer(1, 30))
    footer_text = f"<i>Generated on {datetime.datetime.now().strftime('%B %d, %Y at %H:%M')}</i>"
    elements.append(Paragraph(footer_text, ParagraphStyle('Footer', parent=normal_style, fontSize=8, textColor=colors.grey, alignment=TA_CENTER)))
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and return it
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
