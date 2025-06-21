from docx import Document
from docx.shared import Pt, RGBColor

def generate_resume_docx(user_data):
    doc = Document()

    # 🧑‍💼 Ism — markazda
    name = doc.add_heading(user_data["name"], level=1)
    name.alignment = 1  # center

    # 📧 Email & telefon
    contact = doc.add_paragraph()
    contact_run = contact.add_run(f"📧 {user_data['email']} | 📞 {user_data['phone']}")
    contact_run.font.size = Pt(10)
    contact.alignment = 1

    # 🛠 Ko‘nikmalar
    doc.add_heading("🛠 Ko‘nikmalar", level=2).runs[0].font.color.rgb = RGBColor(0, 102, 204)
    for skill in user_data["skills"].split(','):
        doc.add_paragraph(skill.strip(), style='List Bullet')

    # 💼 Ish tajribasi
    doc.add_heading("💼 Ish tajribasi", level=2).runs[0].font.color.rgb = RGBColor(0, 102, 204)

    for line in user_data["experience"].split('\n'):
        parts = [p.strip() for p in line.split(',')]
        if len(parts) == 3:
            company, years, role = parts
            doc.add_paragraph(f"🏢 {company} ({years})", style='Heading 3')
            doc.add_paragraph(role, style='Normal')
        else:
            doc.add_paragraph(line, style='Normal')

    filename = f"{user_data['name'].replace(' ', '_')}_resume.docx"
    doc.save(filename)
    return filename
