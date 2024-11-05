import requests
import json
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


load_dotenv()

def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents

def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks

file_path = "./pdf__files/file.pdf"
extracted_data = load_pdf(file_path)
text_chunks = text_split(extracted_data)

VULTR_API_KEY = os.getenv("VULTR_API")
collection_id = "sentify"


VECTOR_STORE_ENDPOINT = f"https://api.vultrinference.com/v1/vector_store/{collection_id}/items"


headers = {
    "Authorization": f"Bearer {VULTR_API_KEY}",
    "Content-Type": "application/json"
}


for i, chunk in enumerate(text_chunks):
    payload = {
        "content": chunk.page_content, 
       
    }

    
    response = requests.post(VECTOR_STORE_ENDPOINT, headers=headers, data=json.dumps(payload))

   
    if response.status_code == 201:  
        print(f"Chunk {i+1} added successfully:", response.json())
    else:
        print(f"Error adding chunk {i+1}:", response.status_code, response.text)
