from agno.agent import Agent
from agno.tools import tool
from agno.models.google import Gemini
import google.generativeai as genai
from custom_memory_manager import CustomMemoryManager
from data import add_book, update_progress, get_books_by_user, fetch_user_books
import requests

# -------------------- Gemini Model Setup --------------------
genai.configure(api_key='AIzaSyDhUe-DaKLru5R51KX4oG0cMUmxG4aBD8g')
ml=genai.GenerativeModel(model_name="gemini-1.5-pro")
model = Gemini(api_key="AIzaSyAVjuGthW9WvvR2ps5Zgr-Xs5aoe0kAVPQ", id="gemini-1.5-pro")

memory_manager = CustomMemoryManager()


def call_gemini(prompt: str) -> str:
    print(f"[Gemini Prompt] {prompt}")
    response = ml.generate_content(prompt)
    print(f"[Gemini Response] {response.text}")
    return response.text.strip()

@tool(name="Summarize_Book", description="Summarize the description of the book")
def summarize_book(book_title: str, author: str) -> str:
    if not book_title or not author:
        return "Book title and author are required for summarization."

    url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{book_title}+inauthor:{author}&maxResults=1"

    res = requests.get(url).json()
    if not res.get("items"):
        return "No book found with the given title and author."
    info = res["items"][0]["volumeInfo"]
    date = info.get("publishedDate", "Unknown")
    summary = call_gemini(f"Summarize this book {book_title}")
    return f"**Published:** {date}\n\n**Summary:**\n{summary}"




@tool(name="Recommend_Books", description="Recommend a list of books based on genre")
def recommend_books(genre: str) -> str:
    if not genre:
        return "Genre is required for recommendations."
    prompt = f"Suggest a list of 3 most fascinating books in {genre} "
    return call_gemini(prompt)

@tool(name="Save_Progress", description="Save reading progress for a book")
def save_progress(book_title: str, email: str, page_number: str) -> str:
    if not book_title or not email:
        return "Book title and email are required."
    book_id = add_book(book_title, "Unknown Author", email)
    update_progress(book_id, email, int(page_number))
    return f"Saved: {book_title} — Page {page_number}"

@tool(name="Remember_Books", description="Recall books saved in the system")
def remember_books(user_email: str) -> str:
    books = fetch_user_books(user_email)
    if not books:
        return "No saved books found."
    return "\n".join([f"{b['title']} - Page {b['progress']}" for b in books])

@tool(name="List_Finished_Books", description="List all books that are 100% complete")
def list_finished_books(user_email: str) -> str:
    books = get_books_by_user(user_email)
    if not books:
        return "No saved books found."
    finished = [b for b in books if b.get("progress", 0) == 100]
    return "\n".join([f"{b['title']} ✅" for b in finished]) or "No books marked as finished yet."


agent = Agent(
    tools=[summarize_book, recommend_books, save_progress, remember_books, list_finished_books],
    model=model,
    memory=memory_manager
)



