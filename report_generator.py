"""
PDF Report Generator for Pothole Detection
Generates downloadable PDF reports with detection results and GPS location
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from pathlib import Path
import os

class PotholeReportGenerator:
    """Generate PDF reports for pothole detections"""
    
    def __init__(self, output_dir='reports'):
        """Initialize the report generator"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#6366f1'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#4b5563'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
        
        # Info style
        self.styles.add(ParagraphStyle(
            name='InfoText',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#374151'),
            spaceAfter=6
        ))
    
    def generate_report(self, detections, location=None, image_path=None):
        """
        Generate a PDF report for pothole detections
        
        Args:
            detections: List of detection dictionaries with bbox, confidence, severity
            location: Dictionary with 'latitude', 'longitude', 'accuracy'
            image_path: Path to the detection image (optional)
        
        Returns:
            str: Path to generated PDF file
        """
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'pothole_report_{timestamp}.pdf'
        filepath = self.output_dir / filename
        
        # Create PDF document
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build content
        story = []
        
        # Title
        story.append(Paragraph("Pothole Detection Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 12))
        
        # Report metadata
        story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                              self.styles['InfoText']))
        story.append(Paragraph(f"<b>Total Potholes Detected:</b> {len(detections)}", 
                              self.styles['InfoText']))
        story.append(Spacer(1, 20))
        
        # Location information
        if location:
            story.append(Paragraph("Location Information", self.styles['CustomSubtitle']))
            
            lat = location.get('latitude', 'N/A')
            lon = location.get('longitude', 'N/A')
            accuracy = location.get('accuracy', 'N/A')
            
            location_data = [
                ['Latitude:', f"{lat}°"],
                ['Longitude:', f"{lon}°"],
                ['Accuracy:', f"±{accuracy}m" if accuracy != 'N/A' else 'N/A'],
                ['Google Maps:', f'<link href="https://www.google.com/maps?q={lat},{lon}">View on Map</link>']
            ]
            
            location_table = Table(location_data, colWidths=[2*inch, 4*inch])
            location_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#374151')),
                ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#6b7280')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            
            story.append(location_table)
            story.append(Spacer(1, 20))
        
        # Detection details
        if detections:
            story.append(Paragraph("Detection Details", self.styles['CustomSubtitle']))
            
            # Create table data
            table_data = [['#', 'Severity', 'Confidence', 'Depth Score']]
            
            for idx, detection in enumerate(detections, 1):
                severity = detection.get('severity', 'Unknown')
                confidence = detection.get('confidence', 0) * 100
                depth_score = detection.get('depth_score', 0)
                
                # Color code severity
                if severity == 'High':
                    severity_text = f'<font color="#ef4444">🔴 {severity}</font>'
                elif severity == 'Medium':
                    severity_text = f'<font color="#f59e0b">🟡 {severity}</font>'
                elif severity == 'Low':
                    severity_text = f'<font color="#10b981">🟢 {severity}</font>'
                else:
                    severity_text = f'⚪ {severity}'
                
                table_data.append([
                    str(idx),
                    Paragraph(severity_text, self.styles['Normal']),
                    f'{confidence:.1f}%',
                    f'{depth_score:.3f}' if depth_score else 'N/A'
                ])
            
            detection_table = Table(table_data, colWidths=[0.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            detection_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
            ]))
            
            story.append(detection_table)
            story.append(Spacer(1, 20))
        
        # Add image if provided
        if image_path and Path(image_path).exists():
            story.append(Paragraph("Detection Image", self.styles['CustomSubtitle']))
            try:
                img = Image(str(image_path), width=5*inch, height=3.75*inch)
                story.append(img)
            except Exception as e:
                story.append(Paragraph(f"<i>Image could not be loaded: {e}</i>", 
                                     self.styles['Normal']))
        
        # Footer
        story.append(Spacer(1, 30))
        story.append(Paragraph(
            '<i>Generated by AI-Powered Pothole Detection System | YOLOv8 + MiDaS</i>',
            ParagraphStyle(
                'Footer',
                parent=self.styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#9ca3af'),
                alignment=TA_CENTER
            )
        ))
        
        # Build PDF
        doc.build(story)
        
        return str(filepath)

# Singleton instance
_report_generator = None

def get_report_generator():
    """Get or create the report generator singleton"""
    global _report_generator
    if _report_generator is None:
        _report_generator = PotholeReportGenerator()
    return _report_generator
