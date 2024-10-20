import uuid

class ChatHandler:
    def __init__(self):
        # Store chat histories by interview_id
        self.history_store = {}

    def start_interview(self):
        # Create a unique interview_id for each new interview
        interview_id = str(uuid.uuid4())
        self.history_store[interview_id] = []
        return interview_id

    def add_to_chat_history(self, interview_id, question, answer):
        # Ensure the interview_id exists in the history store
        if interview_id in self.history_store:
            self.history_store[interview_id].append({"question": question, "answer": answer})
        else:
            raise ValueError("Invalid interview ID")

    def get_chat_history(self, interview_id):
        # Return the chat history for the given interview_id
        if interview_id in self.history_store:
            return self.history_store[interview_id]
        else:
            raise ValueError("Invalid interview ID")

    def reset_chat_history(self, interview_id):
        # Clear the chat history for a specific interview session
        if interview_id in self.history_store:
            self.history_store[interview_id] = []
        else:
            raise ValueError("Invalid interview ID")
