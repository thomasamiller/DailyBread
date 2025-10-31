import requests
from bs4 import BeautifulSoup
import re
from string import digits

# Define the Bible Gateway base URL
base_url = "https://www.biblegateway.com/passage/?search="
has_display_url = False
is_hard_code_verse = True
selected_reference = "Romans 15:13"
testament = "new"

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

    return field_reference

def get_reference():
    return input("Enter a Bible reference (e.g., John 3:16): ").strip()

def reference_url(reference):
    return reference.replace(" ", "+")

def get_testament():
    # Prompt the user for the Testament
    return input("Is the reference from the Old Testament or New Testament? ").strip().lower()

def validate_testament():
    if testament not in ["old", "new", "nt", "ot", "old testament", "new testament"]:
        print("Invalid input. Please specify 'old / Old Testament / ot' or 'new / New Testament / nt'.")
        exit()

def extract_reference():
    if is_hard_code_verse:
        print("testament and reference hard coded at the moment")

    # Prompt the user for the Bible reference
    #if not is_hard_code_verse:
        #testament = get_testament()
        #reference = get_reference()

    # Define the versions for each Testament or CUVMPT
    new_testament_versions = ["NIV", "NGU-DE", "NEG1979", "NVI", "UBG", "JLB", "KLB", "CUVMPS "]
    old_testament_versions = ["NIV", "SCH2000", "SG21", "NVI", "UBG", "JLB", "KLB", "CUVMPS "]

    # Determine which versions to use
    versions = new_testament_versions if testament in ["new", "new testament", "nt"] else old_testament_versions

    # Open a page for each version
    for version in versions:
        search_reference = reference_url(selected_reference)

        url = f"{base_url}{search_reference}&version={version}"
        if has_display_url:
            print("url=" + url)
        # Make an HTTP GET request to fetch the page content
        response = requests.get(url)
        
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            print_reference = get_reference_text(soup, url)
            #print_reference = "<b><a href='" + url + "'>" +  print_reference + "</a></b>"
            print(print_reference)

            field_reference = format_reference_for_field(selected_reference)

            verse = ""
            for ref in field_reference:
                verse = verse + get_verse_content(ref, soup)

            verse = verse.strip()
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
            if not parent_name == "h3" and not parent_name == "h4" :
                # replace <br> with space

                new_lines = verseContent.findAll("br")
                for lines in new_lines:
                    lines.replaceWith(" ")
                verse_numbers = verseContent.findAll("sup")
                for numbers in verse_numbers:
                    numbers.replaceWith("")
                #handle the Lord in the text <span style="font-variant: small-caps" class="small-caps">Herr</span> GErman, English, SPanish
                verse = verse + str(verseContent.get_text(strip=False))
                # remove square brackets and contents (link to cross reference)
                verse = re.sub('\[.*?]', " ", verse)
                # remove brackets and contents (cross reference)
                verse = re.sub("[(\[].*?[)\]]", " ", verse)
                # remove leading digits
                verse = verse.lstrip(digits) + " "
    verse = verse.lstrip(digits)

    verse = verse.replace("—", " —")
    verse = re.sub('([.,!?()])', r'\1 ', verse)
    verse = re.sub('([.,!?()] ["\'])', '', verse)
    # remove double spaces
    verse = re.sub('\s{2,}', ' ', verse)


    return verse


def get_reference_text(soup, url):
    # Find the element containing the passage reference
    dropdown_text = soup.find("div", class_="dropdown-display-text")
    if dropdown_text:
        dropdown_text = dropdown_text.get_text(strip=True)
        #uncomment to print the reference without hyperlink
        #print(dropdown_text)

        return dropdown_text
    else:
        print("Reference not found: " + url)
        #https://www.bible.com/bible/132/MAT.1.PBG or https://www.bible.com/bible/137/MAT.1.PLNT

def get_book_short_name(book_name):
    bible_books = open("C:\\Users\\thoma\PycharmProjects\extract_bible\src\\verse_extractor\\bibleBooksMatch.txt", "r")
    short_name = ""

    for references in bible_books:
        if bool(short_name):
            break
        #print("references=" + references)
        book = references.split("=", 1)[0]
        if book_name == book:
            short_name = references.split("=", 1)[1]

    bible_books.close()
    # remove the new line character from the reference
    short_name = short_name[:-1]

    return short_name

if __name__ == "__main__":
    extract_reference()

    #handle case in Japanese when multiple verses shown together 詩篇 23:2-3 not 詩篇 23:2 as expected Ps-23-2-Ps-23-3