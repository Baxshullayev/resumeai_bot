from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

def set_font(run, size=12, bold=False):
    run.font.name = 'Garamond'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Garamond')
    run.font.size = Pt(size)
    run.bold = bold

def generate_resume_docx(user_data):
    doc = Document()

    # Ism (sarlavha)
    name = doc.add_heading(level=0)
    name_run = name.add_run(user_data['name'])
    set_font(name_run, size=22, bold=True)
    name.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Aloqa (email, telefon)
    contact = doc.add_paragraph()
    contact_run = contact.add_run(f"📧 {user_data['email']} | 📞 {user_data['phone']}")
    set_font(contact_run, size=10)
    contact.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Bo‘lim nomlarini yozish uchun funksiyasi
    def add_section(title):
        p = doc.add_paragraph()
        run = p.add_run(title)
        set_font(run, size=14, bold=True)
        run.font.color.rgb = RGBColor(0, 102, 204)

    # 🎯 Maqsad
    add_section("🎯 Maqsad")
    p = doc.add_paragraph(user_data['objective'])
    set_font(p.runs[0], size=12)

    # 🎓 Ta’lim
    add_section("🎓 Ta’lim")
    for line in user_data['education'].split('\n'):
        p = doc.add_paragraph(line)
        set_font(p.runs[0], size=12)

    # 💼 Ish tajribasi
    add_section("💼 Ish tajribasi")
    for line in user_data["experience"].split('\n'):
        parts = [p.strip() for p in line.split(',')]
        if len(parts) == 3:
            company, years, role = parts
            company_paragraph = doc.add_paragraph(f"🏢 {company} ({years})", style='Heading 3')
            set_font(company_paragraph.runs[0], size=12, bold=True)
            role_paragraph = doc.add_paragraph(role)
            set_font(role_paragraph.runs[0], size=12)

    # 🛠 Ko‘nikmalar
    add_section("🛠 Ko‘nikmalar")
    for skill in user_data["skills"].split(','):
        p = doc.add_paragraph(skill.strip(), style='List Bullet')
        set_font(p.runs[0], size=12)

    # 🌐 Tillar
    add_section("🌐 Tillar")
    for lang in user_data["languages"].split('\n'):
        p = doc.add_paragraph(lang.strip(), style='List Bullet')
        set_font(p.runs[0], size=12)

    # 📊 Office dasturlari
    add_section("📊 Office dasturlari")
    for office_item in user_data["office"].split(','):
        p = doc.add_paragraph(office_item.strip(), style='List Bullet')
        set_font(p.runs[0], size=12)

    # Faylni saqlash
    filename = f"{user_data['name'].replace(' ', '_')}_resume.docx"
    doc.save(filename)
    return filename
