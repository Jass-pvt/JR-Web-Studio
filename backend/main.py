from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mail import FastMail, MessageSchema
from models import ContactForm
from email_config import conf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend working 🚀"}

@app.post("/contact")
async def contact(form: ContactForm):
    print("DATA RECEIVED:", form)

    try:
        message = MessageSchema(
            subject=f"New Contact from {form.name}",
            recipients=["devcraft.jr@gmail.com"],
            body=f"""
Name: {form.name}
Phone: {form.phone if form.phone else "Not provided"}
Email: {form.email}
Message: {form.message}
""",
            subtype="plain"
        )

        fm = FastMail(conf)

        print("👉 SENDING EMAIL NOW...")

        await fm.send_message(message)

        print("✅ EMAIL SENT SUCCESSFULLY")

        return {"status": "success"}

    except Exception as e:
        print("❌ EMAIL FAILED:", str(e))
        return {"status": "error", "detail": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)