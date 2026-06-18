from transformers import GPT2TokenizerFast
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import textract
import pickle

def Create_Vector_Database():
    # Step 1: Convert PDF to text
    doc = textract.process("./Data/Powerflex 755T Features.pdf")

    # Step 2: Save to .txt and reopen (helps prevent issues)
    with open('ExtractedTextFromPDF.txt', 'w', encoding="utf-8") as f:
        f.write(doc.decode('utf-8'))

    with open('ExtractedTextFromPDF.txt', 'r', encoding="utf-8") as f:
        text = f.read()

    # Step 3: Create function to count tokens
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

    def count_tokens(text: str) -> int:
        return len(tokenizer.encode(text))

    # Step 4: Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size = 1024,
        chunk_overlap  = 24,
        length_function = count_tokens,
    )

    chunks = text_splitter.create_documents([text])

    # Get embedding model
    embeddings = OpenAIEmbeddings()

    # Create vector database
    db = FAISS.from_documents(chunks, embeddings)

    with open("Powerflex755T.pkl", "wb") as f:
        pickle.dump(db, f)

