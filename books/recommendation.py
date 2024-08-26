import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import Book, Rating, User

def load_data():
    # Load data from the database
    books = pd.DataFrame(list(Book.objects.all().values()))
    ratings = pd.DataFrame(list(Rating.objects.all().values()))
    return books, ratings

def create_tfidf_matrix(books):
    # Combine relevant text features
    books['combined_features'] = books['title'] + ' ' + books['author'] + ' ' + books['publisher']

    # Create a TF-IDF Vectorizer to transform text data into feature vectors
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(books['combined_features'])

    return tfidf_matrix

def get_recommendations(book_id, books, tfidf_matrix):
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    idx = books[books['id'] == book_id].index[0]

    # Get pairwise similarity scores for all books with the given book
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices of the most similar books
    book_indices = [i[0] for i in sim_scores[1:11]]  # Top 10 similar books

    return books.iloc[book_indices]

def recommend_books(user_id):
    books, ratings = load_data()
    tfidf_matrix = create_tfidf_matrix(books)

    # Get the books the user has rated
    user_ratings = ratings[ratings['user_id'] == user_id]
    
    recommended_books = pd.DataFrame()

    for book_id in user_ratings['book_id']:
        recommended_books = pd.concat([recommended_books, get_recommendations(book_id, books, tfidf_matrix)])

    # Drop duplicates and return the top 10 recommendations
    return recommended_books.drop_duplicates().head(10)

