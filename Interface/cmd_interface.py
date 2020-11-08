import requests as rq


# set item dictionaries for making choices meaningful
pizza_dic = {}
def set_pizza_dic():
    id = 1
    response = rq.get('http://localhost:5000/pizza/pizza_menu')
    menu = response.json()
    for pizza in menu:
        pizza_dic[str(id)] = pizza['name']
        id += 1

drink_dic = {}
def set_drink_dic():
    id = 1
    response = rq.get('http://localhost:5000/pizza/drink_menu')
    menu = response.json()
    for drink in menu:
        drink_dic[str(id)] = drink['name']
        id += 1

topping_dic = {}
def set_topping_dic():
    id = 1
    response = rq.get('http://localhost:5000/pizza/topping_menu')
    menu = response.json()
    for topping in menu:
        topping_dic[str(id)] = topping['name']
        id += 1


def main():
    set_topping_dic()
    set_pizza_dic()
    set_drink_dic()

    order = {}
    order_number = 'none'

    print('Welcome to Pizza Parlour!\nWe\'re happy to have you here.')
    print('*'*64)
    while(True):
        print('1. Pizza menu')
        print('2. Drinks menu')
        print('3. Topping menu')
        print('4. Add order')
        print('5. Edit order')
        print('6. Cancel order')
        print('7. Delivery')
        print('8. Exit')
        choice = input('Select your the number of your choice: ')
        print('\n')
        if choice == '1':
            response = rq.get('http://localhost:5000/pizza/pizza_menu')
            menu = response.json()
            for pizza in menu:
                print(f"Type: {pizza['name']}\n\tPrice:\n\tMedium: {pizza['price']['medium']}\n\tLarge: {pizza['price']['large']}")
                print(f"\tDescription: {pizza['method_of_prepration']}")
                print('\n')

        elif choice == '2':
            response = rq.get('http://localhost:5000/pizza/drink_menu')
            menu = response.json()
            for drink in menu:
                print(f"Type: {drink['name']}\n\tPrice: {drink['price']}")
                print('\n')

        elif choice == '3':
            response = rq.get('http://localhost:5000/pizza/topping_menu')
            menu = response.json()
            for topping in menu:
                print(f"Type: {topping['name']}\n\tPrice: {topping['price']}")
                print('\n')

        elif choice == '4':
            print('You are now in the ordering section!')
            while(True):
                print('1. Add Pizza')
                print('2. Add drink')
                print('3. Add topping')
                print('4. Clear order (Warning: all the chosen items will be lost)')
                print('5. Show order')
                print('6. Submit order')

                order_choice = input('Enter your choice: ')
                print('\n')
                if order_choice == '1':
                    while(True):
                        for key in pizza_dic:
                            print(f'{key}: {pizza_dic[key]}\n')
                        print(f'{0}: Exit')
                        pizza_add = input("Add Pizza by entering it's number: ")
                        if pizza_add != str(0):
                            if pizza_dic[pizza_add] in order:
                                order[pizza_dic[pizza_add]] += 1
                            else:
                                order[pizza_dic[pizza_add]] = 1
                            print('Added to item!\n')
                        if pizza_add == str(0):
                            break

                if order_choice == '2':
                    while(True):
                        for key in drink_dic:
                            print(f'{key}: {drink_dic[key]}\n')
                        print(f'{0}: Exit')
                        drink_add = input("Add drink by entering it's number: ")
                        if drink_add != str(0):
                            if drink_dic[drink_add] in order:
                                order[drink_dic[drink_add]] += 1
                            else:
                                order[drink_dic[drink_add]] = 1
                            print('Added to order!\n')
                        if drink_add == str(0):
                            break

                if order_choice == '3':
                    while(True):
                        for key in topping_dic:
                            print(f'{key}: {topping_dic[key]}\n')
                        print(f'{0}: Exit')
                        topping_add = input("Add topping by entering it's number: ")
                        if topping_add != str(0):
                            if topping_dic[topping_add] in order:
                                order[topping_dic[topping_add]] += 1
                            else:
                                order[topping_dic[topping_add]] = 1
                            print('Added to order!\n')
                        if topping_add == str(0):
                            break
                if order_choice == '4':
                    order = {}
                if order_choice == '5':
                    for key in order:
                        print(f'{key}: {order[key]}')
                if order_choice == '6':
                    response = rq.post('http://localhost:5000/pizza/orders', json = order)
                    req_data = response.json()
                    order_number = req_data['order_number']
                    order['order_number'] = req_data['order_number']
                    print(f'Your order has been submitted!\nYour order number is: {order_number}')
                    break

        elif choice == '5':
            order = {'order_number': order_number}
            print('Your order has been cleared!')
            print('Select from menus again')
            print('You are now in the editing section!')
            while(True):
                print('1. Edit Pizza')
                print('2. Edit drink')
                print('3. Edit topping')
                print('4. Clear order (Warning: all the chosen items will be lost)')
                print('5. Show order')
                print('6. Submit order')

                order_choice = input('Enter your choice: ')
                print('\n')
                if order_choice == '1':
                    while(True):
                        for key in pizza_dic:
                            print(f'{key}: {pizza_dic[key]}\n')
                        print(f'{0}: Exit')
                        pizza_add = input("Add Pizza by entering it's number: ")
                        if pizza_add != str(0):
                            if pizza_dic[pizza_add] in order:
                                order[pizza_dic[pizza_add]] += 1
                            else:
                                order[pizza_dic[pizza_add]] = 1
                            print('Added to item!\n')
                        if pizza_add == str(0):
                            break

                if order_choice == '2':
                    while(True):
                        for key in drink_dic:
                            print(f'{key}: {drink_dic[key]}\n')
                        print(f'{0}: Exit')
                        drink_add = input("Add drink by entering it's number: ")
                        if drink_add != str(0):
                            if drink_dic[drink_add] in order:
                                order[drink_dic[drink_add]] += 1
                            else:
                                order[drink_dic[drink_add]] = 1
                            print('Added to order!\n')
                        if drink_add == str(0):
                            break

                if order_choice == '3':
                    while(True):
                        for key in topping_dic:
                            print(f'{key}: {topping_dic[key]}\n')
                        print(f'{0}: Exit')
                        topping_add = input("Add topping by entering it's number: ")
                        if topping_add != str(0):
                            if topping_dic[topping_add] in order:
                                order[topping_dic[topping_add]] += 1
                            else:
                                order[topping_dic[topping_add]] = 1
                            print('Added to order!\n')
                        if topping_add == str(0):
                            break
                if order_choice == '4':
                    order = {}
                if order_choice == '5':
                    for key in order:
                        print(f'{key}: {order[key]}')
                if order_choice == '6':
                    print(order)
                    response = rq.post(f'http://localhost:5000/pizza/orders/{order_number}', json = order)
                    req_data = response.json()
                    order_number = req_data['order_number']
                    print(req_data)
                    print('Your order has been edited!')
                    break
                else:
                    continue
        elif choice == '6':
            print(order_number)
            response = rq.get(f'http://localhost:5000/pizza/orders/{order_number}?cancel=true')
            print('Your order was deleted!')
        elif choice == '7':
            print('We have 3 ways to deliver you this order:\n1. in-house delivery\n2. Uber Eats\n3. Foodora')
            delivery_choice = input('Enter the number of your choice delivery: ')
            if delivery_choice == '1':
                response = rq.get(f'http://localhost:5000/pizza/deliveries?order_number={order_number}&service=in-house')
                print('You chose Pizza Parlour\'s in-house delivey')
            if delivery_choice == '2':
                print('You chose Uber')
                response == rq.get(f'http://localhost:5000/pizza/deliveries?order_number={order_number}&service=Uber')
            if delivery_choice == '3':
                print('You chose Foodora')
                response == rq.get(f'http://localhost:5000/pizza/deliveries?order_number={order_number}&service=Foodora')
        else:
            continue

if __name__ == '__main__':
    main()
