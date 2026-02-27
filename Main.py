import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from fastapi.responses import FileResponse

# Setup the Clarifai Client
# Make sure your Replit Secret is named: CLARIFAI_KEY
client = OpenAI(
    base_url="https://api.clarifai.com",
    api_key=os.environ['CLARIFAI_API_KEY'],
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    character_name: str
    personality: str

@app.post("/chat")
async def chat_with_character(req: ChatRequest):
    try:
        print(f"Received message: {req.message}")
        response = client.chat.completions.create(
            model="https://clarifai.com/minimaxai/chat-completion/models/MiniMax-M2_5/versions/9a68428cb615414f99e45f04b9a84912",
            messages=[
                {"role": "system", "content": f"You are {req.character_name}. Personality: {req.personality}"},
                {"role": "user", "content": req.message}
            ],
            temperature=0.7
        )
        reply = response.choices[0].message.content
        print(f"AI Reply: {reply}")
        return {"reply": reply}
    except Exception as e:
        print(f"Error in chat: {str(e)}")
        return {"reply": f"Sorry, I encountered an error: {str(e)}"}

@app.get("/")
async def serve_website():
    return FileResponse('index.html')
