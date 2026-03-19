from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import CHROMA_PATH, embeddings

def get_or_create_vector_store(domain_name: str):
    """
    Obtiene la base de datos vectorial existente o la crea si no existe.
    """
    collection_name = f"{domain_name}_collection"
    
    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH
    )
    
    if len(vector_store.get()['ids']) == 0:
        print(f"--- ⚙️ Indexando documentos nuevos para: {domain_name} ---")
        
        loader = DirectoryLoader(
            f"./data/{domain_name}_docs", 
            glob="**/*.md", 
            loader_cls=UnstructuredMarkdownLoader
        )
        docs = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True
        )
        chunks = text_splitter.split_documents(docs)
        
        vector_store.add_documents(documents=chunks)
        print(f"✅ Dominio '{domain_name}' indexado con {len(chunks)} fragmentos.\n")
    else:
        print(f"⚡ Base de datos local cargada al instante para: {domain_name}")

    return vector_store

booking_db = get_or_create_vector_store("booking")
logistics_db = get_or_create_vector_store("logistics")
marketing_db = get_or_create_vector_store("marketing")