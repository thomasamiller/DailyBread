from pathlib import Path
import json

from src.polish_bible.polish_bible_rest_client import PolishBibleRestClient


BASE_DIR = Path(__file__).parent
MAPPING_PATH = BASE_DIR / "mapping.json"

class PolishBible:
    def __get_polish_name_and_abbreviation(self, english_abbr):

        with open(MAPPING_PATH, "r", encoding="utf-8") as f:
            mappings = json.load(f)

        for entry in mappings:
            if entry["english_name"].lower() == english_abbr.lower():
                return [entry["polish_abbr"], entry["polish_name"]]

        return None

    def parse_reference(self, selected_reference: str) -> dict:
        # Split the book name from the rest (e.g., "Psalm 119:105" → ["Psalm", "119:105"])
        parts = selected_reference.split(" ", 2)
        if(len(parts) > 2):
            parts[0] = parts[0] + " " + parts[1]
            parts[1] = parts[2]
            del parts[2]
        book = parts[0]
        chapter_and_verse = parts[1]

        # Split chapter and verse (e.g., "119:105" → ["119", "105"])
        chapter, verse = chapter_and_verse.split(":")

        # Check if the verse contains a range
        multiple = "-" in verse

        book = self.__get_polish_name_and_abbreviation(book)

        return {
            "book": book[0],
            "chapter": chapter,
            "verse": verse,
            "multiple": multiple,
            "book_name": book[1]
        }

    def __get_verses_from_rest_api(self, reference: dict[str, str | bool]) -> str:
        bible_client = PolishBibleRestClient()
        return bible_client.get_verse(reference["book"], reference["chapter"], reference["verse"])

    def print_verses(self, reference: dict[str, str|bool]):
        verses = self.__get_verses_from_rest_api(reference)
        line = " ".join(verses).replace("/", "")
        line = line[0].upper() + line[1:]

        print(reference["book_name"] + " " + reference["chapter"] + ":" + reference["verse"])
        print(line)