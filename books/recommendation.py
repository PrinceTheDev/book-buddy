from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import Book

def create_tfidf_matrix():
    books = Book.objects.all()
    books_data = list(books.values('title', 'author', 'description'))

    for book in books_data:
        book['combined_features'] = f"{book['title']} {book['author']} {book['description']}"

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform([book['combined_features'] for book in books_data])

    return books_data, tfidf_matrix

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
    books_data, tfidf_matrix = create_tfidf_matrix()

    book_id = books_data[0]['id']

    recommended_books = get_recommendations(book_id, books_data, tfidf_matrix)

    return recommended_books

