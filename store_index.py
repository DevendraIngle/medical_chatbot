from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from pinecone import Pinecone ,ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY not found. Make sure it's set in the .env file.")

extracted_data=load_pdf_file(data='Data/')

text_chunks=text_split(extracted_data)
embeddings = download_hugging_face_embeddings()

index_name = "medbot"
pc = Pinecone(api_key=PINECONE_API_KEY)
pc.create_index(
    name=index_name,
    dimension=384, # Replace with your model dimensions
    metric="cosine", # Replace with your model metric
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
)

vector_store = PineconeVectorStore.from_documents(documents = text_chunks,index_name=index_name,embedding=embeddings)