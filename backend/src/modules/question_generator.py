from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

class QuestionGenerator:
    def __init__(self):
        self.chat_model = ChatOpenAI(temperature=0.7, api_key="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")

    def generate_initial_question(self, job_description, resume_content):
        # Define the initial system message to instruct the model
        system_prompt = f"You are an interviewer. Given this Job Description: '{job_description}' and this Resume: '{resume_content}', start the interview by asking a relevant opening question. Prioritize getting personalized with the user's resume and jd. Try to ask question based on the details he/she submitted"

        # Generate the initial question
        response = self.chat_model([SystemMessage(content=system_prompt)])
        return response.content

    def generate_next_question(self, chat_history):
        # Build the conversation history based on chat_history
        messages = [SystemMessage(content="You are an interviewer.")]
        for entry in chat_history:
            messages.append(HumanMessage(content=f"Question: {entry['question']}"))
            messages.append(HumanMessage(content=f"Answer: {entry['answer']}"))

        # Continue the interview and generate the next question
        prompt = "Based on the conversation so far, ask the next personalized interview question. Consider a follow up or a fresh question on a new topic. (Only return question text)"
        messages.append(HumanMessage(content=prompt))

        response = self.chat_model(messages)
        return response.content
