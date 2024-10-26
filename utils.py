import json
from langchain.schema.messages import HumanMessage, AIMessage
from datetime import datetime

def save_chat_history_json(chat_history, file_path):
    print("Writing to file:", file_path)  # Add this line
    with open(file_path, "w") as f:
        json_data = [message.dict() for message in chat_history]
        json.dump(json_data, f)
        print("Data written successfully.")  # Confirm writing was successful


def load_chat_history_json(file_path):
    with open(file_path, "r") as f:
        json_data = json.load(f)
        messages = [HumanMessage(**message) if message["type"] == "human" else AIMessage(**message) for message in json_data]
        return messages

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")

