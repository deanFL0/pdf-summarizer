from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import GoogleGenerativeAI
from pypdf import PdfReader

def process_text(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    knowledge_base = FAISS.from_texts(chunks, embeddings)

    return knowledge_base

def summarizer(pdf):
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""

        for page in pdf_reader.pages:
            text += page.extract_text(text) or ""

        knowledge_base = process_text(text)
        
        query = "Summarize the content of the document."

        if query:
            docs = knowledge_base.similarity_search(query)
            llm = GoogleGenerativeAI(model="gemini-1.5-flash")
            chain = load_qa_chain(llm, chain_type='stuff')
            response = chain.run(input_documents=docs, question=query)
            return response