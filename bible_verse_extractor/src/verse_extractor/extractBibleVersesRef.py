import requests
from bs4 import BeautifulSoup
import re
from string import digits

# Define the Bible Gateway base URL
base_url = "https://www.biblegateway.com/passage/?search="


def format_reference_for_field(reference):
    #if reference is a range of verses with -, take the last verse number, e.g. Exodus 28:2-3
    #process verse by verse in a loop
    isMultiple = False
    if "-" in reference:
        leftText = reference.split(":",1)[0]
        rightText = reference.split("-",1)[1]
        reference = leftText + ":" + rightText
        isMultiple = True
    #get the book name
    book = reference.split(":", 1)[0]
    # remove second character if it is a space and get first 4 letters of the book for the class name for the reference
    # e.g. 1 John 1
    if reference.index(" ") == 1:
        bookNumber = reference.split(" ", 1)[0]
        book = reference.split(" ", 2)[1]
        replaceBook = bookNumber + " " + book
        bookSearch = bookNumber + book
        bookSearch = bookSearch[:4]
    elif reference.find("Psalm")  > -1:
        bookSearch = "Ps"
        replaceBook = "Psalm"
    else:
        replaceBook = reference.split(" ", 1)[0]
        bookSearch = replaceBook[:3]

    search_reference = reference.replace(replaceBook, bookSearch)
    search_reference = search_reference.replace(" ", "-")
    search_reference = search_reference.replace(":", "-")

    #return search_reference
    #return "Ps-23-2-Ps-23-3"
    #arr.append(8) arr.insert(6, 7) length = len(arr)
    return "Ps-30-6"

def get_reference():
    #return input("Enter a Bible reference (e.g., John 3:16): ").strip()
    print("testament and reference hard coded at the moment")
    return "Psalm 30:6"

def reference_url(reference):
    return reference.replace(" ", "+")

def get_testament():
    # Prompt the user for the Testament
    #return input("Is the reference from the Old Testament or New Testament? ").strip().lower()
    return "old"

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

            verse = get_verse_content(format_reference_for_field(reference), soup)
            print(verse)
        else:
            print(f"Failed to fetch the page. Status code: {response.status_code}")


def get_verse_content(search_reference, soup):
    # Find the element with the verse text
    # add loop as in English there are often multiple spans that have the text split up
    verse = ""
    for verseContent in soup.find_all("span", class_="text " + str(search_reference)):
        if verseContent:
            #handle the Lord in the text <span style="font-variant: small-caps" class="small-caps">Herr</span> GErman, English, SPanish
            verse = verse + str(verseContent.get_text(strip=True))
            # remove square brackets and contents (link to cross reference)
            verse = re.sub('[\[].*?[\]]', "", verse)
            # remove brackets and contents (cross reference)
            verse = re.sub("[(\[].*?[)\]]", " ", verse)
            # remove leading digits
            verse = verse.lstrip(digits) + " "
        else:
            print("Verse not found.")
    verse = verse.lstrip(digits) + "\n"
    #remove double spaces
    #remove title from the text e.g. Revelation 11:15 The Seventh Trumpet 15The seventh angel sounded his trumpet, and there were loud voices in heaven, which said: “The kingdom of the world has become the kingdom of our Lord and of his Messiah,  and he will reign for ever and ever.”
    #Offenbarung 11:15 Die siebte Posaune: Die Herrschaft Gottes und des Messias 15Nun blies der siebte Engel seine Posaune. Daraufhin erklang im Himmel ein mächtiger, vielstimmiger Jubelgesang: »Jetzt gehört die Herrschaft über die Welt ´endgültig` unserem Herrn und dem, den er als König eingesetzt hat – Christus. Ja, ´unser Herr` wird für immer und ewig regieren.«
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



if __name__ == "__main__":
    extract_reference()

    #handle case in Japanese when multiple verses shown together 詩篇 23:2-3 not 詩篇 23:2 as expected Ps-23-2-Ps-23-3