# Book Buddy

![Book Buddy Logo](root/book-buddy/static/images/logo.png)

## Project Overview

Book Buddy is a web-based application designed to recommend books based on user preferences and reading history. It allows users to browse books, get personalized recommendations, and view detailed book information.

## Features

- **User Accounts**: Users can create accounts and log in to manage their preferences and reading history.
- **Book Search**: Search for books using the Google Books API.
- **Recommendations**: Personalized book recommendations based on user preferences and reading history.
- **Book Details**: View detailed information about each book, including cover image, author, publication date, genre, and description.
- **Responsive Design**: A user-friendly and responsive design that works across various devices.

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/your-username/book-buddy.git
    cd book-buddy
    ```

2. **Create a Virtual Environment**

    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows use: env\Scripts\activate
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**

    Create a `.env` file in the root directory of the project and add your Google Books API key:

    ```plaintext
    GOOGLE_BOOKS_API_KEY=your_google_books_api_key
    ```

5. **Apply Migrations**

    ```bash
    python manage.py migrate
    ```

6. **Run the Development Server**

    ```bash
    python manage.py runserver
    ```

    Access the application at `http://127.0.0.1:8000/`.

## Usage

- **Home Page**: Displays the latest books and featured recommendations.
- **Search Books**: Use the search bar to find books by title, author, or keyword.
- **Book Details**: Click on a book to view detailed information.
- **Recommendations**: Get personalized book recommendations based on your reading history.

## API Endpoints

- **Search Books**

    `GET /api/search/`

    Parameters: `query`

- **Recommendations**

    `GET /api/recommendations/`

    Parameters: `user_id`

    **Note**: Recommendations are still being refined.

## Testing

1. **Run Tests**

    ```bash
    python manage.py test
    ```

2. **Check Test Coverage**

    Ensure that your tests cover the major functionalities of the application, including search, recommendations, and book details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Google Books API](https://developers.google.com/books)
- [Django](https://www.djangoproject.com/)
- [Scikit-Learn](https://scikit-learn.org/)

## Disclaimer

This project is a work in progress, and there are still many updates and improvements to be made. Your feedback and contributions are appreciated as we continue to enhance the application.


