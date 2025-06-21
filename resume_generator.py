from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH

def generate_resume_docx(user_data):
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style._element.rPr.rFonts.set(qn('w:eastAsia'), 'Calibri')

    # Ism
    name = doc.add_heading(user_data['name'], level=0)
    name.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Contact info
    contact = doc.add_paragraph()
    contact_run = contact.add_run(f"📧 {user_data['email']} | 📞 {user_data['phone']}")
    contact_run.font.size = Pt(9)
    contact.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Bo‘limlar uchun funksiya
    def add_section(title):
        sec = doc.add_paragraph()
        run = sec.add_run(title)
        run.bold = True
        run.font.color.rgb = RGBColor(0, 102, 204)
        run.font.size = Pt(12)
        sec.alignment = WD_ALIGN_PARAGRAPH.LEFT

    # Ko‘nikmalar (bullet list)
    add_section("🛠 Ko‘nikmalar")
    for skill in user_data["skills"].split(','):
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(skill.strip())

    # Ish tajribasi (kompaniya va lavozim)
    add_section("💼 Ish tajribasi")
    for line in user_data["experience"].split('\n'):
        company, years, role = [p.strip() for p in line.split(',')]
        # Kompaniya va vaqt — chap tomonda
        p1 = doc.add_paragraph()
        p1.add_run(f"{company} ({years})").bold = True
        # Lavozim — yangi paragraf
        doc.add_paragraph(role)

    filename = f"{user_data['name'].replace(' ', '_')}_resume.docx"
    doc.save(filename)
    return filename
