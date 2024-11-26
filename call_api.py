import os
import requests

def download_nt_xml_files(docID, mss):
    """
    Downloads XML files for New Testament books based on the provided docID and manuscript folder.

    Parameters:
    docID (str): The document ID for the API request.
    mss (str): The subfolder where files will be saved.
    """
    
    # List of New Testament books
    books = [
        "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians", 
        "Ephesians", "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy", 
        "2 Timothy", "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John", 
        "3 John", "Jude", "Revelation"
    ]
    
    # Base URL of the API with docID as a variable input
    base_url = f"https://ntvmr.uni-muenster.de/community/vmr/api/transcript/get/?docID={docID}&indexContent={{}}&fullPage=true&format=teiraw"
    
    # Specify the subfolder where you want to save the files
    subfolder = f"xml files/{mss}"  # Adjust to your desired folder structure
    os.makedirs(subfolder, exist_ok=True)  # Create the folder if it doesn't exist
    
    for book in books:
        # Format the book name to replace spaces with %20
        formatted_book = book.replace(" ", "%20")
        
        # Format the URL with the current book
        url = base_url.format(formatted_book)
        
        # Send GET request to the API
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Create file path in the specified subfolder
            file_name = os.path.join(subfolder, f"{book.replace(' ', '_')}_{mss}.xml")
            
            # Save the content to an XML file for each book
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"File saved successfully as '{file_name}'")
        else:
            print(f"Failed to retrieve data for {book}. Status code: {response.status_code}")

# Example usage:
# download_nt_xml_files(docID="20001", mss="manuscript123")
