import mysql.connector
import json


def get_db_cursor():
    # open database connection
    db = mysql.connector.connect(
        host="localhost",
        user="-> insert here the username <-",
        password="-> insert here the password <-",
        database="restaurant_db"
    )

    # create a new cursor instance
    cursor = db.cursor()

    return db, cursor


def close_db_connection(db, cursor):
    # disconnect from server
    cursor.close()
    db.close()


def get_products_for_initial_prompt():
    """Get all the names of the products in the menu for the initial prompt message."""
    db, cursor = get_db_cursor()
    cursor.callproc('get_product_for_prompt')
    result = None
    for res in cursor.stored_results():
        result = (res.fetchall())  # Fetch the first column of the first row
    close_db_connection(db, cursor)
    return result


def get_menu(params):
    db, cursor = get_db_cursor()
    cursor.callproc('get_product_menu', [params.get('product_name', ''), params.get('product_type', '')])
    result = None
    for res in cursor.stored_results():
        result = str(res.fetchall())  # Fetch the first column of the first row
    close_db_connection(db, cursor)
    return result


def get_price(params):
    """Get the price of a specific product"""
    db, cursor = get_db_cursor()
    cursor.callproc('get_price', [params.get('product_name', '')])
    result = None
    for res in cursor.stored_results():
        result = float(res.fetchone()[0])  # Fetch the first column of the first row
    close_db_connection(db, cursor)
    return result


def get_ingredients_and_description(params):
    """Get informations like ingredients and description of a specific product"""
    db, cursor = get_db_cursor()
    cursor.callproc('get_ingredients_and_description', [params.get('product_name', '')])
    result = None
    for res in cursor.stored_results():
        result = str(res.fetchone())  # Fetch the first column of the first row
    close_db_connection(db, cursor)
    return result


def place_an_order(params):
    """Place an order by the user."""
    order_info = {
        "product": params.get('product', '')
    }
    converted_order = {valore: order_info.get("product").count(valore) for valore in order_info.get("product")} #dict
    return json.dumps(converted_order)


def check_availability(params):
    """Check availability of a specific product"""
    db, cursor = get_db_cursor()
    cursor.callproc('check_availability', [params.get('product_name', '')])
    result = None
    for res in cursor.stored_results():
        result = str(res.fetchone()[0])  # Fetch the first column of the first row
    close_db_connection(db, cursor)
    return result


def get_beers(params):
    db, cursor = get_db_cursor()
    cursor.callproc('get_beers', [params.get('product_name', '')])
    result = None
    for res in cursor.stored_results():
        result = str(res.fetchall())  # Fetch the first column of the first row
    close_db_connection(db, cursor)
    return result



if __name__ == "__main__":

    print(get_price({
        'product_name': "margherita"
    }))
    print(get_beers({
        'product_name': "punk ipa"
    }))

   
   