import os
import CreateChunks
import QueryData
from getpass import getpass

# Front end web app
import gradio as gr

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")
    chat_history = []


    def user(user_message, history):
        # Get response from QA chain
        response = QueryData.query_data(user_message, history)
        # Append user message and response to chat history
        history.append((user_message, response["answer"]))
        return gr.update(value=""), history


    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False)
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == '__main__':
    os.environ["OPENAI_API_KEY"] = getpass("Paste your OpenAI API key here and hit enter:")
    #CreateChunks.Create_Vector_Database()
    demo.launch(debug=True)

