# SCIO_sovellus

SCIO is a scientific community platform where users can share research, articles, discoveries, projects, and scientific discussions. The purpose of the application is to create a place where users can publish scientific content, discuss topics, and organize publications by categories.

## Main features

The application allows users to:

- Create an account
- Log in and log out
- Create scientific publications
- Edit and delete own publications
- Search publications by keywords
- Organize publications using categories
- Comment on publications and participate in discussions
- View user profiles and user publications

## Technologies used

- Python
- Flask
- SQLite
- HTML
- Jinja templates

## Database

The application uses an SQLite database with tables for:

- Users
- Publications
- Comments
- Categories
- Publication categories

## How to run the application

1. Clone the repository:
git clone <repository-url>


2. Create and activate a virtual environment:
python3 -m venv venv
source venv/bin/activate


3. Install dependencies:
pip install flask


4. Start the application:
python app.py


5. Open the application in a browser:
http://127.0.0.1:5000/


## Testing

A tester can:

1. Register a new user account.
2. Log in with the account.
3. Create a scientific publication.
4. Add categories to the publication.
5. Edit or delete own publications.
6. Search publications.
7. Comment on publications.
8. View user profiles.

## Future improvements

Possible future improvements:

- Password hashing for improved security
- More advanced user profiles
- Additional scientific categories
- Improved user interface design

