# File Assistant

A conversational file assistant powered by Groq (LLaMA) that can read, list, search and write files using natural language queries.

## Project Structure

```
file-assistant/
├── resumes/                  # Sample files for testing
├── outputs/                  # AI generated output files
├── fs_tools.py               # Core file system tools
├── llm_file_assistant.py     # Groq LLM integration
├── main.py                   # Entry point
├── requirements.txt          # Dependencies
└── .env                      # API keys (not in git)
```

## Setup

1. Clone the repository
2. Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create `.env` file in project root

```
GROQ_API_KEY=your_groq_api_key_here
```

5. Run the assistant

```bash
python main.py
```

## Example Queries

```
What files are in the resumes folder?
Read the file resume_test_1.txt from resumes folder
Search for Python in resumes/resume_test_1.txt
Create a summary file in outputs folder called summary.txt with content 'John Doe is a Python developer'
```

## Tools

| Tool | Description |
|---|---|
| `read_file()` | Reads PDF, TXT, DOCX files |
| `list_files()` | Lists files in a directory |
| `write_file()` | Writes or appends content to a file |
| `search_in_file()` | Searches for keywords in a file |

## Dependencies

| Library | Purpose |
|---|---|
| `groq` | LLM API client |
| `pymupdf` | PDF reading |
| `python-docx` | DOCX reading |
| `python-dotenv` | Environment variables |

## How It Works

```
You type a natural language query
        ↓
Groq reads the query and decides which tool to call
        ↓
Python executes the actual tool
        ↓
Result is sent back to Groq
        ↓
Groq forms a human readable answer
        ↓
Answer is printed to terminal



[screen-capture.webm](https://github.com/user-attachments/assets/2aa6c5d7-615c-4338-b4c6-c8b5e2e567d0)

```
