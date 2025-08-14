from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def generate(prompt: str):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text

class ScriptWriter:
    def __init__(self, problem: str, solution: str, keywords: list):
        self.problem = problem
        self.solution = solution
        self.keywords = keywords
        

    def generate(self):
        prompt = f"Generate a base script for the following problem: {self.problem}, solution: {self.solution}, keywords: {self.keywords}"
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text