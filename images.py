import requests
import json
import base64
import random
import streamlit as st
import os
from replicate.client import Client
from dotenv import load_dotenv

load_dotenv()
replicate_api_token = os.getenv("REPLICATE_API_TOKEN")

if not replicate_api_token:
    raise ValueError("REPLICATE_API_TOKEN environment variable not set")

replicate_client = Client(api_token=replicate_api_token)

def get_image(prompt: str):
    url = f"https://generateimage-lkjcclx3ma-uc.a.run.app?prompt={requests.utils.quote(prompt)}"
    response = requests.get(url)
    if response.status_code == 200:
        response_json = json.loads(response.content)
        base64_url = response_json.get("base64Url")
        if base64_url:
            decoded_url = base64.b64decode(base64_url).decode('utf-8')
            return decoded_url
        else:
            return "Error: base64Url not found in response"
    else:
        return f"Error: {response.status_code}, {response.text}"
   
def fetch_random_image_url():
    with open('prompts.txt', 'r') as f:
        lines = f.readlines()
        random_line = random.choice(lines).strip()  # Get a random line and strip any extraneous whitespace
        prompt, image_url = random_line.split('|')  # Split the line into prompt and image URL
        return prompt, image_url

def fetch_image_urls(prompt: str):
    image_url = get_image(prompt)
    return image_url