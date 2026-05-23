import os

def read_file(filepath):
    if not os.path.exists(filepath):
        return {"success": False, "error": "File not found"}
    
    if filepath.endswith(".txt"):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        return {
            "success": True,
            "filepath": filepath,
            "extension": ".txt",
            "content": content
        }

    
    else:
        return {"success": False, "error": "File type not supported yet"}
    

if __name__ == "__main__":
    result = read_file("resumes/test_1.txt")
    print(result)