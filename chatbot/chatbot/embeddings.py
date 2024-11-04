from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

# Extract data from the PDF
def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents


# Create text chunks
def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(extracted_data)

    return text_chunks


def embeddings_data():
    pdf_file = "finbert.pdf"

    extracted_data = load_pdf(pdf_file)

    text_chunks = text_split(extracted_data)

    text_list = [chunk.page_content for chunk in text_chunks]

    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    embeddings = model.encode(text_list)


    return text_chunks, embeddings



if _name_ == '_main_':
    print(embeddings_data()[0][1])