import os, json
from dotenv import load_dotenv
# from openai import OpenAI
from groq import Groq
from fs_tools import list_files , read_file , write_file

load_dotenv()

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# Define the tool for OpenAI
tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List all files in a directory. Optionally filter by file extension.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "The directory path to list files from e.g. resumes"
                    },
                    "extension": {
                        "type": "string",
                        "description": "Optional file extension to filter by e.g. .txt .pdf .docx"
                    }
                },
                "required": ["directory"]
            }
        }
    },{
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read and extract text content from a file. Supports PDF, TXT and DOCX formats.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "The full path to the file e.g. resumes/resume_test_1.txt"
                    }
                },
                "required": ["filepath"]
            }
        }
    },{
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write or append content to a file. Creates the file if it does not exist.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "The full path to the file to write to e.g. outputs/summary.txt"
                    },
                    "content": {
                        "type": "string",
                        "description": "The text content to write to the file"
                    }
                },
                "required": ["filepath", "content"]
            }
        }
    }
]

def run_assistant(user_message):
    print(f"\nYou: {user_message}")

    # Step 1 - Send user message to OpenAI
    messages = [
        {"role": "system", "content": "You are a file assistant. Only help with file related tasks. If a question is not related to files politely say you can only help with file related tasks. Never try to call tools for non file related questions."},
        {"role": "user", "content": user_message}
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message

    if response_message.tool_calls:
        tool_call = response_message.tool_calls[0]
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)

        print(f"\n[AI is calling tool: {tool_name} with args: {tool_args}]")

    # Step 3 - Call the actual tool
        if tool_name == "list_files":
            tool_result = list_files(**tool_args)
            # print(tool_result)
        elif tool_name == "read_file":
            tool_result = read_file(**tool_args)
        elif tool_name == "write_file":
            tool_result = write_file(**tool_args)
        
         # Step 4 - Send tool result back to Groq
        messages.append(response_message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(tool_result)
        })

        # Step 5 - Get final response from Groq
        final_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            # tools=tools dont need this
        )

        final_message = final_response.choices[0].message.content
        print(f"\nAssistant: {final_message}")
        return final_message
    
    else:
        print(f"\nAssistant: {response_message.content}")
        return response_message.content

# ---- TEST ----
# if __name__ == "__main__":
#     run_assistant("What files are in the resumes folder?")
    # run_assistant("How to cook turkey?")

# if __name__ == "__main__":
#     run_assistant("Read the file resume_test_1.txt from resumes folder")

if __name__ == "__main__":
    run_assistant("Create a file called summary.txt in outputs folder with content 'This is a test summary Rohit'")


    
