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


def search_in_file(filepath, keyword):
    # Check if file exists
    if not os.path.exists(filepath):
        return {"success": False, "error": "File not found"}

    # Read the file content using our existing read_file function
    result = read_file(filepath)

    if not result["success"]:
        return {"success": False, "error": result["error"]}

    # Split content into lines
    lines = result["content"].split("\n")
    matches = []

    for i, line in enumerate(lines):
        if keyword.lower() in line.lower():
            # Get surrounding context (line before and after)
            context_start = max(0, i - 1)
            context_end = min(len(lines) - 1, i + 1)

            matches.append({
                "line_number": i + 1,
                "line": line,
                "context": lines[context_start:context_end + 1]
            })

    return {
        "success": True,
        "filepath": filepath,
        "keyword": keyword,
        "total_matches": len(matches),
        "matches": matches
    }


def search_all_files(directory, keyword, extension=None):
    # First list all files in the directory
    files_result = list_files(directory, extension)

    if not files_result["success"]:
        return {"success": False, "error": files_result["error"]}

    matched_files = []

    for file in files_result["files"]:
        filepath = file["filepath"]

        # Search for keyword in each file
        result = search_in_file(filepath, keyword)

        if result["success"] and result["total_matches"] > 0:
            matched_files.append({
                "filename": file["name"],
                "filepath": filepath,
                "total_matches": result["total_matches"]
            })

    return {
        "success": True,
        "directory": directory,
        "keyword": keyword,
        "total_files_searched": len(files_result["files"]),
        "matched_files": matched_files,
        "total_matched": len(matched_files)
    }


if __name__ == "__main__":
    result = search_all_files("resumes", "python")
    print(result)


# if __name__ == "__main__":
#     # result = read_file("resumes/resume_test_8.docx")
#     result = list_files("resumes")
#     for file in result["files"]:
#         print(file)

    # result = list_files("resumes", ".pdf")
    # print(result)
    # Test 1 - write to existing outputs folder
    # result = write_file("outputs/summary_john_doe.txt", "This is a summary of John Doe.")
    # print(result)

    # # Test 2 - write to a folder that doesn't exist yet
    # result = write_file("outputs/new_folder/summary_test.txt", "Testing folder creation.")
    # print(result)

    # result = search_in_file("resumes/test_1.txt", "python")
    # print(result)