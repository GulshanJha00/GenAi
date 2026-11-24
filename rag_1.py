from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq()

pdf_path = Path(__file__).parent / "nodejs.pdf"

loader = PyPDFLoader(
    file_path = pdf_path,
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(docs)


embeddings = OllamaEmbeddings(model="nomic-embed-text")


# doc_store = QdrantVectorStore.from_documents(
#     documents=[],
#     embedding=embeddings,
#     collection_name="my_documents",
#     url="http://localhost:6333",
# )

# doc_store.add_documents(documents=texts)
# print("Documents successfully stored in Qdrant!")

retriver = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name="my_documents",
    url="http://localhost:6333"
)
user_query = input(">")
result = retriver.similarity_search(
    query=user_query
)
context = "\n\n".join(
    [doc.page_content for doc in result]
)

SYSTEM_PROMPT = f"""
You are a helpful Node.js documentation assistant.

Answer the user's question using ONLY the
provided context.

If the answer is not available in the context,
clearly say that you don't have enough information.

Do not use your external knowledge.

CONTEXT:
{context}
"""
message = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    },
    {
        "role": "user",
        "content": user_query
    }
]

chat_completion = client.chat.completions.create(
        messages=message,
        model="openai/gpt-oss-120b",
)

parsed_res = chat_completion.choices[0].message.content

print(parsed_res)