import requests
from bs4 import BeautifulSoup
import re
from string import digits

# Define the Bible Gateway base URL
base_url = "https://www.biblegateway.com/passage/?search="

def format_reference_for_field(reference):
    #if reference is a range of verses with -, take the last verse number, e.g. Exodus 28:2-3
    #process verse by verse in a loop
    is_multiple = reference.find("-") >= 0
    verses = []

    if is_multiple:
        # convention Exodus 28:2-3: start verse between : and -
        colon_location = reference.find(":")
        hyphen_location = reference.find("-")
        start_verse = int(reference[colon_location+1:hyphen_location])
        end_verse = int(reference.split("-")[1])
        counter = start_verse
        while counter in range(end_verse):
            verses.append(counter)
            counter = counter+1
        verses.append(end_verse)

    # split on space and check if the first result is numeric (e.g. 2 Kings) then add second split
    book = reference.split(" ", 1)[0]
    chapter_verse = reference.split(" ", 1)[1]
    if book.isnumeric():
        book = book + " " + reference.split(" ", 2)[1]
        chapter_verse = reference.split(" ", 2)[2]
    elif book == "Song":
        book = "Songs"
        chapter_verse = reference.rsplit(" ", 1) [1]

    #get book short name for field
    short_name = get_book_short_name(book)
    if is_multiple:
        base_reference = short_name + "-" + chapter_verse.split(":")[0]
        field_reference = []
        for ref in verses:
            field_reference.append(base_reference + "-" + str(ref))
    else:
        chapter_verse = chapter_verse.replace(" ", "-")
        chapter_verse = chapter_verse.replace(":", "-")
        field_reference = [short_name + "-" + chapter_verse]


    #return search_reference

    return field_reference

def get_reference():
    #return input("Enter a Bible reference (e.g., John 3:16): ").strip()
    print("testament and reference hard coded at the moment")
    return "1 Peter 3:15"

def reference_url(reference):
    return reference.replace(" ", "+")

def get_testament():
    # Prompt the user for the Testament
    #return input("Is the reference from the Old Testament or New Testament? ").strip().lower()
    return "new"

def validate_testament(testament):
    if testament not in ["old", "new", "nt", "ot", "old testament", "new testament"]:
        print("Invalid input. Please specify 'old / Old Testament / ot' or 'new / New Testament / nt'.")
        exit()

def extract_reference():
    testament = get_testament()

    # Prompt the user for the Bible reference
    reference = get_reference()

    # Define the versions for each Testament or CUVMPT
    new_testament_versions = ["NIV", "NGU-DE", "NEG1979", "NVI", "JLB", "KLB", "CUVMPS "]
    old_testament_versions = ["NIV", "SCH2000", "SG21", "NVI", "JLB", "KLB", "CUVMPS "]

    # Determine which versions to use
    versions = new_testament_versions if testament in ["new", "new testament", "nt"] else old_testament_versions

    # Open a page for each version
    for version in versions:
        search_reference = reference_url(reference)
        url = f"{base_url}{search_reference}&version={version}"
        #print("url=" + url)
        # Make an HTTP GET request to fetch the page content
        response = requests.get(url)
        
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            get_reference_text(soup)

            field_reference = format_reference_for_field(reference)

            verse = ""
            for ref in field_reference:
                verse = verse + get_verse_content(ref, soup)

            print(verse + "\n")
        else:
            print(f"Failed to fetch the page. Status code: {response.status_code}")


def get_verse_content(search_reference, soup):
    # Find the element with the verse text
    # add loop as in English there are often multiple spans that have the text split up
    # in Japanese we might have multiple verses together: text Matt-16-2-Matt-16-3
    verse = ""
    for verseContent in soup.find_all("span", class_="text " + str(search_reference)):
        if not verseContent:
            print("Verse not found.")
        else:
            parent_name = verseContent.parent.name
            # remove title from the text e.g. Revelation 11:15 <h3><span class="text Rev-11-15" id="en-NIV-30889">The Seventh Trumpet</span></h3>
            if not parent_name == "h3" :
                #handle the Lord in the text <span style="font-variant: small-caps" class="small-caps">Herr</span> GErman, English, SPanish
                verse = verse + str(verseContent.get_text(strip=True))
                # remove square brackets and contents (link to cross reference)
                verse = re.sub('\[.*?[]]', "", verse)
                # remove brackets and contents (cross reference)
                verse = re.sub("[(\[].*?[)\]]", " ", verse)
                # remove leading digits
                verse = verse.lstrip(digits) + " "
    verse = verse.lstrip(digits)
    # remove double spaces
    verse = verse.replace("  ", " ")
    #insert spaces around this text <span style="font-variant: small-caps" class="small-caps">Gott</span>
    #insert spaces around this text <span class="text Isa-30-15">«C'est dans le retour à moi<sup data-fn="#ffr-SG21-18301a" class="footnote" data-link="[<a href=&quot;#ffr-SG21-18301a&quot; title=&quot;See footnote a&quot;>a</a>]">[<a href="#ffr-SG21-18301a" title="See footnote a">a</a>]</sup> et le repos que sera votre salut,</span>

    return verse


def get_reference_text(soup):
    # Find the element containing the passage reference
    dropdown_text = soup.find("div", class_="dropdown-display-text")
    if dropdown_text:
        print(dropdown_text.get_text(strip=True))
    else:
        print("Reference not found.")

def get_book_short_name(book_name):
    bible_books = open("C:\\Users\\thoma\PycharmProjects\extract_bible\src\\verse_extractor\\bibleBooksMatch.txt", "r")
    short_name = ""

    for reference in bible_books:
        if bool(short_name):
            break
        #print("reference=" + reference)
        book = reference.split("=", 1)[0]
        if book_name == book:
            short_name = reference.split("=", 1)[1]
        #print("book=" + book + " short_name=" +short_name)
        #search_reference = get_url(reference)
        #url = f"{"https://www.biblegateway.com/passage/?search="}{search_reference}"
        #print("url=" + url)
        #ref = reference.split("=", 1)[0]
        #output = reference.split("=", 1)[1]
    bible_books.close()
    # remove the new line character from the reference
    short_name = short_name[:-1]

    return short_name

if __name__ == "__main__":
    extract_reference()

    #handle case in Japanese when multiple verses shown together 詩篇 23:2-3 not 詩篇 23:2 as expected Ps-23-2-Ps-23-3