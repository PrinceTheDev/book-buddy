"""
This module defines a function that fetches data from the google book api
"""

import os
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv ('GOOGLE_BOOK_API')

def fetch_books(query):
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}&key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data['items']
