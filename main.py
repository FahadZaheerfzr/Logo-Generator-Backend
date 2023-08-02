from fastapi import FastAPI, Request,Body,HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from connection import db
from logoai import LogoAi
import requests
import json
from PIL import Image
from io import BytesIO
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import cairosvg

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
    image_url = image_urls[0]["url"]
    name = prompt
    print (image_url)

    logo_response = requests.get(image_url)

    if logo_response.status_code != 200:
        return {"message": "Failed to generate logo"}

    # save to db
    # db.logos.insert_one({"name": name, "url": image_urls})
    #make request to get font
    payload = {
    "type": "sans-serif",
    "era": 0.7,
    "maturity": 0.4,
    "weight": 0,
    "personality": 0.5,
    "definition": 0.7,
    "concept": 0.6
}

    amount_near = 1 
    params = {
        "payload": json.dumps(payload),
        "amount_near": amount_near
    }
    res = requests.get('http://localhost:1234/getRecommendedFont', params=params)
    print(res.json())
    if res.status_code != 200:
        return {"message": "Failed to generate logo"}
    
    svgPath="logoString.svg"
    svg_string = res.json()["fonts"][0]['svg']
    with open(svgPath, 'w') as f:
        f.write(svg_string)
    pngPath="logoString.png"
    drawing = svg2rlg(svgPath)
    renderPM.drawToFile(drawing, pngPath, fmt="PNG")
    

    svg_image = Image.open(pngPath)

    logo_image = Image.open(BytesIO(logo_response.content))

    logo_image.paste(svg_image, (0, 0), svg_image)
    logo_image.save('logo.png')

    resImage64= logo_image.tobytes().decode('base64')

    return {"message": "Logo generated successfully", "image": image_urls, "newImage": resImage64}