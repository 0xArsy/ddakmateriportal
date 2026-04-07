import os
import json
import re

def extract_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    # Basic text extraction from HTML
    # 1. Remove script and style
    html = re.sub(r'<(script|style).*?>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
    # 2. Extract content from specific tags or just all text
    tags_to_extract = re.findall(r'<(h[1-6]|p|li|td|strong|em|span|b|i|code).*?>(.*?)</\1>', html, flags=re.DOTALL | re.IGNORECASE)
    
    text_content = []
    for tag, content in tags_to_extract:
        # Clean tags inside content
        clean_text = re.sub(r'<.*?>', '', content)
        clean_text = clean_text.strip().replace('\n', ' ')
        if clean_text:
            text_content.append(clean_text)
            
    return " ".join(text_content)

def build_index():
    chapters = [
        {"id": "01", "title": "Topik 01: Introduction", "file": "TOPIK 01.html"},
        {"id": "02", "title": "Topik 02: Boolean Algebra", "file": "TOPIK 02.html"},
        {"id": "03", "title": "Topik 03: Karnaugh Map", "file": "TOPIK 03.html"},
        {"id": "04", "title": "Topik 04: Logic Gates and Combinational Logic", "file": "TOPIK 04.html"},
        {"id": "05", "title": "Topik 05: Combinational circuits MSI and Sequential circuits", "file": "TOPIK 05.html"},
        {"id": "06", "title": "Topik 06: Sequential circuits analysis, register and memory", "file": "TOPIK 06.html"},
        {"id": "07", "title": "Topik 07: Intro to computer architecture & Intro to Datapath", "file": "TOPIK 07.html"},
        {"id": "08", "title": "Topik 08: Introduction to AVR", "file": "TOPIK 08.html"}
    ]
    
    search_index = []
    for chapter in chapters:
        file_path = chapter['file']
        if os.path.exists(file_path):
            print(f"Indexing {file_path}...")
            content = extract_content(file_path)
            # Normalize and remove excessive spaces
            content = re.sub(r'\s+', ' ', content).strip()
            
            # Extract keywords (simple: alphanumeric or common DB terms)
            keywords = list(set(re.findall(r'\b\w{3,}\b', content.lower())))
            
            search_index.append({
                "title": chapter['title'],
                "file": chapter['file'],
                # We store a truncated content or just keywords to save space
                "keywords": keywords,
                # Store some preview text (first 200 chars)
                "preview": content[:200] + "..."
            })
            
    with open('search_index.json', 'w', encoding='utf-8') as f:
        json.dump(search_index, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    build_index()
