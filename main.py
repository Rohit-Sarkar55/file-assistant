from llm_file_assistant import run_assistant

def main():
    print("=" * 50)
    print("Welcome to File Assistant")
    print("Type 'exit' or 'quit' to stop")
    print("=" * 50)

    while True:
        # Get user input
        user_input = input("\nYou: ").strip()

        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit"]:
            print("\nGoodbye!")
            break

        # Skip empty input
        if not user_input:
            continue

        # Run the assistant
        run_assistant(user_input)


if __name__ == "__main__":
    main()