"""
english-polish names mapping file generator

Reads file with english books names and polish books names.
Merge them into mapping.json

        "english_name": "Daniel",
        "english_abbr": "Dan",
        "polish_name": "Księga Daniela",
        "polish_abbr": "dn"
"""

import json

def filter_by_second_element(collection):
    unique = []
    seen = set()

    for item in collection:
        key = item[1]
        if key not in seen:
            unique.append(item)
            seen.add(key)

    return unique

if __name__ == "__main__":
    with open("polish_books.json", "r", encoding="utf-8") as f:
        polish_books = json.load(f)

    with open("../verse_extractor/bibleBooksMatch.txt", "r", encoding="utf-8") as books:
        english_books = []
        for references in books:
            book = references.split("=", 1)
            book[1] = book[1][:-1]
            english_books.append(book)
        english_books = filter_by_second_element(english_books)

    result = []
    polish_abbr = []
    for polish_book in polish_books["books"]:
        polish_abbr.append(polish_book["abbreviation"])

    for polish_abbr_index, val in enumerate(polish_abbr):
        # print(polish_abbr[polish_abbr_index])
        # print(english_books[polish_abbr_index])
        row = [english_books[polish_abbr_index][0], english_books[polish_abbr_index][1], polish_books["books"][polish_abbr_index]["name"], polish_abbr[polish_abbr_index]]
        result.append(row)

    result_in_json = [
        {
            "english_name": w[0],
            "english_abbr": w[1],
            "polish_name": w[2],
            "polish_abbr": w[3]
        }
        for w in result
    ]

    with open("mapping.json", "w", encoding="utf-8") as f:
        json.dump(result_in_json, f, indent=4, ensure_ascii=False)

    print(json.dumps(result_in_json, indent=4, ensure_ascii=False))