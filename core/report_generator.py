def generate_pdf_report(total, pos, neg, neu, avg, seq_time, par_time):

    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.pagesizes import A4
    from datetime import datetime
    import os

    if not os.path.exists("reports"):
        os.makedirs("reports")

    file_path = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("Sentiment Analysis Report", styles["Title"]))
    elements.append(Spacer(1, 20))

    content = f"""
    Generated On: {datetime.now()}<br/><br/>

    Total Records: {total}<br/>
    Positive: {pos}<br/>
    Negative: {neg}<br/>
    Neutral: {neu}<br/>
    Average Score: {round(avg,2)}<br/><br/>

    Sequential Time: {round(seq_time,4)} sec<br/>
    Parallel Time: {round(par_time,4)} sec<br/>
    """

    elements.append(Paragraph(content, styles["Normal"]))

    doc.build(elements)

    return file_path