from google import genai

client = genai.Client(
    vertexai=True,
    project="ai-event-flow-optimizer",
    location="us-central1",
    http_options={"api_version": "v1"},
)

def get_ai_response(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text
