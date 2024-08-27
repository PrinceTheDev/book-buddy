import requests
import os
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


load_dotenv()

GOOGLE_BOOKS_API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')

def fetch_books_from_google(query):
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}&key={GOOGLE_BOOKS_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data.get('items', [])

def parse_book_data(items):
    books = []
    for item in items:
        volume_info = item.get('volumeInfo', {})
        books.append({
            'id': item.get('id', ''),
            'title': volume_info.get('title', ''),
            'author': ', '.join(volume_info.get('authors', [])),
            'isbn': next((identifier['identifier'] for identifier in volume_info.get('industryIdentifiers', []) if identifier['type'] == 'ISBN_13'), ''),
            'publication_date': volume_info.get('publishedDate', ''),
            'genre': ', '.join(volume_info.get('categories', [])),
            'description': volume_info.get('description', ''),
            'cover_image': volume_info.get('imageLinks', {}).get('thumbnail', ''),
            'combined_features': f"{volume_info.get('title', '')} {', '.join(volume_info.get('authors', []))} {volume_info.get('description', '')}"
        })
    return books

def create_tfidf_matrix(books_data):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform([book['combined_features'] for book in books_data])
    return tfidf_matrix

def get_recommendations(book_id, books_data, tfidf_matrix):
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    idx = next((i for i, book in enumerate(books_data) if book['id'] == book_id), None)
    
    if idx is None:
        return []

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    book_indices = [i[0] for i in sim_scores[1:11]]

    return [books_data[i] for i in book_indices]

def recommend_books(user_id=None):
    query = 'bestsellers'
    items = fetch_books_from_google(query)
    books_data = parse_book_data(items)
    tfidf_matrix = create_tfidf_matrix(books_data)
    
    if not books_data:
        return []

    book_id = books_data[0]['id']
    recommended_books = get_recommendations(book_id, books_data, tfidf_matrix)

    return recommended_books

