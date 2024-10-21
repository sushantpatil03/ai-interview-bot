# src/modules/interview_evaluator.py
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from pydantic import BaseModel
from typing import List, Dict

class EvaluationResult(BaseModel):
    confidence_score: int
    communication_score: int
    strengths: List[str]
    weaknesses: List[str]
    detailed_feedback: str
    improvement_suggestions: List[str]

class InterviewEvaluator:
    def __init__(self):
        self.chat_model = ChatOpenAI(temperature=0.7, api_key="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")

    def evaluate_interview(self, chat_history: List[Dict[str, str]]) -> EvaluationResult:
        # Prepare the conversation history for analysis
        conversation = "\n".join([
            f"Q: {entry['question']}\nA: {entry['answer']}"
            for entry in chat_history
        ])

        system_prompt = """
        You are an expert interview evaluator. Analyze the following interview conversation and provide a detailed evaluation based on:
        1. Confidence (Scale 1-10): Assess how confidently the candidate communicated
        2. Communication (Scale 1-10): Evaluate clarity, structure, and effectiveness of responses
        3. Strengths: Identify key strong points demonstrated
        4. Weaknesses: Identify areas for improvement
        5. Detailed Feedback: Provide comprehensive analysis
        6. Improvement Suggestions: Offer specific recommendations

        Provide your evaluation in a structured format that can be parsed into the following JSON structure:
        {
            "confidence_score": int,
            "communication_score": int,
            "strengths": list[str],
            "weaknesses": list[str],
            "detailed_feedback": str,
            "improvement_suggestions": list[str]
        }
        """

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Here's the interview conversation to evaluate:\n\n{conversation}")
        ]

        response = self.chat_model(messages)
        
        # Parse the response and create an EvaluationResult
        # Note: In a production environment, you'd want to add proper error handling here
        import json
        evaluation_data = json.loads(response.content)
        
        return EvaluationResult(**evaluation_data)