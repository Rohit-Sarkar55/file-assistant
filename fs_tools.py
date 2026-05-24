import os,fitz
from docx import Document
from datetime import datetime

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
    
    elif filepath.endswith(".docx"):
        content = ""
        doc = Document(filepath)
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                content += paragraph.text + "\n"

        return {
            "success": True,
            "filepath": filepath,
            "extension": ".docx",
            "content": content
        }
    
    else:
        return {"success": False, "error": "File type not supported yet"}
    

def list_files(directory, extension=None):

    if not os.path.exists(directory):
        return {"success": False, "error": "Directory not found"}

    files = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        # Skip if it is not a file
        if not os.path.isfile(filepath):
            # print(f"Skipping non-file: {filename}")
            continue

        # Filter by extension if provided
        if extension and not filename.endswith(extension):
            continue

        # Get file metadata
        size = os.path.getsize(filepath)
        modified = os.path.getmtime(filepath)
        modified_readable = datetime.fromtimestamp(modified).strftime("%Y-%m-%d %H:%M:%S")

        files.append({
            "name": filename,
            "filepath": filepath,
            "size_bytes": size,
            "modified": modified_readable
        })

    return {"success": True, "directory": directory, "files": files}

def write_file(filepath, content):
    # Get the directory part of the filepath
    directory = os.path.dirname(filepath)

    # Create directories if they don't exist
    if directory:
        os.makedirs(directory, exist_ok=True)

    # Write content to file
    existing_content = ""
#     if os.path.exists(filepath):
#         with open(filepath, "r", encoding="utf-8") as f:
#             existing_content = f.read()

# # Write combined content — "w" creates file if not exists
#     with open(filepath, "w", encoding="utf-8") as f:
#         f.write(existing_content + "\n" + content)

    with open(filepath, "a+", encoding="utf-8") as f:
        if os.path.getsize(filepath) > 0:
            f.seek(0, 2)              # move cursor to end of file
            f.seek(f.tell() - 1)      # step back exactly one character
            last_char = f.read(1)     # read that one character

            if last_char != "\n":
                f.write("\n" + content + "\n")
            else:
                f.write(content + "\n")
        else:
            f.write(content + "\n")

    return {
        "success": True,
        "filepath": filepath,
        "message": f"File written successfully"
    }


if __name__ == "__main__":
    # result = read_file("resumes/test_3.docx")
    # result = list_files("resumes")
    # print(result)

    # result = list_files("resumes", ".pdf")
    # print(result)
    # Test 1 - write to existing outputs folder
    result = write_file("outputs/summary_john_doe.txt", "This is a summary of John Doe.")
    print(result)

    # Test 2 - write to a folder that doesn't exist yet
    result = write_file("outputs/new_folder/summary_test.txt", "Testing folder creation.")
    print(result)