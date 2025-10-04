import os
from dotenv import load_dotenv
load_dotenv()
import ollama
# from langchain_core.output_parsers import PydanticOutputParser
# from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel
class Disease(BaseModel):
    name: str
    percentage: int

class Analyze(BaseModel):
    top_5_disease: list[Disease] 
    prescribed_medicine: list[str] 
    transcript_summary: str


class Agent:
    def __init__(self):
        self.model = os.getenv('LLM_MODEL')

    def __generate_response(self, prompt: str) -> str:
        """
        Generates a response from the LLM based on the provided prompt.
        
        Returns:
            str: The generated response from the LLM.
        """
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                format=Analyze.model_json_schema())
            return response['message']['content']
        except Exception as e:
            raise RuntimeError(f"Error generating response: {e}")

    def analyze_transcript(self, transcript: str) -> tuple:
        """
        Analyzes the transcript to extract top 5 diseases, prescribed medicine, and summary.
        
        Returns:
            tuple: A tuple containing:
                - top_5_disease: List of top 5 diseases.
                - prescribed_medicine: List of prescribed medicines.
                - transcript_summary: Summary of the consultation.
        """
        prompt = f"""
        Analyze the following transcript and extract the following 
        1. top 5 diseases with each percentage out of 100.
        2. prescribed medicine
        3. summary in 3rd person's point of view.
        Transcript: {transcript}"""
        response = self.__generate_response(prompt)
        return response




# Demo conversation
Conversation = """
Doctor: Good morning Mr. Sanchez. What brought you here today?
Patient: Good morning doctor. My left shoulder hurts.
Doctor: Oh, I’m sorry to hear that. When did it start?
Patient: I can’t remember when it started doctor.
Doctor: Are there any events that you think triggered your shoulder pain?
Patient: I couldn’t think of anything doctor.
Doctor: Oh I see. Is it painful all the time?
Patient: It comes and goes doctor.
Doctor: Has it been worsening?
Patient: Yes, it has worsened now.
Doctor: What is the pain like? Sharp? Dull? Tingling?
Patient: It’s sharp doctor.
Doctor: Does it radiate to any other parts of your body?
Patient: Yes doctor, the pain radiates to my neck and arm at the same side.
Doctor: On a scale of 1 to 10, with 10 as the highest and 0 as no pain at all, how severe is the pain?
Patient: 8, doctor.
Doctor: Oh it must be really painful for you. Is there anything that makes the pain worse?
Patient: There’s nothing that I know of that makes the pain worse.
Doctor: How about anything that makes it better? Like medications?
Patient: It doesn’t improve with the medication I’m taking, but the pain lessens when I’m resting my shoulder.
Doctor: What medication are you taking?
Patient: Pain killer, doctor, Ibuprofen.
Doctor: Have you ever had the same pain before?
Patient: No, doctor.
Doctor: Do you have any other symptoms?
Patient: None, doctor.
Doctor: Do you have any other medical problems like high blood pressure or diabetes?
Patient: Yes, I have hypertension
Doctor: What medications are you taking for it?
Patient: HCTZ, doctor.
Doctor: Is there anybody in your family having heart problems, strokes or diabetes?
Patient: My father died because of diabetes.
Doctor: Ok. Now I’m going to ask you some personal questions that would be helpful. Do you mind?
Patient: Not at all, doctor. Please feel free to ask questions.
Doctor: Thanks. What type of work do you do?
Patient: I’m a factory worker.
Doctor: Okay. Do you drink?
Patient: Yes, doctor, every Saturday night.
Doctor: How many bottles do you drink?
Patient: 4-5 bottles of beer per night doctor.
Doctor: Okay, it’s better if you cut down on your drinking habits like you drink 2-3 bottles of beer only.
Patient: I’ll try to do that, doctor, thanks!
Doctor: Do you smoke?
Patient: No, doctor.
Doctor: Oh, that’s good. Thank you for answering all my questions. Now, you will go through some tests for
me to have a clear diagnosis of your illness. Is this OK with you?
DOCTOR-PATIENT CONVERSATION
Patient: Yes, it’s OK doctor. Thank you.
Doctor: You’re welcome."""

# ag = Agent()
# ag.analyze_transcript(Conversation)  # 