from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def generate_resume_docx(user_data):
    doc = Document()

    # Ism
    name = doc.add_heading(user_data['name'], level=0)
    name.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Aloqa
    contact = doc.add_paragraph()
    contact.add_run(f"📧 {user_data['email']} | 📞 {user_data['phone']}").font.size = Pt(9)
    contact.alignment = WD_ALIGN_PARAGRAPH.CENTER

    def add_section(title):
        p = doc.add_paragraph()
        run = p.add_run(title)
        run.bold = True
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0, 102, 204)

    # Maqsad
    add_section("🎯 Maqsad")
    doc.add_paragraph(user_data['objective'])

    # Ta’lim
    add_section("🎓 Ta’lim")
    for line in user_data['education'].split('\n'):
        doc.add_paragraph(line)

    # Ish tajribasi
    add_section("💼 Ish tajribasi")
    for line in user_data["experience"].split('\n'):
        parts = [p.strip() for p in line.split(',')]
        if len(parts) == 3:
            company, years, role = parts
            doc.add_paragraph(f"🏢 {company} ({years})", style='Heading 3')
            doc.add_paragraph(role)

    # Ko‘nikmalar
    add_section("🛠 Ko‘nikmalar")
    for skill in user_data["skills"].split(','):
        doc.add_paragraph(skill.strip(), style='List Bullet')

    # Tillar
    add_section("🌐 Tillar")
    for lang in user_data["languages"].split('\n'):
        doc.add_paragraph(lang.strip(), style='List Bullet')

    filename = f"{user_data['name'].replace(' ', '_')}_resume.docx"
    doc.save(filename)
    return filename
