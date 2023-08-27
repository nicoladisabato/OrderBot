import chainlit as cl
import openai_functions

@cl.on_chat_start
async def start():
    await cl.Message(author="Chatbot", content="""Welcome to OrderBot! The server chatbot in your restaurant. ✍️📋

- Order: Order what you want 🛒
- Get advice: The chatbot will recommend dishes based on your tastes, allergies or intolerances! 💬
                     
What you want to eat?                  """).send()

@cl.on_message
async def main(message: str):
   # Your custom logic goes here…
   answer = openai_functions.get_answer(message)
   # Send a response back to the user
   await cl.Message(author="Chatbot",
     content=answer,
   ).send()