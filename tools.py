import requests
from tool2schema import EnableTool


@EnableTool
def search_gutenberg_books(search_terms: list[str]):
    """
    Searches for books in the Project Gutenberg library.

    Args:
        search_terms (list[str]): A list of search keywords.  Can include author names,
            book titles, or other relevant terms. For example, ['dickens', 'great'] will
            search for books containing both 'dickens' and 'great', which might return
            Dickens' "Great Expectations". Multiple keywords are joined with spaces to form the search query.

    Returns:
        list[dict]: A list of simplified search results, where each book contains 'id', 'title', and 'authors' information.

    Example:
        >>> search_gutenberg_books(['dickens', 'twist'])
        [{'id': 730, 'title': 'Oliver Twist', 'authors': [{'name': 'Charles Dickens', ...}]}]
    """
    search_query = " ".join(search_terms)
    url = "https://gutendex.com/books"
    response = requests.get(url, params={"search": search_query})

    simplified_results = []
    for book in response.json().get("results", []):
        simplified_results.append(
            {
                "id": book.get("id"),
                "title": book.get("title"),
                "authors": book.get("authors"),
            }
        )

    return simplified_results
