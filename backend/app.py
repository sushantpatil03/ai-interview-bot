from fastapi import FastAPI
from pydantic import BaseModel
from src.modules.question_generator import QuestionGenerator
from src.modules.chat_handler import ChatHandler
from src.modules.resume_parser import parse_resume
from src.modules.interview_evaluator import InterviewEvaluator, EvaluationResult

app = FastAPI()

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


# Start a new interview (returns first question and interview_id)
@app.post("/start-interview")
async def start_interview(interview_input: InterviewInput):
    resume_content = interview_input.resume_content  # Resume content as string
    jd_text = interview_input.job_description  # Job Description

    # Start a new interview and get a unique interview_id
    interview_id = chat_handler.start_interview()

    # Generate the opening question based on JD and resume
    initial_question = question_gen.generate_initial_question(jd_text, resume_content)

    # Return the first question and the unique interview ID to the frontend
    return {"question": initial_question, "interview_id": interview_id}

# Process the user's answer and generate the next question
@app.post("/next-question")
async def get_next_question(answer_input: AnswerInput):
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

@app.post("/evaluate-interview", response_model=EvaluationResult)
async def evaluate_interview(evaluation_input: EvaluationInput):
    # Get the chat history for the interview
    chat_history = chat_handler.get_chat_history(evaluation_input.interview_id)
    
    # Initialize the evaluator
    evaluator = InterviewEvaluator()
    
    # Generate the evaluation
    evaluation_result = evaluator.evaluate_interview(chat_history)
    
    return evaluation_result


@app.post("/reset-interview")
async def reset_interview(interview_id: str):
    chat_handler.reset_chat_history(interview_id)
    return {"message": "Chat history reset successfully."}


### OLD CODE HEREE #####


# from src.extract_resume import extract_resume_data

# pdf_path = "SushantResume.pdf"
# resume_data = extract_resume_data(pdf_path)

# print(resume_data)

#### -------- NEWWW CODE --------- ########
# from fastapi import FastAPI, UploadFile, File
# from pydantic import BaseModel
# from src.modules.question_generator import QuestionGenerator
# from src.modules.chat_handler import ChatHandler
# from src.modules.resume_parser import parse_resume

# app = FastAPI()

# # Initialize the Question Generator and Chat Handler
# question_gen = QuestionGenerator()
# chat_handler = ChatHandler()

# # Data models
# class JobDescription(BaseModel):
#     description: str

# class AnswerInput(BaseModel):
#     interview_id: str
#     question: str
#     answer: str

# # Start a new interview (returns first question and interview_id)
# @app.post("/start-interview")
# async def start_interview(job_description: JobDescription, file: UploadFile = File(...)):
#     resume_content = parse_resume(await file.read())  # Parse resume content
#     jd_text = job_description.description  # Job Description

#     # Start a new interview and get a unique interview_id
#     interview_id = chat_handler.start_interview()

#     # Generate the opening question based on JD and resume
#     initial_question = question_gen.generate_initial_question(jd_text, resume_content)

#     # Return the first question and the unique interview ID to the frontend
#     return {"question": initial_question, "interview_id": interview_id}

# # Process the user's answer and generate the next question
# @app.post("/next-question")
# async def get_next_question(answer_input: AnswerInput):
#     interview_id = answer_input.interview_id
#     question = answer_input.question
#     answer = answer_input.answer

#     # Add the current question-answer pair to the chat history
#     chat_handler.add_to_chat_history(interview_id, question, answer)

#     # Retrieve the full chat history for the interview
#     chat_history = chat_handler.get_chat_history(interview_id)

#     # Generate the next question based on the chat history
#     next_question = question_gen.generate_next_question(chat_history)

#     # Return the next question and updated chat history
#     return {"next_question": next_question, "chat_history": chat_history}

# @app.post("/reset-interview")
# async def reset_interview(interview_id: str):
#     chat_handler.reset_chat_history(interview_id)
#     return {"message": "Chat history reset successfully."}
