from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

def generate_pdf_report(score, explanation, transactions, ai_summary=None):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, height - 60, "Smart Credit Analysis Report")
    c.setFont("Helvetica", 12)
    c.drawString(40, height - 100, f"Credit Trust Score: {score}/100")

    y = height - 140
    c.setFont("Helvetica", 10)
    c.drawString(40, y, "Score explanation:")
    y -= 14
    for k, v in explanation.items():
        if k == 'components':
            c.drawString(60, y, "Components:")
            y -= 12
            for ck, cv in v.items():
                c.drawString(80, y, f"- {ck}: {cv:.2f}")
                y -= 12
        else:
            c.drawString(60, y, f"{k}: {v}")
            y -= 12

    y -= 6
    if ai_summary:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, "AI Summary:")
        y -= 14
        c.setFont("Helvetica", 10)
        for line in ai_summary.get('summary','').splitlines():
            c.drawString(60, y, line[:100])
            y -= 12
            if y < 60:
                c.showPage()
                y = height - 60

    y -= 6
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Recent transactions:")
    y -= 14
    c.setFont("Helvetica", 9)
    for t in transactions[:20]:
        c.drawString(60, y, f"{t.get('date')} — £{t.get('amount'):.2f} — {t.get('raw')[:80]}")
        y -= 12
        if y < 60:
            c.showPage()
            y = height - 60
    c.save()
    buf.seek(0)
    return buf.read()
