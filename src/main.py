import uvicorn
from groq import Groq
from fastapi import FastAPI, Form, Response
from twilio.twiml.messaging_response import MessagingResponse
from config import GROQ_API_KEY, MY_NUMBER

app = FastAPI()
client = Groq(api_key=GROQ_API_KEY)

@app.post("/whatsapp")
async def reply(From: str = Form(...), Body: str = Form(...)):
    if From != MY_NUMBER:
        print(f"Unauthorized access attempt from: {From}")
        return Response(content="", media_type="application/xml")

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": Body}]
        )
        ai_response = completion.choices[0].message.content
    except Exception as e:
        ai_response = "System error. Please try again later."
        print(f"Groq Error: {e}")

    twiml_resp = MessagingResponse()
    twiml_resp.message(ai_response)

    return Response(content=str(twiml_resp), media_type="application/xml")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)