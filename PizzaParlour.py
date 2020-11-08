from flask import Flask, jsonify, request
import socket
import random
from collections import OrderedDict


pizza_types = [
    {
        'method_of_prepration': 'Pepperoni is made from a mixture of ground pork and beef mixed with spices and flavorings. Salt and sodium nitrate are then added as curing agents, which prevent the growth of unwanted microorganisms. Nitrate is also added, which gives pepperoni its color.',
        'name': 'Pepperoni',
        'price': {'medium': 0, 'large': 0}
    },
    {
        'method_of_prepration':  'Pizza Margherita is a typical Neapolitan pizza, made with San Marzano tomatoes, mozzarella cheese, fresh basil, salt and extra-virgin olive oil.',
        'name': 'Margherita',
        'price': {'medium': 0, 'large': 0}
    },
    {
        'method_of_prepration': 'Mushrooms, Garlic and Mint',
        'name': 'Vegetarian',
        'price': {'medium': 0, 'large': 0}
    },
    {
        'method_of_prepration': 'Neapolitan pizza also known as Naples-style pizza, is a style of pizza made with tomatoes and mozzarella cheese.',
        'name': 'Neapolitan',
        'price': {'medium': 0, 'large': 0}
    }
]

drinks = [
    {
        'name': 'Cock',
        'price': 0
    },
    {
        'name': 'Diet Cock',
        'price': 0
    },
    {
        'name': 'Cock Zero',
        'price': 0
    },
    {
        'name': 'Pepsi',
        'price': 0
    },
    {
        'name': 'Diet Pepsi',
        'price': 0
    },
    {
        'name': 'Dr. Pepper',
        'price': 0
    },
    {
        'name': 'Water',
        'price': 0
    },
    {
        'name': 'Juice',
        'price': 0
    }
]

toppings = [
    {
        'name' : 'olives',
        'price' : 0
    },
    {
        'name' : 'tomatoes',
        'price' : 0
    },
    {
        'name' : 'mushrooms',
        'price' : 0
    },
    {
        'name' : 'jalapenos',
        'price' : 0
    },
    {
        'name' : 'chicken',
        'price' : 0
    },
    {
        'name' : 'beef',
        'price' : 0
    },
    {
        'name' : 'pepperoni',
        'price' : 0
    }
]

orders = [{'order_number': 1000, 'Pepperoni': 2, 'Water': 4},
    {'order_number': 1001, 'Margherita': 2, 'Juice': 4}
]

deliveries = [{'order_number': 1000, 'delivery': 'Uber', 'items': {'Pepperoni': 2, 'Water': 4}}]

# reads drink prices from 'prices/drink_prices.txt'
def set_drink_prices(path = 'prices/drink_prices.txt'):
    try:
        file = open(path)
        while(True):
            line = file.readline()
            if not line:
                break
            line_split = line.split(',')
            for i in range(len(drinks)):
                if drinks[i]['name'] == line_split[0]:
                    drinks[i]['price'] = float(line_split[1])
    except:
        return False

    file.close()
    return True

# reads pizza prices from 'prices/pizza_prices.txt'
def set_pizza_prices(path='prices/pizza_prices.txt'):
    try:
        file = open(path)
        while(True):
            line = file.readline()
            if not line:
                break
            line_split = line.split(',')
            for i in range(len(pizza_types)):
                if pizza_types[i]['name'] == line_split[0]:
                    pizza_types[i]['price'] = {'medium': float(line_split[1]), 'large': float(line_split[2])}
    except:
        return False

    file.close()
    return True

# reads topping prices from 'prices/topping_prices.txt'
def set_topping_prices(path = 'prices/topping_prices.txt'):
    try:
        file = open(path)
        while(True):
            line = file.readline()
            if not line:
                break
            line_split = line.split(',')
            for i in range(len(toppings)):
                if toppings[i]['name'] == line_split[0]:
                    toppings[i]['price'] = float(line_split[1])
    except:
        return False

    file.close()
    return True

