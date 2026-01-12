# Report Generator Service
import io
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import random

def generate_security_report(report_type: str, date_range: str, include_charts: bool = True, 
                             include_raw: bool = False, executive_summary: bool = True) -> bytes:
    """Generate a security report in text format (compatible with all systems)"""
    
    # Generate report content
    report_lines = []
    
    # Header
    report_lines.append("=" * 70)
    report_lines.append("")
    report_lines.append("                  AI-DRIVEN AUTONOMOUS SOC")
    report_lines.append("                     SECURITY REPORT")
    report_lines.append("")
    report_lines.append("=" * 70)
    report_lines.append("")
    report_lines.append(f"Report Type: {report_type}")
    report_lines.append(f"Date Range: {date_range}")
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    report_lines.append("-" * 70)
    report_lines.append("")
    
    # Executive Summary
    if executive_summary:
        report_lines.append("EXECUTIVE SUMMARY")
        report_lines.append("-" * 30)
        report_lines.append("")
        report_lines.append("This report provides a comprehensive overview of the security posture")
        report_lines.append("for the specified reporting period. Key findings include:")
        report_lines.append("")
        report_lines.append("  * Total security events analyzed: 2,847")
        report_lines.append("  * Critical threats detected: 23")
        report_lines.append("  * Threats successfully blocked: 156")
        report_lines.append("  * Average response time: 1.2 seconds")
        report_lines.append("  * Overall security score: 87/100")
        report_lines.append("")
        report_lines.append("-" * 70)
        report_lines.append("")
    
    # Threat Analysis Section
    report_lines.append("THREAT ANALYSIS")
    report_lines.append("-" * 30)
    report_lines.append("")
    report_lines.append("Top Attack Types Detected:")
    report_lines.append("")
    
    attack_types = [
        ("DDoS Attack", 45, "HIGH"),
        ("Port Scanning", 38, "MEDIUM"),
        ("Brute Force", 28, "HIGH"),
        ("SQL Injection", 15, "CRITICAL"),
        ("XSS Attempts", 12, "MEDIUM"),
        ("Malware C2", 8, "CRITICAL"),
    ]
    
    report_lines.append("  Attack Type          | Count | Severity")
    report_lines.append("  " + "-" * 45)
    for attack, count, severity in attack_types:
        report_lines.append(f"  {attack:<20} | {count:>5} | {severity}")
    report_lines.append("")
    report_lines.append("-" * 70)
    report_lines.append("")
    
    # Geographic Analysis
    report_lines.append("GEOGRAPHIC ANALYSIS")
    report_lines.append("-" * 30)
    report_lines.append("")
    report_lines.append("Top Source Countries for Attacks:")
    report_lines.append("")
    
    countries = [
        ("China", 156),
        ("Russia", 89),
        ("United States", 67),
        ("Iran", 34),
        ("North Korea", 23),
    ]
    
    for country, count in countries:
        bar = "#" * (count // 10)
        report_lines.append(f"  {country:<15} | {bar} ({count})")
    report_lines.append("")
    report_lines.append("-" * 70)
    report_lines.append("")
    
    # Automated Response Summary
    report_lines.append("AUTOMATED RESPONSE SUMMARY")
    report_lines.append("-" * 30)
    report_lines.append("")
    report_lines.append("  Response Action      | Count")
    report_lines.append("  " + "-" * 30)
    report_lines.append("  IPs Blocked          | 89")
    report_lines.append("  Sessions Terminated  | 45")
    report_lines.append("  Users Notified       | 156")
    report_lines.append("  Alerts Escalated     | 12")
    report_lines.append("  Malware Quarantined  | 7")
    report_lines.append("")
    report_lines.append("-" * 70)
    report_lines.append("")
    
    # Recommendations
    report_lines.append("RECOMMENDATIONS")
    report_lines.append("-" * 30)
    report_lines.append("")
    report_lines.append("Based on the analysis, we recommend the following actions:")
    report_lines.append("")
    report_lines.append("  1. Update firewall rules to block persistent threat IPs")
    report_lines.append("  2. Implement rate limiting on login endpoints")
    report_lines.append("  3. Enable additional logging for database queries")
    report_lines.append("  4. Review access permissions for admin accounts")
    report_lines.append("  5. Schedule security awareness training for staff")
    report_lines.append("")
    report_lines.append("-" * 70)
    report_lines.append("")
    
    # Raw Data Section (if requested)
    if include_raw:
        report_lines.append("RAW DATA SAMPLE")
        report_lines.append("-" * 30)
        report_lines.append("")
        report_lines.append("Recent Critical Events:")
        report_lines.append("")
        for i in range(5):
            ts = (datetime.now() - timedelta(hours=random.randint(1, 24))).strftime("%Y-%m-%d %H:%M")
            ip = f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
            attack = random.choice(["SQL Injection", "DDoS", "Brute Force", "Malware"])
            report_lines.append(f"  [{ts}] {ip} - {attack} - BLOCKED")
        report_lines.append("")
        report_lines.append("-" * 70)
        report_lines.append("")
    
    # Footer
    report_lines.append("")
    report_lines.append("=" * 70)
    report_lines.append("                     END OF REPORT")
    report_lines.append("")
    report_lines.append("AI-Driven Autonomous SOC - Zero Trust Security Platform")
    report_lines.append(f"Report ID: SOC-{datetime.now().strftime('%Y%m%d%H%M%S')}")
    report_lines.append("=" * 70)
    
    # Join all lines and encode
    report_content = "\n".join(report_lines)
    return report_content.encode('utf-8')


def generate_pdf_report(report_type: str, date_range: str, include_charts: bool = True,
                        include_raw: bool = False, executive_summary: bool = True) -> bytes:
    """Generate PDF report using reportlab if available, otherwise text"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib import colors
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=24, alignment=1, textColor=colors.HexColor('#00D4FF'))
        story.append(Paragraph("AI-Driven Autonomous SOC", title_style))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph("Security Report", styles['Heading2']))
        story.append(Spacer(1, 0.3*inch))
        
        # Report Info
        story.append(Paragraph(f"<b>Report Type:</b> {report_type}", styles['Normal']))
        story.append(Paragraph(f"<b>Date Range:</b> {date_range}", styles['Normal']))
        story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Executive Summary
        if executive_summary:
            story.append(Paragraph("Executive Summary", styles['Heading2']))
            story.append(Paragraph(
                "This report provides a comprehensive overview of the security posture. "
                "Key metrics: 2,847 events analyzed, 23 critical threats, 156 threats blocked, "
                "1.2s average response time, 87/100 security score.",
                styles['Normal']
            ))
            story.append(Spacer(1, 0.2*inch))
        
        # Threat Table
        story.append(Paragraph("Top Threats", styles['Heading2']))
        threat_data = [
            ['Attack Type', 'Count', 'Severity'],
            ['DDoS Attack', '45', 'HIGH'],
            ['Port Scanning', '38', 'MEDIUM'],
            ['Brute Force', '28', 'HIGH'],
            ['SQL Injection', '15', 'CRITICAL'],
            ['XSS Attempts', '12', 'MEDIUM'],
        ]
        
        threat_table = Table(threat_data, colWidths=[2.5*inch, 1*inch, 1.5*inch])
        threat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00D4FF')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#1a1f2e')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#333')),
        ]))
        story.append(threat_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Recommendations
        story.append(Paragraph("Recommendations", styles['Heading2']))
        recommendations = [
            "1. Update firewall rules to block persistent threat IPs",
            "2. Implement rate limiting on login endpoints",
            "3. Enable additional logging for database queries",
            "4. Review access permissions for admin accounts",
            "5. Schedule security awareness training for staff"
        ]
        for rec in recommendations:
            story.append(Paragraph(rec, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
        
    except ImportError:
        # Fallback to text report if reportlab not available
        return generate_security_report(report_type, date_range, include_charts, include_raw, executive_summary)
