from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.modules.question_generator import QuestionGenerator
from src.modules.chat_handler import ChatHandler
from src.modules.resume_parser import parse_resume
from src.modules.interview_evaluator import InterviewEvaluator, EvaluationResult

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize the Question Generator and Chat Handler
question_gen = QuestionGenerator()
chat_handler = ChatHandler()

# Data models
class InterviewInput(BaseModel):
    job_description: str
    resume_content: str

class AnswerInput(BaseModel):
    interview_id: str
    question: str
    answer: str
    
class EvaluationInput(BaseModel):
    interview_id: str

# Add a health check endpoint
@app.get("/health-check")
async def health_check():
    return {"status": "ok"}

# Start a new interview (returns first question and interview_id)
@app.post("/start-interview")
async def start_interview(interview_input: InterviewInput):
    try:
        resume_content = interview_input.resume_content
        jd_text = interview_input.job_description

        # Start a new interview and get a unique interview_id
        interview_id = chat_handler.start_interview()

        # Generate the opening question based on JD and resume
        initial_question = question_gen.generate_initial_question(jd_text, resume_content)

        # Return the first question and the unique interview ID to the frontend
        return {"question": initial_question, "interview_id": interview_id}
    except Exception as e:
        return {"error": str(e)}, 500

# Process the user's answer and generate the next question
@app.post("/next-question")
async def get_next_question(answer_input: AnswerInput):
    try:
        interview_id = answer_input.interview_id
        question = answer_input.question
        answer = answer_input.answer

        # Add the current question-answer pair to the chat history
        chat_handler.add_to_chat_history(interview_id, question, answer)

        # Retrieve the full chat history for the interview
        chat_history = chat_handler.get_chat_history(interview_id)

        # Generate the next question based on the chat history
        next_question = question_gen.generate_next_question(chat_history)

        # Return the next question and updated chat history
        return {"next_question": next_question, "chat_history": chat_history}
    except Exception as e:
        return {"error": str(e)}, 500

@app.post("/evaluate-interview", response_model=EvaluationResult)
async def evaluate_interview(evaluation_input: EvaluationInput):
    try:
        # Get the chat history for the interview
        chat_history = chat_handler.get_chat_history(evaluation_input.interview_id)
        
        # Initialize the evaluator
        evaluator = InterviewEvaluator()
        
        # Generate the evaluation
        evaluation_result = evaluator.evaluate_interview(chat_history)
        
        return evaluation_result
    except Exception as e:
        return {"error": str(e)}, 500

@app.post("/reset-interview")
async def reset_interview(interview_id: str):
    try:
        chat_handler.reset_chat_history(interview_id)
        return {"message": "Chat history reset successfully."}
    except Exception as e:
        return {"error": str(e)}, 500