import requests
from bs4 import BeautifulSoup
import re
from string import digits

# Prompt the user for the Testament
#testament = input("Is the reference from the Old Testament or New Testament? ").strip().lower()
#testament = "new"
testament = "old"

# Define the versions for each Testament
new_testament_versions = ["NIV", "NGU-DE", "NEG1979", "NVI", "JLB", "KLB"]
old_testament_versions = ["NIV", "SCH2000", "SG21", "NVI", "JLB", "KLB"]

# Define the Bible Gateway base URL
base_url = "https://www.biblegateway.com/passage/?search="

# Validate input
if testament not in ["old", "new", "nt", "ot", "old testament", "new testament"]:
    print("Invalid input. Please specify 'old / Old Testament / ot' or 'new / New Testament / nt'.")
else:
    # Prompt the user for the Bible reference
    reference = input("Enter a Bible reference (e.g., John 3:16): ").strip()
    #reference = "John 3:16" reference = "Exodus 28:2-3"
    #reference = "Proverbs 16:9"
    formatted_reference = reference.replace(" ", "+")
    #if refence is a range of verses with -, take the last number, e.g. Exodus 28:2-3
    if "-" in reference:
        leftText = reference.split(":",1)[0]
        rightText = formatted_reference.split("-",1)[1]
        search_reference = leftText + ":" + rightText
        #get the book name
    search_reference = reference.replace(" ", "-")
    search_reference = search_reference.replace(":", "-")
    print("search_reference " + search_reference)
    #search_reference = "Exod-28-3"
    #search_reference = "Prov-16-9"
    # for Exodus 28:2-3 expect Exod-28-3 for the text ID

    # Determine which versions to use
    versions = new_testament_versions if testament in ["new", "new testament", "nt"] else old_testament_versions

    # Open a page for each version
    for version in versions:
        url = f"{base_url}{formatted_reference}&version={version}"
        print(url)
        # Make an HTTP GET request to fetch the page content
        response = requests.get(url)
        
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the element containing the passge
            dropdown_text = soup.find("div", class_="dropdown-display-text")
            
            if dropdown_text:
                print(dropdown_text.get_text(strip=True))
            else:
                print("Reference not found.")

            # Find the element with the verse text 
            verse_text = soup.find("span", class_="text " + str(search_reference))
            #add loop as in English there are often multiple spans that have the text split up

            if verse_text:
                verse = str(verse_text.get_text(strip=True))
                # remove square brackets and contents (link to cross reference)
                verse = re.sub('[\[].*?[\]]', "", verse)
                # remove brackets and contents (cross reference)
                verse = re.sub("[(\[].*?[)\]]", " ", verse)
                # remove leading digits
                verse = verse.lstrip(digits) + "\n"
                print(verse)
            else:
                print("Verse not found.")
        else:
            print(f"Failed to fetch the page. Status code: {response.status_code}")

