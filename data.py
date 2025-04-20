from supabase import create_client, Client

SUPABASE_URL = "https://qnqnurfuzqhdinkleyql.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFucW51cmZ1enFoZGlua2xleXFsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ4MDY5NTIsImV4cCI6MjA2MDM4Mjk1Mn0.wwfjKKpAvpDlF-L_casEnumlgEfwMd8Se5uyrRHmHu0"


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


db = "booksdata"


def add_book(title: str, author: str, email: str):
    """Insert a new book entry."""
    response = supabase.table(db).insert({
        "title": title,
        "author": author,
        "progress": 0,
        "status": "reading",
        "user_email": email
    }).execute()

    if response.status_code != 201:
        return {"error": "Failed to add book"}

    return response.data[0]["id"]


def update_progress(title: str, email: str, progress: int):
    """Update progress for a given book using title and email."""
    response = supabase.table(db).update({
        "progress": progress
    }).eq("title", title).eq("user_email", email).execute()
    return response.data


def get_books_by_user(email: str):
    """Fetch all books associated with the given user's email."""
    response = supabase.table(db).select("*").eq("user_email", email).execute()


    return response.data



def fetch_user_books(email: str):
    """Prints the user's books and their progress."""
    books = get_books_by_user(email)
    if isinstance(books, dict) and books.get("error"):
        print(f"Error fetching books: {books['error']}")
        return

    return books


# ---------------------- MAIN TEST ----------------------
fetch_user_books("jash@gmail.com")
