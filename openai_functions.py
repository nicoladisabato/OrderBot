import openai
import json
from my_openai_key import openai_api_key
import db_helper

openai.api_key = openai_api_key


def generate_menu(input_list):
    menu = {}
    
    for item, category in input_list:
        if category in menu:
            menu[category].append(item)
        else:
            menu[category] = [item]
    
    output = ""
    for category, items in menu.items():
        output += f"{category}: {', '.join(items)}.\n"
    
    return output.strip()


input_list = db_helper.get_products_for_initial_prompt()

menu_output = generate_menu(input_list)
beer_list = db_helper.get_beers({
        'product_name': ""
    })

# Content of the initial message prompt, describing the role and tasks of a pizzeria server in Italy, along with menu items and restrictions.
messages = [
    {"role": "system", 
    "content": "Restaurant server. Take orders, assist with the following menu choices. Offer only items from menu, no inventions beyond this menu." 
    + menu_output + 
    """ \n Beer list:"""
    + beer_list + 
    """ . Respond with relevant and funny emojii always. Menu: Alcoholic beers incl. details: beer name, country, style, Alc %, IBU (higher -> bitter, lower -> sweater). Example: [('PUNK IPA', 'Scotland', 'India pale ale (ipa)', 5.6, 35)] -> [(name, country, style, Alc %, IBU)]. Offer only listed in the menu. items. GF means gluten free. If the name doesn't contain GF, the item contains gluten."""
    }]
print(messages)

def get_answer(question):
    question = question+("\n Response 200 chars: generate short reply. No non-food Qs allowed.") #not always necessary
    messages.append({'role': 'user', 'content': question})
    functions = [
        {
            "name": "get_product_from_menu",
            "description": """Retrieve menu items which the customer can eat. Perfect funcion for procuct recommendation or if the customers has a specific request. Customer orders, known product name yields full info, known product type yields all of that type, no name or type specified, return all menu items. 
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "The name of the products on the menu of the restaurant.",
                    },
                    "product_type": {
                        "type": "string",
                        "description": "The type of the products on the menu of the restaurant.",
                        "enum": ["pizza", "drink"]
                    },
                },
                "required": [],
            },
        },
        {
            "name": "get_price",
            "description": """Retrieve user-specified item price. Implicit type, EUR. -1 = no DB record found. 
            You must activate this function only if the user asks explicitly the price. 
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "The name of a specific product within the menu of the restaurant.",
                    },
                },
                "required": ["product_name"],
            },
        },
        {
            "name": "get_ingredients_and_description",
            "description": """Return ingredients of a specific user-specified product. Use product name as parameter (from menu). -1 return means no record in database.
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "The name of a specific product within the menu of the restaurant.",
                    },
                },
                "required": ["product_name"],
            },
        },

{
            "name": "check_availability",
            "description": """Check product availability (0: unavailable, 1: available).
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "The name of a specific product within the menu of the restaurant.",
                    },
                },
                "required": ["product_name"],
            },
        },
        {
            "name": "get_beers",
            "description": """"Get list of beers to the user, as advice, for ordering or for proposals. Implicit types. 
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "beer_name": {
                        "type": "string",
                        "description": "The name of a specific beer included in the menu restaurant.",
                    },
                },
                "required": [],
            },
        },
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions=functions,
        function_call="auto",  
    )
    response_message = response["choices"][0]["message"]

    if response_message.get("function_call"):

        available_functions = {
            'get_product_from_menu': db_helper.get_menu,
            "get_price": db_helper.get_price,
            "get_ingredients_and_description": db_helper.get_ingredients_and_description,
            #'place_order': db_helper.place_an_order, #not implemented yet
            'check_availability': db_helper.check_availability,
            'get_beers': db_helper.get_beers
        }

        function_name = response_message["function_call"]["name"]
        print(function_name)
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        print(function_args)
        function_response = fuction_to_call(function_args)
        print(function_response)


        messages.append(response_message)
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": str(function_response),
            }
        )


        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            temperature=0,
            #max_tokens=256,
        )  # get a new response from GPT where it can see the function response

        messages.append({"role": "assistant", "content": second_response["choices"][0]["message"]["content"]})
        print(second_response["usage"])

        return second_response["choices"][0]["message"]["content"]
    else:
        messages.append({"role": "assistant", "content": response_message["content"]})
        print(response["usage"])
        print(messages)
        return response_message["content"]



if __name__ == '__main__':
    print(get_answer("How much is pizza margherita?"))
    #print(type(beer_list))
