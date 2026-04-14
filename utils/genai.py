from google import genai
import logging
import os

PROJECT_ID = os.getenv("PROJECT_ID", "ai-event-flow-optimizer")

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location="us-central1",
)


logging.basicConfig(level=logging.INFO)

def get_ai_response(prompt):
    try:
        logging.info("Sending request to Vertex AI")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        logging.info("Response received from Vertex AI")

        return response.text if hasattr(response, "text") else "No response"

    except Exception as e:
        logging.error(f"Vertex AI Error: {str(e)}")
        return "⚠️ AI service unavailable"