from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from logger import get_logger
from utils import chatmessagetuple

logger = get_logger()

def create_pdf(messages: list[chatmessagetuple], output_path: str = "DocChatAI.pdf") -> str:
    """
    Create a PDF titled 'DocChatAI' from a list of (role, message) tuples.

    :param messages: List of tuples -> [(role, message), ...]
    :param output_path: Output PDF file path
    """
    logger.info(f"Creating PDF at {output_path} with {len(messages)} messages")
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )

    styles = getSampleStyleSheet()

    # Title style
    title_style = ParagraphStyle(
        name="TitleStyle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        textColor=HexColor("#2E3A59"),
        fontSize=28,
        spaceAfter=30,
    )

    # Role style
    role_style = ParagraphStyle(
        name="RoleStyle",
        parent=styles["Heading3"],
        textColor=HexColor("#1F6AE1"),
        spaceAfter=6,
        spaceBefore=12,
    )

    # Message style
    message_style = ParagraphStyle(
        name="MessageStyle",
        parent=styles["BodyText"],
        fontSize=11,
        leading=16,
        spaceAfter=10,
    )

    story = []

    # Title
    story.append(Paragraph("DocChatAI", title_style))
    story.append(Spacer(1, 0.3 * inch))

    # Messages
    for role, message in messages:
        role_text = role.capitalize()
        story.append(Paragraph(role_text, role_style))

        # Preserve line breaks
        message = message.replace("\n", "<br/>")
        story.append(Paragraph(message, message_style))

    doc.build(story)
    logger.info(f"PDF created successfully at {output_path}")
    
    return output_path
