import unittest
from src.verse_extractor.extractBibleVersesRef import reference_url
from src.verse_extractor.extractBibleVersesRef import format_reference_for_field

class ExtractBibleVerseTest(unittest.TestCase):
    #https://www.geeksforgeeks.org/how-to-compare-two-text-files-in-python/
    def test_format_reference(self):
        self.assertEqual(format_reference_for_field("2 Corinthians 12:9"), "2Cor-12-9")
        self.assertEqual(format_reference_for_field("Exodus 28:2-3"), "Exod-28-3")
        self.assertEqual(format_reference_for_field("1 Chronicles 22:5"), "1Chr-22-5")
        self.assertEqual(format_reference_for_field("Psalm 121:2"), "Psal-121-2")
        self.assertEqual(format_reference_for_field("Psalm 90:14"), "Psal-90-14")
        self.assertEqual(format_reference_for_field("Psalm 20:7"), "Psal-20-7")
        self.assertEqual(format_reference_for_field("John 8:12"), "John-8-12")
        self.assertEqual(format_reference_for_field("Isaiah 65:25"), "Isa-65-25")
        self.assertEqual(format_reference_for_field("Isaiah 42:9"), "Isa-42-9")
        self.assertEqual(format_reference_for_field("Isaiah 5:8"), "Isa-5-8")
        self.assertEqual(format_reference_for_field("Colossians 1:17"), "Colo-1-17")
        self.assertEqual(format_reference_for_field("1 Timothy 2:1-2"), "1Tim-2-2")
        self.assertEqual(format_reference_for_field("1 Thessalonians 5:16-18"), ["1The-5-16", "1The-5-17", "1The-5-18"])
        get_book_short_name(self)

#check if 4 chars only for books with number
    def test_reference_url(self):
        self.assertEqual(self.get_url("2 Corinthians 12:9"), "2+Corinthians+12:9")
        self.assertEqual(reference_url("Exodus 28:2-3"), "Exodus+28:2-3")
        self.assertEqual(reference_url("1 Chronicles 22:5"), "1+Chronicles+22:5")
        self.assertEqual(reference_url("Psalm 121:2"), "Psalm+121:2")
        self.assertEqual(reference_url("Psalm 90:14"), "Psalm+90:14")
        self.assertEqual(reference_url("Psalm 20:7"), "Psalm+20:7")
        self.assertEqual(reference_url("John 8:12"), "John+8:12")
        self.assertEqual(reference_url("Isaiah 65:25"), "Isaiah+65:25")
        self.assertEqual(reference_url("Isaiah 42:9"), "Isaiah+42:9")
        self.assertEqual(reference_url("Isaiah 5:8"), "Isaiah+5:8")
        self.assertEqual(reference_url("Colossians 1:17"), "Colossians+1:17")
        self.assertEqual(reference_url("1 Timothy 2:1-2"), "1+Timothy+2:1-2")
        self.assertEqual(reference_url("1 Thessalonians 5:16-18"), "1+Thessalonians+5:16-18")

    def get_url(self, reference):
        return reference_url(reference)

def get_book_short_name(self):
    bible_books = open("../bibleBooksList.txt", "r")

    for reference in bible_books:
        search_reference = reference_url(reference)
        url = f"{"https://www.biblegateway.com/passage/?search="}{search_reference}"
        print("url=" + url)
        ref = reference.split("=", 1)[0]
        output = reference.split("=", 1)[1]
        self.assertEqual(format_reference_for_field(ref), output)

#input Porque yo soy elSeñortu Dios, que sostiene tu mano derecha; yo soy quien te dice: “No temas, yo te ayudaré”.
#output Porque yo soy el Señor tu Dios, que sostiene tu mano derecha; yo soy quien te dice: “No temas, yo te ayudaré”.
#remove double spaces
if __name__ == "__main__":
    unittest.main()
