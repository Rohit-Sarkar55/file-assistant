import os,fitz

def read_file(filepath):
    if not os.path.exists(filepath):
        return {"success": False, "error": "File not found"}
    
    if filepath.endswith(".txt"):
        content = ""
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        return {
            "success": True,
            "filepath": filepath,
            "extension": ".txt",
            "content": content
        }
    elif filepath.endswith(".pdf"):
        content = ""
        with fitz.open(filepath) as pdf_file:
            for page in pdf_file:
                content += page.get_text()

        return {
            "success": True,
            "filepath": filepath,
            "extension": ".pdf",
            "content": content
        }
    
    else:
        return {"success": False, "error": "File type not supported yet"}
    

if __name__ == "__main__":
    result = read_file("resumes/test_2.pdf")
    print(result)