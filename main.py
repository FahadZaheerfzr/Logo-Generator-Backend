from fastapi import FastAPI, Request,Body,HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from connection import db
from logoai import LogoAi

app = FastAPI()
LogoBot = LogoAi()
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test-db")
async def test_db_connection():
    """
    Tests the database connection.

    Returns:
        dict: A dictionary containing the message and error (if any).
    """
    try:
        db.command("ping")
        return {"message": "Database connected successfully"}
    except Exception as e:
        return {"message": "Failed to connect to the database", "error": str(e)}
    
@app.post("/logos")
async def logoGeneration(request: Request):
    """
    Generates a logo from the prompt.

    Args:
        request (Request): The request object.

    Raises:
        HTTPException: If the prompt is not provided.

    Returns:
        dict: A dictionary containing the message and the generated logo.
    """
    data = await request.json()
    prompt = data.get("prompt")

    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt not provided")

    image_urls = LogoBot.getImageFromPrompt(prompt)
    name = prompt

    # save to db
    # db.logos.insert_one({"name": name, "url": image_urls})


    return {"message": "Logo generated successfully", "image": image_urls}