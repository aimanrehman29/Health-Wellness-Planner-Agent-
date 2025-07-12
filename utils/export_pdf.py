from fpdf import FPDF

def generate_pdf(plan_data, filename="health_wellness_plan.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in plan_data:
        pdf.cell(200, 10, txt=line, ln=True, align="L")
    pdf.output(filename)