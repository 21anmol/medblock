import docx

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

if __name__ == "__main__":
    docx_path = "Decentralized Healthcare Record System.docx"
    text = extract_text_from_docx(docx_path)
    print(text)