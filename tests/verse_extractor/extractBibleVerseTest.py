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

    def test_strip_the_lord(self):
        markup = '<p class="verse"><span class="text Ps-27-1"><sup class="versenum">1&nbsp;</sup><i>Von David.</i></span></p>'
        markup += '<p class="verse"><span class="text Ps-27-1">Der <span style="font-variant: small-caps" class="small-caps">Herr</span> ist mein Licht und mein Heil,<br>vor wem sollte ich mich fürchten?<br>Der <span style="font-variant: small-caps" class="small-caps">Herr</span> ist meines Lebens Kraft,<br>vor wem sollte mir grauen?</span></p>'
        expected = "Von David. Der Herr ist mein Licht und mein Heil, vor wem sollte ich mich fürchten? Der Herr ist meines Lebens Kraft, vor wem sollte mir grauen?"

        self.assert_soup(markup, expected, "Ps-27-1")

    def test_strip_heading(self):
        #if parent is a heading, ignore the line <h3><span class="text Rev-11-15" id="en-NIV-30889">The Seventh Trumpet</span></h3>
        markup = '<h3><span class="text Rev-11-15" id="en-NIV-30889">The Seventh Trumpet</span></h3>'
        self.assert_soup(markup, "", "Rev-11-15")

    def test_strip_cross_references(self):
        markup = '<span class="text Rev-11-15"><sup class="versenum">15 </sup>The seventh angel sounded his trumpet,<sup class="crossreference" ...ference B"&gt;B&lt;/a&gt;)\'>(<a href="#cen-NIV-30889B" title="See cross-reference B">B</a>)</sup> in heaven, which said:</span>'
        markup += '<span class="text Rev-11-15">“The kingdom of the world has become</span>'
        markup += '<span class="text Rev-11-15">the kingdom of our Lord and of his Messiah,<sup class="crossreference" data-cr="#cen-NIV-30889C" ...9C" title="See cross-reference C"&gt;C&lt;/a&gt;)\'>(<a href="#cen-NIV-30889C" title="See cross-reference C">C</a>)</sup></span>'
        markup += '<span class="text Rev-11-15">and he will reign for ever and ever.”<sup class="crossreference" data-cr="#cen-NIV-30889D" data-l...9D" title="See cross-reference D"&gt;D&lt;/a&gt;)\'>(<a href="#cen-NIV-30889D" title="See cross-reference D">D</a>)</sup></span>'

        expected = 'The seventh angel sounded his trumpet, in heaven, which said: “The kingdom of the world has become the kingdom of our Lord and of his Messiah, and he will reign for ever and ever. ”'

        self.assert_soup(markup, expected, "Rev-11-15")

    def test_replace_br_with_space(self):
        # missing space after Hilfe Psalmen 146:5 Wohl dem, dessen Hilfeder Gott Jakobs ist,dessen Hoffnung ruht auf dem Herrn, seinem Gott!

        markup = '<span id="de-SCH2000-16416" class="text Ps-146-5"><sup class="versenum">5&nbsp;</sup>Wohl dem, dessen Hilfe<br>der Gott Jakobs ist,<br>dessen Hoffnung ruht auf dem <span style="font-variant: small-caps" class="small-caps">Herrn</span>, seinem Gott!</span>'
        expected = 'Wohl dem, dessen Hilfe der Gott Jakobs ist, dessen Hoffnung ruht auf dem Herrn, seinem Gott!'
        self.assert_soup(markup, expected, "Ps-146-5")

    def test_delete_chapter(self):
        # chapter not deleted: Salmos 46:1-2 Al director musical. De los hijos de Coré. Canción según alamot. 46 Dios es nuestro refugio y nuestra fortaleza, nuestra segura ayuda en momentos de angustia.Por eso, no temeremos aunque se desmorone la tierra y las montañas se hundan en el fondo del mar;

        markup = '<p class="line"><span class="chapter-2"><span class="text Ps-46-1"><span class="chapternum">46&nbsp;</span>Dios es nuestro refugio y nuestra fortaleza,</span></span><br><span class="indent-1"><span class="indent-1-breaks">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="text Ps-46-1">nuestra segura ayuda en momentos de angustia.</span></span><br><span id="es-NVI-14617" class="text Ps-46-2"><sup class="versenum">2&nbsp;</sup>Por eso, no temeremos</span><br><span class="indent-1"><span class="indent-1-breaks">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="text Ps-46-2">aunque se desmorone la tierra</span></span><br><span class="indent-1"><span class="indent-1-breaks">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="text Ps-46-2">y las montañas se hundan en el fondo del mar;</span></span></p>'
        expected = 'Dios es nuestro refugio y nuestra fortaleza, nuestra segura ayuda en momentos de angustia.'
        self.assert_soup(markup, expected, "Ps-46-1")

    def test_delete_chapter_space_hyphens(self):
        # Psalm 27:1 Of David. 1TheLordis my light and my salvation — whom shall I fear? TheLordis the stronghold of my life— of whom shall I be afraid?
        markup = '<p class="line"><span class="text Ps-27-1"><sup class="versenum">1&nbsp;</sup>The <span style="font-variant: small-caps" class="small-caps">Lord</span> is my light<sup class="crossreference" data-cr="#cen-NIV-14287A" data-link="(<a href=&quot;#cen-NIV-14287A&quot; title=&quot;See cross-reference A&quot;>A</a>)">(<a href="#cen-NIV-14287A" title="See cross-reference A">A</a>)</sup> and my salvation<sup class="crossreference" data-cr="#cen-NIV-14287B" data-link="(<a href=&quot;#cen-NIV-14287B&quot; title=&quot;See cross-reference B&quot;>B</a>)">(<a href="#cen-NIV-14287B" title="See cross-reference B">B</a>)</sup>—</span><br><span class="indent-1"><span class="indent-1-breaks">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="text Ps-27-1">whom shall I fear?</span></span><br><span class="text Ps-27-1">The <span style="font-variant: small-caps" class="small-caps">Lord</span> is the stronghold<sup class="crossreference" data-cr="#cen-NIV-14287C" data-link="(<a href=&quot;#cen-NIV-14287C&quot; title=&quot;See cross-reference C&quot;>C</a>)">(<a href="#cen-NIV-14287C" title="See cross-reference C">C</a>)</sup> of my life—</span><br><span class="indent-1"><span class="indent-1-breaks">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="text Ps-27-1">of whom shall I be afraid?<sup class="crossreference" data-cr="#cen-NIV-14287D" data-link="(<a href=&quot;#cen-NIV-14287D&quot; title=&quot;See cross-reference D&quot;>D</a>)">(<a href="#cen-NIV-14287D" title="See cross-reference D">D</a>)</sup></span></span></p>'

        expected = "The Lord is my light and my salvation — whom shall I fear? The Lord is the stronghold of my life — of whom shall I be afraid?"
        self.assert_soup(markup, expected, "Ps-27-1")

    def assert_soup(self, markup, expected, verse):
        soup = BeautifulSoup(markup, 'html.parser')
        actual = get_verse_content(verse, soup)
        actual = actual.strip()
        self.assertEqual(expected, actual)
#Genesis 23:2 - Japanese not found: <span class="text Gen-23-1-Gen-23-2"><span class="chapternum">23&nbsp;</span><sup class="versenum">1-2&nbsp;</sup>さて、サラはカナンの地ヘブロンにいた時、百二十七歳で死にました。アブラハムが嘆き悲しんだことは言うまでもありません。 </span>
#Genesis 7:7,23 handle an extra verse
#Mark 12:44 - Japanese not found: <span id="ja-JLB-21925" class="text Mark-12-43-Mark-12-44"><sup class="versenum">43-44&nbsp;</sup>それをごらんになったイエスは、弟子たちを呼び寄せて、こう言われました。「あの貧しい未亡人は、どの金持ちよりも、はるかに多く投げ入れたのです。金持ちはあり余る中からほんの少しばかりささげたのに、この女は、乏しい中から持っている全部をささげたのですから。」</span>
if __name__ == "__main__":
    unittest.main()