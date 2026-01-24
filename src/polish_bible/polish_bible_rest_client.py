import requests
import json

class PolishBibleRestClient:
    BASE_URL = "https://www.biblia.info.pl/api/biblia"

    def __init__(self, bible="bt"):
        """
        bible – translation abbreviation (e.g. bt, ubg, bw)
        """
        self.bible = bible

    def get_verse(self, book: str, chapter: int, verses: str):
        """
        Fetches verse text from the API.

        book    – book abbreviation, e.g. 'mat', 'rom', 'ps'
        chapter – chapter number
        verses  – verse or range, e.g. '5', '1-5', '7a-9', '12[*2]'
        """
        url = f"{self.BASE_URL}/{self.bible}/{book}/{chapter}/{verses}?escape=false"

        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"API error: HTTP {response.status_code}")

        data = response.json()

        # Return a list of texts for individual verses
        return [v["text"].replace("  ", " ") for v in data.get("verses", [])]