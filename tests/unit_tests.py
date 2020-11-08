from PizzaParlour import app
from PizzaParlour import set_drink_prices
from PizzaParlour import set_pizza_prices
from PizzaParlour import set_topping_prices
from PizzaParlour import pizza_types
from PizzaParlour import drinks
from PizzaParlour import toppings
from PizzaParlour import order_count
from PizzaParlour import orders
import os

def test_pizza():
    response = app.test_client().get('/pizza')
    # response2 = app.test_client().get('/harbor')

    assert response.status_code == 200
    assert response.data == b'Welcome to Pizza parlour!'
    # assert response2.data == 2

def test_pizza_types():
    #response = app.test_client().get('/pizza/pizza_menu')
    for item in pizza_types:
        response = app.test_client().get(f'/pizza/pizza_menu?name={item["name"]}')
        data = response.get_json()
        assert response.status_code == 200
        assert data['name'] == item['name']

    set_pizza_prices()
    response = app.test_client().get(f'/pizza/pizza_menu?name=Pepperoni')
    data = response.get_json()
    assert data['name'] == 'Pepperoni'

    response = app.test_client().get(f'/pizza/pizza_menu')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == len(pizza_types)

def test_get_pizza_price():
    response = app.test_client().get(f'/pizza/pizza_menu/Pepperoni?size=medium')
    data = response.get_json()
    assert response.status_code == 200
    assert float(data) == 3.50

    response = app.test_client().get(f'/pizza/pizza_menu/Pepperoni?size=large')
    data = response.get_json()
    assert response.status_code == 200
    assert float(data) == 6.40

    response = app.test_client().get(f'/pizza/pizza_menu/Pepperoni')
    data = response.get_json()
    assert response.status_code == 200
    assert data == {'medium': 3.50, 'large': 6.40}


def test_drinks():
    for item in drinks:
        response = app.test_client().get(f'/pizza/drink_menu?name={item["name"]}')
        data = response.get_json()
        assert response.status_code == 200
        assert not response.data == b'not found'
        assert response.get_json()
        assert data['name'] == item['name']

    set_pizza_prices()
    response = app.test_client().get(f'/pizza/drink_menu?name=Cock')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Cock'

    response = app.test_client().get(f'/pizza/drink_menu')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == len(drinks)

def test_get_drink_price():
    response = app.test_client().get(f'/pizza/drink_menu/Diet Cock')
    data = response.get_json()
    assert response.status_code == 200
    assert float(data) == 3.00

def test_toppings():
    for item in toppings:
        response = app.test_client().get(f'/pizza/topping_menu?name={item["name"]}')
        data = response.get_json()
        assert response.status_code == 200
        assert data['name'] == item['name']

    set_topping_prices()
    response = app.test_client().get(f'/pizza/topping_menu?name=mushrooms')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'mushrooms'

    response = app.test_client().get(f'/pizza/topping_menu')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == len(toppings)

def test_get_topping_price():
    response = app.test_client().get(f'/pizza/topping_menu/mushrooms')
    data = response.get_json()
    assert response.status_code == 200
    assert float(data) == 5.20

def test_set_pizza_prices():
    assert set_pizza_prices() == True
    assert set_pizza_prices('prices/pizza_prices_undefined.txt') == False

def test_set_drink_prices():
    assert set_drink_prices() == True
    assert set_drink_prices('prices/drink_prices_undefined.txt') == False

def test_set_topping_prices():
    assert set_topping_prices() == True
    assert set_topping_prices('prices/topping_prices_undefined.txt') == False

def test_add_order():
    request_json = {
        'Cock': 2,
        'mushrooms': 2,
        'Pepperoni': 2
    }
    response = app.test_client().post('/pizza/orders', json = request_json)
    data = response.get_json()
    assert response.status_code == 200
    assert not data['order_number'] == 1001
    # assert not response.data == 'bad request'
    # assert data['Cock'] == 2

def test_update_order():
    request_json = {
        'Cock': 2,
        'mushrooms': 2,
        'Pepperoni': 2,
        'order_number': 1000
    }

    response = app.test_client().post('/pizza/orders/1000', json = request_json)
    data = response.get_json()
    assert response.status_code == 200
    assert data['Cock'] == 2

    response = app.test_client().get('/pizza/orders/1001')
    assert response.status_code == 200
    data = response.get_json()
    assert data == {'order_number': 1001, 'Margherita': 2, 'Juice': 4}

    response = app.test_client().get('/pizza/orders/1001?cancel=true')
    data = response.data
    assert data == b'Order Deleted!'

def test_get_delivery():

    response = app.test_client().get('/pizza/delivery/1000')
    data = response.get_json()
    assert response.status_code == 200
    assert data == {'order_number': 1000, 'delivery': 'Uber', 'items': {'Pepperoni': 2, 'Water': 4}}

def test_delivery_add():
    #{'order_number': 1000, 'Pepperoni': 2, 'Water': 4}
    response = app.test_client().get('/pizza/deliveries?order_number=1000&service=Uber')
    data = response.get_json()
    assert response.status_code == 200
