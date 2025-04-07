from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from src.prompt import system_prompt

from langchain_pinecone import PineconeVectorStore
import langchain_groq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from dotenv import load_dotenv
from src.prompt import*
import os


app = Flask(__name__)

load_dotenv()
# Get them once
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')


embeddings = download_hugging_face_embeddings()

index_name = "medbot"

vector_store = PineconeVectorStore.from_existing_index(index_name=index_name,embedding=embeddings)

retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5,"k":4}
)


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

prompt = ChatPromptTemplate.from_messages(
  [
    ("system",system_prompt),
    ("human", "{input}"),
  ]
)

question_answer_chain = create_stuff_documents_chain(llm,prompt)
rag_chain = create_retrieval_chain(retriever , question_answer_chain)

@app.route("/")
def index():
  return render_template('chat.html')

@app.route("/get", methods=["GET","POST"])
def chat():
  msg = request.form["msg"]
  input = msg
  print(input)
  response = rag_chain.invoke({"input":msg})
  print("Response : ",response["answer"])
  return str(response["answer"])

if __name__ == "__main__":
    app.run(debug=True)