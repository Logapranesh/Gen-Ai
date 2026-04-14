import ollama

MODEL = "llama3.2:3b"

roles = {
    "1": {"name": "Python Tutor", "prompt": "You are a Python tutor."},
    "2": {"name": "Fitness Coach", "prompt": "You are a fitness coach."},
    "3": {"name": "Travel Guide", "prompt": "You are a travel guide."}
}

def choose_role():
    print("\nAvailable Roles:")
    for key, role in roles.items():
        print(f"{key}. {role['name']}")
    return roles.get(input("Pick a role: "))


def chat():
    role = choose_role()

    if not role:
        print("Invalid choice")
        return chat()

    print(f"\nRole set: {role['name']}")

    messages = [
        {"role": "system", "content": role["prompt"]}
    ]

    while True:
        user_input = input("You: ")

        if user_input == "quit":
            break

        if user_input == "switch":
            return chat()

        messages.append({"role": "user", "content": user_input})

        response = ollama.chat(
            model=MODEL,
            messages=messages
        )

        reply = response["message"]["content"]

        messages.append({"role": "assistant", "content": reply})

        print(f"{role['name']}: {reply}")


chat()