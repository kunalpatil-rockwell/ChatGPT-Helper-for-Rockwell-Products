from langchain.chat_models import ChatOpenAI
from langchain.vectorstores.base import VectorStoreRetriever
from langchain.chains import ConversationalRetrievalChain
import pickle

def load_retriever():
    with open("Powerflex755T.pkl", "rb") as f:
        vectorstore = pickle.load(f)
    retriever = VectorStoreRetriever(vectorstore=vectorstore)
    return retriever

def query_data(user_query,chat_history):
    #Get the retriever for our vectorstore
    retriever = load_retriever()

    # Create conversation chain that uses our vectordb as retriver, this also allows for chat history management
    qa = ConversationalRetrievalChain.from_llm(ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"), retriever.vectorstore.as_retriever(), return_source_documents=True)

    result = qa({"question": user_query, "chat_history": chat_history})
    return result
