import PyPDF2

def parse_resume(file_content):
    pdf_reader = PyPDF2.PdfReader(file_content)
    resume_text = ""

    for page in pdf_reader.pages:
        resume_text += page.extract_text()

    return resume_text