set_pizza_prices()
set_drink_prices()
set_topping_prices()

app = Flask("Assignment 2")
@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza parlour!'

# for getting pizza types. if 'name' argument is sent, return certain pizza type
@app.route('/pizza/pizza_menu')
def get_pizza_types():
    if request.args.get('name'):
        for item in pizza_types:
            if item['name'] == request.args.get('name'):
                return jsonify(item)
    return jsonify(pizza_types)

# return Pizza type for <name>
@app.route('/pizza/pizza_menu/<name>')
def get_pizza_price(name):
    if request.args.get('size'):
        for item in pizza_types:
            if request.args.get('size') == 'medium' and item['name'] == name:
                chosen_price = item['price']
                return jsonify(chosen_price['medium'])
            elif request.args.get('size') == 'large' and item['name'] == name:
                chosen_price = item['price']
                return jsonify(chosen_price['large'])

    for item in pizza_types:
        if item['name'] == name:
            chosen_price = item['price']
            return jsonify(chosen_price)


# return drinks, if 'name' specified, return certain drink
@app.route('/pizza/drink_menu')
def get_drinks():
    if request.args.get('name'):
        for item in drinks:
            if item['name'] == request.args.get('name'):
                return jsonify(item)
    return  jsonify(drinks)

# return drink type for <name>
@app.route('/pizza/drink_menu/<name>')
def get_drink_price(name):
    for item in drinks:
        if item['name'] == name:
            chosen_price = item['price']
            return jsonify(chosen_price)

# return toppings, if 'name' specified, return certain drink
@app.route('/pizza/topping_menu')
def get_toppings():
    if request.args.get('name'):
        for item in toppings:
            if item['name'] == request.args.get('name'):
                return jsonify(item)

    return jsonify(toppings)

# return topping type for <name>
@app.route('/pizza/topping_menu/<name>')
def get_topping_price(name):
    for item in toppings:
        if item['name'] == name:
            chosen_price = item['price']
            return jsonify(chosen_price)

# add order: receives json
@app.route('/pizza/orders', methods=['POST']) #GET requests will be blocked
def add_order():
    req_data = request.get_json()
    order_number = random.randrange(1000,9999)
    req_data['order_number'] = order_number
    orders.append(req_data)
    return jsonify(req_data)

# update order: receives json
@app.route('/pizza/orders/<orderNumber>', methods=['POST', 'GET'])
def update_order(orderNumber):
    order_index = -1
    if request.method == 'POST':
        for i in range(len(orders)):
            if orders[i]['order_number'] == int(orderNumber):
                order_index = i
                break

        update_json = request.get_json()
        orders[order_index] = update_json
        return jsonify(update_json)

    elif request.method == 'GET' and request.args.get('cancel'):
        if(request.args.get('cancel') == 'true'):
            for i in range(len(orders)):
                if orders[i]['order_number'] == int(orderNumber):
                    del orders[i]
                    return 'Order Deleted!'

    elif request.method == 'GET':
        for i in range(len(orders)):
            if orders[i]['order_number'] == int(orderNumber):
                return jsonify(orders[i])

# get delivery with <orderNumber>
@app.route('/pizza/delivery/<orderNumber>')
def get_delivery(orderNumber):
    for i in range(len(deliveries)):
        if deliveries[i]['order_number'] == int(orderNumber):
            return jsonify(deliveries[i])

# add delivery receives two arguments: 'order_number' and 'service'
@app.route('/pizza/deliveries')
def delivery_add():
    if request.args.get('order_number') and request.args.get('service'):
        delivery_json = {'order_number': int(request.args.get('order_number')), 'service': request.args.get('service')}

        for i in range(len(orders)):
            if orders[i]['order_number'] == delivery_json['order_number']:
                chosen_order = orders[i]
                for item in chosen_order:
                    if item != 'order_number':
                        delivery_json[item] = chosen_order[item]
        deliveries.append(delivery_json)
        return jsonify(delivery_json)

if __name__ == "__main__":
    app.run()

