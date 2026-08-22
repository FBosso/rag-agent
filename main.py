from graph import app


def main():
    print("Agent ready! Write something to begin. Write 'exit' to end the session")

    while True:
        user_input = input("Human: ")
        #terminating condition
        if user_input.lower().strip() == "exit":
            print("🤖 Agent: See you next time!")
            break
        
        events = app.stream(
            {"messages": [("user", user_input)]}, #input to the graph
            stream_mode="values" #returns the entire state after every node
        )

        for event in events:
            last_message = event["messages"][-1] #select the last message

        if last_message.type == "ai" and not last_message.tool_calls:
            print(f"🤖 Agent: {last_message.content}\n") #if it is ai i print it


if __name__ == "__main__":
    main()
