import requests
import re
import os


def fetch_book_details(user_input):
    """Fetch book result from the API and parse the result"""
    # Validate input
    user_input = user_input.strip()

    # API url
    base_url = "https://openlibrary.org/search.json"

    # Make the API request
    try:
        response = requests.get(
            base_url, params={"q": user_input, "language": "eng", "limit": 1}
        )
        # Raises an error if the API is not responding
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"success": -1, "error": f"API request failed: {e}"}

    # Parse JSON response
    data = response.json()

    # Check for results
    if not data.get("docs"):
        return {"success": -2, "error": "No matching books found"}

    # get book results
    book = data["docs"][0]

    # parse book data
    title = book.get("title", "Unknown Title")
    authors = ", ".join(book.get("author_name", "Unknown Author")[:3])  # max 3
    isbn = book.get("isbn", "ISBN Not Found")[0]
    publish_date = book.get("first_publish_year", "Publish Date Not Found")
    first_sentence = book.get("first_sentence", "Unknown First Sentence")[0]
    subject = book.get("subject", [])

    # Find matching genres
    matching_genre = get_matching_genres(subject)

    # Get cover images
    cover_id = book.get("cover_i", None)
    cover_image_url = (
        f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
        if cover_id else ""
    )

    # store the url that will be the cached location
    if cover_id:
        cached_url = f"../static/book_covers/{cover_id}-M.jpg"
    else:
        cached_url = "../static/book_covers/placeholder.jpg"

    # Return book details
    return {
        "success": 0,
        "cover_image_url": cover_image_url,
        "cached_url": cached_url,
        "authors": authors,
        "title": title,
        "isbn": isbn,
        "publish_date": publish_date,
        "first_sentence": first_sentence,
        "subject": ", ".join(matching_genre),
    }


def validate_email(email):
    """Confirm an Email is a valid Imperial Email"""
    pattern = r"^[a-zA-Z0-9]+@ic\.ac\.uk$"
    return re.match(pattern, email) is not None


def save_img(url):
    """Save image to local filesystem for caching"""
    # return path to default image if no url
    if url == "":
        return "../static/book_covers/placeholder.jpg"  # default image

    # split url into parts
    parts = url.split("/")
    if len(parts) < 2:
        return url  # not properly formatted url

    # create file path for the book cover
    identifier = parts[-1]  # identifier for the img
    filepath = f"./static/book_covers/{identifier}"

    # early exit if file already exists in cache
    if os.path.exists(filepath):
        return f".{filepath}"  # img src needs extra .

    # fetch the cover image
    response = requests.get(url)

    # if failed, return the input url
    if response.status_code != 200:
        return url

    # if successful, write the image to cache
    if response.status_code == 200:
        with open(filepath, "wb") as output_file:
            output_file.write(response.content)

    return f".{filepath}"  # img src needs extra .


def update_cache(cover_urls):
    """Update the cache based on cover_urls from database"""
    # get directory
    dirname = "./static/book_covers/"
    directory = os.path.dirname(dirname)

    # get urls in list
    cached_urls = [fname for fname in os.listdir(directory)]
    cached_urls.remove("placeholder.jpg")  # don't remove the placeholder image
    required_urls = [fname for fname in cover_urls]

    # save each required url if not in cache, otherwise remove from cache list
    for file in required_urls:
        fname = file.split("/")[-1]

        if fname not in cached_urls:
            save_img(file)
        else:
            # if it is a jpg
            if fname.lower().endswith('.jpg'):
                cached_urls.remove(fname)

    # any items remaining in filenames are not needed
    for fname in cached_urls:
        if fname.lower().endswith('.jpg'):
            filepath = os.path.join(dirname, fname)
            os.remove(filepath)


def get_matching_genres(subject):
    """Filter for only matching genres from long list"""
    # List of all possible book genres
    predefined_genres = [
        "Fiction",
        "Fantasy",
        "Science Fiction",
        "Romance",
        "Thriller",
        "Crime",
        "Mystery",
        "Horror",
        "Biography",
        "History",
        "Self-Help",
        "Poetry",
        "Drama",
        "Young Adult",
    ]

    return [genre for genre in subject if genre in predefined_genres]
