"""Console entry point for the LangChain Salesforce POC."""

from langchain_sf_poc.agent import ask_agent


def main() -> None:
    print("LangChain Salesforce POC")
    print("Type 'exit' to quit.\n")

    while True:
        user_prompt = input("You: ").strip()
        if user_prompt.lower() in {"exit", "quit"}:
            print("Bye")
            break
        if not user_prompt:
            continue

        try:
            answer = ask_agent(user_prompt)
            print(f"Agent: {answer}\n")
        except Exception as exc:
            print(f"Error: {exc}\n")


if __name__ == "__main__":
    main()
