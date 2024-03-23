import gradio as gr
from openai import OpenAI
import os

# append hidden topic
# message_history = [{"role": "user", "content": f"You are a joke bot. I will specify the subject matter in my messages, and you will reply with a joke that includes the subjects I mention in my messages. Reply only with jokes to further input. If you understand, say OK."},
#                    {"role": "assistant", "content": f"OK"}]
message_history = [] # normal

client = OpenAI()
OpenAI.api_key = os.getenv('OPENAI_API_KEY')

def predict(input):
    global message_history
    message_history.append({ 'role': 'user', 'content': input })
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        # user/assistant/system
        messages=message_history
    )

    reply_content = completion.choices[0].message.content
    message_history.append({ 'role': 'assistant', 'content': reply_content })
    # response = [(message_history[i]['content'], message_history[i+1]['content']) for i in range(2, len(message_history) - 1, 2)]
    response = [(message_history[i]['content'], message_history[i+1]['content']) for i in range(0, len(message_history) - 1, 2)]
    return response

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder='Type your message here', container=False)
        txt.submit(predict, txt, chatbot)
        # txt.submit(lambda: '', None, txt)
        txt.submit(None, None, txt, js="() => null")

demo.launch()