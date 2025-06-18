from docx import Document

def generate_resume_docx(user_data):
    doc = Document()
    doc.add_heading(user_data["name"], level=1)
    doc.add_paragraph(f"📧 Email: {user_data['email']}")
    doc.add_paragraph(f"📞 Telefon: {user_data['phone']}")

    doc.add_heading("🛠 Ko‘nikmalar", level=2)
    doc.add_paragraph(user_data["skills"])

    doc.add_heading("💼 Ish tajribasi", level=2)
    doc.add_paragraph(user_data["experience"])

    filename = f"{user_data['name'].replace(' ', '_')}_resume.docx"
    doc.save(filename)
    return filename
