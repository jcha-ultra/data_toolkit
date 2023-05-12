"""OpenAI API Example."""

import sys
import openai
import pickle

sys.path.append("")

# Load conversation history from file
def load_conversation_history(file_name):
    try:
        with open(file_name, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []

# Save conversation history to file
def save_conversation_history(file_name, conversation_history):
    with open(file_name, 'wb') as file:
        pickle.dump(conversation_history, file)

# Define a function to complete a chat message
def chatcompletion(messages):
    # Use the chatcompletion endpoint with the messages as the query
    response = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model="gpt-4",
        messages=messages,
    )
    # Return the generated text
    return response["choices"][0]["message"]["content"]

def word_count(messages):
    total_words = 0
    for message in messages:
        total_words += len(message["content"].split())
    return total_words

def remove_oldest_message(messages):
    if messages:
        messages.pop(0)
    return messages

word_threshold = 5000  # Set the word threshold

# Initialize an empty list to store messages
conversation_file = "conversation_history.pkl"
conversation_history = load_conversation_history(conversation_file)


system_message = """You are a software architect who can help collaborators create robust software systems based on information that they provide you. Your goal is to get your collaborator to provide you relevant information so that you can come up with the best solution given the requirements.

You will follow the following process:
1. Based on my input, you will generate the following sections (make sure to include information from your previous responses, unless they're redundant):
   a) Known Facts: the relevant facts needed for the recommendation.
   b) Analysis: perform a step-by-step analysis of the the Known Facts to arrive at both reasonable deductions from the facts, as well as identifying what else needs to be discovered.
   c) Proposed Solution: your current solution based on the known facts, accounting for the unknown elements. Include code snippets, schemas, outlines, etc. if that would be helpful as illustration. If you do not have enough information to make a recommendation, then state that you don't know instead of making a recommendation. 
   d) Evaluation: your evaluation of the notable advantages, drawbacks, and potential uncertainties of the proposed solution.
   e) Questions/Requests: what additional information that I can provide you to improve your recommendation—including sending resources that you do not have access to (such as from internet searches). Be precise in your request. If you don't need any additional information, then say so.
2. We will continue this iterative process with me providing additional information to you and you updating the output sections until you believe you do not need any additional information for your recommendation."""
print(system_message)

# Send an initial greeting message
initial_message = "AI: Hi. What should the software product be about? Please provide a description of the project, its purpose, and any specific requirements or constraints."
print(initial_message)
conversation_history.append({"role": "assistant", "content": initial_message})

while True:
    # Get user input from the command line with multi-line support
    print("Enter your message (type <send> on a new line to send):")
    user_message_lines = []
    while True:
        line = input()
        if line == "<send>":
            break
        user_message_lines.append(line)
    user_message = "\n".join(user_message_lines)

    # Exit the loop if the user types "quit"
    if user_message.lower() == "quit":
        break

    # Add the user's message to the conversation history
    conversation_history.append({"role": "user", "content": user_message})

    conversation_history_with_system = conversation_history + [{"role": "system", "content": system_message}]

    # Remove oldest messages if the conversation exceeds the word threshold
    while word_count(conversation_history_with_system) > word_threshold:
        conversation_history = remove_oldest_message(conversation_history)
        conversation_history_with_system = conversation_history + [{"role": "system", "content": system_message}]

    # Save the conversation history after each user message
    save_conversation_history(conversation_file, conversation_history)

    # Call the function with the updated conversation_history and store the response
    response = chatcompletion(conversation_history_with_system)
    print("AI:", response)

    # Add the response to the conversation history
    conversation_history.append({"role": "assistant", "content": response})

    # Save the conversation history after each AI message
    save_conversation_history(conversation_file, conversation_history)
