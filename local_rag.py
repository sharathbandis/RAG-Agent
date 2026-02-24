from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

print("1. Loading document...")
loader = TextLoader("faq.txt")
docs = loader.load()

print("2. Splitting text...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = text_splitter.split_documents(docs)

print("3. Creating local embeddings and database (this might take a few seconds on the first run)...")
# This downloads a tiny, open-source embedding model directly to your machine
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory="./local_db")
retriever = vectorstore.as_retriever()

print("4. Connecting to local Llama 3.2 model...")
# This connects to the Ollama engine running on your computer
llm = OllamaLLM(model="llama3.2")

print("5. Building the AI brain...")
prompt = ChatPromptTemplate.from_template("""
You are a helpful customer support agent. Answer the question based ONLY on the following context. 
If the answer is not in the context, say "I do not know."

Context:
{context}

Question: {input}
""")

document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)

print("\n--- Testing the Local AI Agent ---")
user_question = "What happens if I return a laptop that I already opened?"
print(f"Question: {user_question}")

# Run it!
response = retrieval_chain.invoke({"input": user_question})
print(f"\nAnswer: {response['answer']}")