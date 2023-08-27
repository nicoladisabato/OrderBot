
# OrderBot 🍕🍽️
A GPT-based Chatbot for Food Ordering 🍽️ using data from MySQL DB and OpenAI Function Calling, through natural language.

<img width="1010" alt="orderbot_image" src="https://github.com/nicoladisabato/OrderBot/assets/45854469/09441058-892e-4535-9112-8f9c8905cd3e">


## Overview
OrderBot is an intelligent virtual server that can take input questions related to a mysql database and uses the power of artificial intelligence to understand users' prompts and propose suitable items to order, totally simulating the tasks of a server. 
Through an intuitive interface it is possible to ask for advice on products based on and to know any information relating to the menu.


## Main features
- Allows customers to order products using a LLM directly with their mysql database.
- Interact with the chatbot using natural language to order products and better understand the best product to order, based on your own data.
- AI-powered interaction: OrderBot uses advanced AI algorithms to take the correct data and generate a precise response.


## Getting started
1. Install all the dependencies using the command:
```bash
pip install -r requirements.txt
```

2. Clone the Orderbot repository to your local machine.
3. Run the script.sql in MySQL workbench
4. Specify the local db credentials inside the file db_helper.py
```bash
db = mysql.connector.connect(
        host="localhost",
        user="-> insert here the username <-",
        password="-> insert here the password <-",
        database="-> insert here your locale db name <-"
    )
``` 
5. Add your OpenAI API key inside the file my_openai_key.py
```bash
openai_api_key = "--> insert API key <--"
```    
6. Open the terminal and launch the following command:
```bash
chainlit run main.py -w
```

## Todo list
- Specify the functions that create the order instance and insert it into the Orders table
- Improve existing functions and their descriptions
- Improve the initial prompt
