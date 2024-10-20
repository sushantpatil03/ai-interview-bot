import fitz
import re

### FUNCTIONS TO EXTRACT CONENT FROM THE RESUME
def extract_resume_data(pdf_path):
    """
    Extracts content from a resume PDF and returns it in a structured format.
    
    Args:
    - pdf_path (str): The path to the resume PDF file.
    
    Returns:
    - dict: A dictionary with section headings as keys and their respective content as values.
    """
    document = fitz.open(pdf_path)
    
    resume_content = {
        "sections": []
    }
    
    section = None
    section_content = []
    
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" in block:
                block_text = ""
                for line in block["lines"]:
                    for span in line["spans"]:
                        block_text += span["text"]
                    block_text += "\n"
                
                # Detect if the block is a section heading
                if is_section_heading(block_text):
                    if section:  # Save the current section
                        resume_content["sections"].append({
                            "heading": section,
                            "content": "\n".join(section_content).strip()
                        })
                    # Start a new section
                    section = block_text.strip()
                    section_content = []
                else:
                    section_content.append(block_text.strip())

    # Add the last section if any
    if section:
        resume_content["sections"].append({
            "heading": section,
            "content": "\n".join(section_content).strip()
        })

    return resume_content

def is_section_heading(text):
    """
    Detects if a block of text is likely to be a section heading based on heuristics.
    Common sections in resumes are "Education", "Experience", etc.
    This function can be enhanced with more logic.
    
    Args:
    - text (str): A block of text from the PDF.
    
    Returns:
    - bool: True if the text is likely a section heading, False otherwise.
    """
    headings = ["Education", "Experience", "Skills", "Projects", "Certifications", "Achievements", "Languages"]
    text = text.strip().lower()
    
    if any(heading.lower() in text for heading in headings):
        return True
    
    # Simple heuristic: Text in uppercase or bold can be a heading
    if re.match(r"^[A-Z\s]+$", text) and len(text.split()) <= 5:
        return True
    
    return False
