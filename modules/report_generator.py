from datetime import datetime
from fpdf import FPDF


def create_pdf_report(username, report_title, content):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "HealthLens AI", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "AI-Powered Multimodal Healthcare Assistant", ln=True, align="C")

    pdf.ln(10)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, report_title, ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Generated for: {username}", ln=True)
    pdf.cell(0, 8, f"Generated on: {datetime.now().strftime('%d %B %Y, %I:%M %p')}", ln=True)

    pdf.ln(8)

    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, content)

    pdf.ln(8)

    pdf.set_font("Arial", "I", 10)
    pdf.multi_cell(
        0,
        7,
        "Disclaimer: This report is AI-generated for educational purposes only. "
        "It is not a replacement for professional medical advice, diagnosis, or treatment."
    )

    return bytes(pdf.output(dest="S"))