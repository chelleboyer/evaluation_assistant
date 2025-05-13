import os
from aimakerspace.text_utils import CharacterTextSplitter, TextFileLoader, PDFLoader
from bs4 import BeautifulSoup

def extract_text_from_html(html_content):
    """Extract text content from HTML."""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        
        # Get text
        text = soup.get_text()
        
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return html_content  # Return original content in case of error

def load_documents():
    """Process all files in the data folder"""
    data_folder = "data"
    
    # Check if folder exists
    if not os.path.exists(data_folder):
        return []
            
    # Get list of files in the folder
    files = [f for f in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder, f))]
    
    if not files:
        return []
    
    # Process each file
    documents = []
    
    # Process each file
    for filename in files:
        file_path = os.path.join(data_folder, filename)
        print(f"Processing file: {file_path}")
        
        try:
            # Read the file content directly
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Check if it's HTML and extract text if so
            if filename.lower().endswith('.html') or content.strip().startswith('<!DOCTYPE html>') or content.strip().startswith('<html'):
                print(f"Detected HTML content in {filename}, extracting text...")
                content = extract_text_from_html(content)
            
            # Print sample document content for debugging
            print(f"File: {filename}, Content length: {len(content)}")
            print(f"Sample content (first 200 chars): {content[:200]}")
            
            # Add to documents list
            documents.append(content)
           
        except Exception as e:
            print(f"Error processing file {filename}: {str(e)}. Skipping.")
            continue
 
    return documents

def split_documents(documents):  
    text_splitter = CharacterTextSplitter()
    try:      
        texts = text_splitter.split_texts(documents)      
    except Exception as e:
        print(f"Error split_documents: {str(e)}.")
        return []
    
    return texts 