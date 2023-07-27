from dotenv import load_dotenv, find_dotenv
import openai
import os


_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.getenv("OPENAI_KEY")

class LogoAi:
    def __init__(self):
        """
        Initializes logo ai class
        """

    def getImageFromPrompt(self, prompt):
        """
        Generates image from prompt
        """
        response = openai.Image.create(
            prompt=prompt,
            n=10,
            size = "256x256",
        )
        image_url = response['data']

        return image_url