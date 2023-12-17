import google.generativeai as genai

class GoogleGenerativeAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.model = None
        self.configure()

    def configure(self):
        genai.configure(api_key=self.api_key)
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
        ]

        self.model = genai.GenerativeModel(model_name="gemini-pro",
                                           generation_config=generation_config,
                                           safety_settings=safety_settings)

    def generate_content(self, prompt_parts):
        response = self.model.generate_content(prompt_parts)
        return response.text

# Usage Example
# api_key = "YOUR_API_KEY"  # Replace with your API key
# google_ai = GoogleGenerativeAI(api_key)
# prompt_parts = ["你好"]
# response_text = google_ai.generate_content(prompt_parts)
# print(response_text)
