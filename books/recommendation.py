import requests
import os
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from books.models import Book


load_dotenv()

GOOGLE_BOOKS_API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')


def fetch_books_from_google(query):
    """
    Fetches books from the Google Books API based on the search query.
    """
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}&key={GOOGLE_BOOKS_API_KEY}'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data.get('items', [])

def parse_book_data(items):
    """
    Parses the raw book data from the Google Books API into a list of book dictionaries.
    """
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

def save_books_to_db(books):
    """
    Saves or updates the books in the database.
    """
    for book_data in books:
        Book.objects.update_or_create(
            isbn=book_data.get('isbn', ''),
            defaults={
                'title': book_data.get('title', ''),
                'author': book_data.get('author', ''),
                'publication_date': book_data.get('publication_date', ''),
                'genre': book_data.get('genre', ''),
                'description': book_data.get('description', ''),
                'cover_image': book_data.get('cover_image', '')
            }
        )

def create_tfidf_matrix(books_data):
    """
    Creates a TF-IDF matrix from the combined book features.
    """
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform([book['combined_features'] for book in books_data])
    return tfidf_matrix

def get_recommendations(book_id, books_data, tfidf_matrix):
    """
    Gets book recommendations based on the cosine similarity of TF-IDF vectors.
    """
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    idx = next((i for i, book in enumerate(books_data) if book['id'] == book_id), None)
    
    if idx is None:
        return []

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    book_indices = [i[0] for i in sim_scores[1:11]]  # Get top 10 recommendations

    return [books_data[i] for i in book_indices]

def recommend_books(user_id=None):
    """
    Recommends books based on a predefined query.
    """
    query = 'bestsellers'
    items = fetch_books_from_google(query)
    books_data = parse_book_data(items)
    save_books_to_db(books_data)
    tfidf_matrix = create_tfidf_matrix(books_data)
    
    if not books_data:
        return []

    book_id = books_data[0]['id']
    recommended_books = get_recommendations(book_id, books_data, tfidf_matrix)

    return recommended_books

def update_books_from_google(query=''):
    """
    Updates the books in the database based on a search query.
    """
    items = fetch_books_from_google(query)
    books = parse_book_data(items)
    save_books_to_db(books)

