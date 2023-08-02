from fastapi import FastAPI, Request,Body,HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from connection import db
from logoai import LogoAi
import requests
import json
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO


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

    logo_response = requests.get(image_url)
    print(logo_response)
    # store image as file
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
    
    text = res.json()["fonts"][0]['name']
    print("fonts/"+text)
    image = Image.open(BytesIO(logo_response.content))
    txt_layer = Image.new('RGBA', image.size, (255,255,255,0))

    average_color = get_average_color(image)
    inverted_color = invert_color(average_color)
    try:
        font = ImageFont.truetype("fonts/"+text+".ttf", 62)
    except:
        #otherwise must be otf file
        font = ImageFont.truetype("fonts/"+text+".otf", 62)

    d = ImageDraw.Draw(txt_layer)
    d.text((0,0), name, fill=inverted_color+(255,), font=font)
    out = Image.alpha_composite(image.convert("RGBA"), txt_layer)
    out.save('out.png')



    return {"message": "Logo generated successfully", "image": image_urls, "newImage": "none"}



def get_average_color(image):
    # Calculate the average color of the image
    colors = image.getdata()
    r, g, b = 0, 0, 0
    count = 0

    for color in colors:
        r += color[0]
        g += color[1]
        b += color[2]
        count += 1

    return (r // count, g // count, b // count)

def invert_color(color):
    r, g, b = color
    return (255 - r, 255 - g, 255 - b)