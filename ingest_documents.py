from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import PDF_DIR, VECTORS_DIR, vector_store


def ingest_documents() -> None:
    #get names of all pdf files in the folder
    pdfs = sorted(PDF_DIR.glob("*.pdf"))

    pdf_loaders = []
    for pdf in pdfs:
        pdf_loaders.append(PyPDFLoader(str(pdf)))

    documents = []
    for loader in pdf_loaders:
        documents.extend(loader.load())

    #chunk text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )
    chunks = text_splitter.split_documents(documents)

    if not chunks:
        print(f"No PDFs found in {PDF_DIR}, nothing to ingest.")
        return

    #embed and persist vectors
    vector_store.add_documents(chunks)
    print(f"Ingested {len(chunks)} chunks from {len(pdfs)} PDFs into {VECTORS_DIR}")


if __name__ == "__main__":
    ingest_documents()
