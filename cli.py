from agent import CPGDecisionAgent

def main():
    agent = CPGDecisionAgent()

    print("\n Smart CPG Decision Support Agent (CLI)")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Ask your business question: ")

        if query.lower() == "exit":
            break

        response = agent.run(query)

        print("\n=== Strategy Memo ===\n")
        print(response)
        print("\n")

if __name__ == "__main__":
    main()
