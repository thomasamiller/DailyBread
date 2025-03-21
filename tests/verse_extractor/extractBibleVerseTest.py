import unittest

from bs4 import BeautifulSoup

from src.verse_extractor.extractBibleVersesRef import format_reference_for_field, get_book_short_name, reference_url, \
    get_verse_content


def get_url(reference):
    return reference_url(reference)


class ExtractBibleVerseTest(unittest.TestCase):
    #tests to add
    #header not removed & spaces not added: 2 Korinther 2:14 expected: Gott aber sei Dank! Weil wir mit Christus verbunden sind, lässt er uns immer in seinem Triumphzug mitziehen und macht durch uns an jedem Ort bekannt, wer er ist, sodass sich diese Erkenntnis wie ein wohlriechender Duft überallhin ausbreitet.
    #if Ps or Eccl, add in the verse afterwards in French and German
    #Isaiah 42:8 - German & English have theLord
    #Psalmen 119:71-72 missing space in German - missing space michals, no Japanese text Ps-119-71-Ps-119-72
    # Deuteronomy 2:7 missing space in English, German, & Spanish: TheLordyour denn derHerr elSeñorsu
    def test_format_reference(self):
        self.assertEqual(format_reference_for_field("2 Corinthians 12:9"), ["2Cor-12-9"])
        self.assertEqual(format_reference_for_field("Exodus 28:2-3"), ['Exod-28-2', "Exod-28-3"])
        self.assertEqual(format_reference_for_field("1 Chronicles 22:5"), ["1Chr-22-5"])
        self.assertEqual(format_reference_for_field("Psalm 121:2"), ["Ps-121-2"])
        self.assertEqual(format_reference_for_field("Psalm 90:14"), ["Ps-90-14"])
        self.assertEqual(format_reference_for_field("Psalm 20:7"), ["Ps-20-7"])
        self.assertEqual(format_reference_for_field("John 8:12"), ["John-8-12"])
        self.assertEqual(format_reference_for_field("Isaiah 65:25"), ["Isa-65-25"])
        self.assertEqual(format_reference_for_field("Isaiah 42:9"), ["Isa-42-9"])
        self.assertEqual(format_reference_for_field("Isaiah 5:8"), ["Isa-5-8"])
        self.assertEqual(format_reference_for_field("Colossians 1:17"), ["Col-1-17"])
        self.assertEqual(format_reference_for_field("1 Timothy 2:1-2"), ['1Tim-2-1', "1Tim-2-2"])

    def test_multiple_verses(self):
        self.assertEqual(format_reference_for_field("1 Thessalonians 5:16-18"), ["1Thess-5-16", "1Thess-5-17", "1Thess-5-18"])

    #check if 4 chars only for books with number
    def test_reference_url(self):
        self.assertEqual(get_url("2 Corinthians 12:9"), "2+Corinthians+12:9")
        self.assertEqual(get_url("Exodus 28:2-3"), "Exodus+28:2-3")
        self.assertEqual(get_url("1 Chronicles 22:5"), "1+Chronicles+22:5")
        self.assertEqual(get_url("Psalm 121:2"), "Psalm+121:2")
        self.assertEqual(get_url("Psalm 90:14"), "Psalm+90:14")
        self.assertEqual(get_url("Psalm 20:7"), "Psalm+20:7")
        self.assertEqual(get_url("John 8:12"), "John+8:12")
        self.assertEqual(get_url("Isaiah 65:25"), "Isaiah+65:25")
        self.assertEqual(get_url("Isaiah 42:9"), "Isaiah+42:9")
        self.assertEqual(get_url("Isaiah 5:8"), "Isaiah+5:8")
        self.assertEqual(get_url("Colossians 1:17"), "Colossians+1:17")
        self.assertEqual(get_url("1 Timothy 2:1-2"), "1+Timothy+2:1-2")
        self.assertEqual(get_url("1 Thessalonians 5:16-18"), "1+Thessalonians+5:16-18")

    def test_get_book_short_name(self):
        self.assertEqual(get_book_short_name("Genesis"), "Gen")
        self.assertEqual(get_book_short_name("2 Corinthians"), "2Cor")

    def test_all_books_short_name(self):
        self.assertEqual(format_reference_for_field("1 Samuel 1:1"), ["1Sam-1-1"])
        self.assertEqual(format_reference_for_field("Song of Solomon 1:1"), ["Song-1-1"])

        bible_books = open("C:\\Users\\thoma\PycharmProjects\extract_bible\\tests\\verse_extractor\\extract_bible_verse_test\\bibleBooksListAll.txt",
                           "r")
        for reference in bible_books:
            test_input = reference.split("=", 1)[0]
            test_expected = reference.split("=", 1)[1]
            #remove the new line character from the expected
            test_expected = [test_expected[:-1]]
            #print("testing input=" + test_input + " expected=" + test_expected)
            self.assertEqual(format_reference_for_field(test_input), test_expected)
        bible_books.close()

    def test_strip_extra_content(self):
        #if parent is a heading, ignore the line <h3><span class="text Rev-11-15" id="en-NIV-30889">The Seventh Trumpet</span></h3>
        markup = '<h3><span class="text Rev-11-15" id="en-NIV-30889">The Seventh Trumpet</span></h3>'
        self.assert_soup(markup, "")

        markup += '<span class="text Rev-11-15"><sup class="versenum">15 </sup>The seventh angel sounded his trumpet,<sup class="crossreference" ...ference B"&gt;B&lt;/a&gt;)\'>(<a href="#cen-NIV-30889B" title="See cross-reference B">B</a>)</sup> in heaven, which said:</span>'
        markup += '<span class="text Rev-11-15">“The kingdom of the world has become</span>'
        markup += '<span class="text Rev-11-15">the kingdom of our Lord and of his Messiah,<sup class="crossreference" data-cr="#cen-NIV-30889C" ...9C" title="See cross-reference C"&gt;C&lt;/a&gt;)\'>(<a href="#cen-NIV-30889C" title="See cross-reference C">C</a>)</sup></span>'
        markup += '<span class="text Rev-11-15">and he will reign for ever and ever.”<sup class="crossreference" data-cr="#cen-NIV-30889D" data-l...9D" title="See cross-reference D"&gt;D&lt;/a&gt;)\'>(<a href="#cen-NIV-30889D" title="See cross-reference D">D</a>)</sup></span>'

        expected = 'The seventh angel sounded his trumpet, in heaven, which said: “The kingdom of the world has become the kingdom of our Lord and of his Messiah, and he will reign for ever and ever.” '

        self.assert_soup(markup, expected)

    def assert_soup(self, markup, expected):
        soup = BeautifulSoup(markup, 'html.parser')
        actual = get_verse_content("Rev-11-15", soup)
        self.assertEqual(actual, expected)


#input Porque yo soy elSeñortu Dios, que sostiene tu mano derecha; yo soy quien te dice: “No temas, yo te ayudaré”.
#output Porque yo soy el Señor tu Dios, que sostiene tu mano derecha; yo soy quien te dice: “No temas, yo te ayudaré”.
# Mark 8:22-25 contains the heading & first verse number
#missing space between sentences 1 Petrus 3:15
#Ehrt vielmehr Christus, den Herrn, indem ihr ihm von ganzem Herzen vertraut.Und seid jederzeit bereit, jedem Rede und Antwort zu stehen, der euch auffordert, Auskunft über die Hoffnung zu geben, die euch erfüllt.
if __name__ == "__main__":
    unittest.main()
