from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
import os

# This hides those annoying TensorFlow info logs to keep your terminal clean
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

# 1. Initialize the FastAPI app
app = FastAPI(title="TechGear Local AI Agent", description="An offline RAG API")

# 2. Define what an incoming request should look like
class UserQuery(BaseModel):
    question: str

print("Booting up the AI Brain... Please wait.")

# 3. Load the Database and Model (We do this outside the endpoint so it only loads once)
loader = TextLoader("faq.txt")
docs = loader.load()
splits = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(docs)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory="./local_db")

llm = OllamaLLM(model="llama3.2")
prompt = ChatPromptTemplate.from_template("""
You are a helpful customer support agent. Answer the question based ONLY on the following context. 
If the answer is not in the context, say "I do not know."

Context:
{context}

Question: {input}
""")

document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(vectorstore.as_retriever(), document_chain)

print("AI is awake and ready to accept API requests!")

# 4. Create the API Endpoint
@app.post("/ask")
async def ask_question(query: UserQuery):
    # When a request comes in, send the question to our local AI
    response = retrieval_chain.invoke({"input": query.question})
    
    # Return the answer as clean JSON
    return {
        "status": "success",
        "question": query.question,
        "answer": response['answer']
    }