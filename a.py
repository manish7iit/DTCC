import fitz
import re

def extract(docu):
    doc = fitz.open(docu)
    pattern = re.compile(r"^\s*(\d{1,2})([\.\s]+)([A-Z][A-Z\s&]+)", re.MULTILINE)
    pages_text = [doc[i].get_text() for i in range(2,len(doc))]
    sections = []
    cur_section = None

    for page_num, text in enumerate(pages_text):
        matches = list(pattern.finditer(text))
        if matches:
            for i,match in enumerate(matches):
                heading = match.group().strip()
                start_ind = matches[i].end()
                next_ind=-1

                if(i+1<len(matches)):
                    next_ind=matches[i+1].end()

                if cur_section:
                    if(i==0):
                        cur_section["content"]+=text[:start_ind].strip()
                    cur_section['end_page'] = page_num
                    sections.append(cur_section)

                cur_section = {
                    "heading": heading,
                    "start_page": page_num,
                    "end_page": page_num,
                    "content": text[start_ind:next_ind].strip()
                }
        else:
            if cur_section:
                cur_section["content"] += text.strip()

    if cur_section:
        cur_section['end_page'] = len(doc) - 1
        sections.append(cur_section)

    return sections

if __name__ == "__main__":
    docu = "example.pdf"
    sections = extract(docu)

    for section in sections:
        print(f"Heading: {section['heading']}")
        print(f"Start Page: {section['start_page']+1}")
        print(f"End Page: {section['end_page']+1}")
        print(f"Content Preview:\n{section['content'][:]}\n")
