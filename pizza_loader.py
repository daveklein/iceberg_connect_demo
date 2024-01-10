import random
import uuid
import json

from confluent_kafka import Producer
from datetime import datetime

pizza_topic = 'completed-pizzas'

def gen_orders():
    pizza_producer = Producer("bootstrap.servers": "localhost:29092")
    while True:
        i = random.randint(1, 5)
        pizza_order = random_pizzas(i)
        for p in pizza_order:
            pizza_producer.produce(pizza_topic, key=p.order_id, value=p.toJSON())
        pizza_producer.flush()
        print(f"Produced {i} pizzas to pizzas topic.")

class Pizza:
    def __init__(self, order_id, store_id, sauce, cheese, meats, veggies):
        self.order_id = order_id
        self.store_id = store_id
        self.sauce = sauce
        self.cheese = cheese
        self.meats = meats
        self.veggies = veggies
        self.date_ordered = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                        sort_keys=False, indent=4)
    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                        sort_keys=False, indent=4)
    
def calc_sauce():
    i = random.randint(0, 3)
    sauces = ['extra', 'bbq', 'light', 'alfredo']
    return sauces[i]

def calc_cheese():
    i = random.randint(0, 3)
    cheeses = ['extra', 'none', 'three cheese', 'goat cheese']
    return cheeses[i]

def calc_meats():
    i = random.randint(0, 4)
    meats = ['pepperoni', 'sausage', 'ham', 'anchovies', 'salami', 'bacon']
    selection = []
    if i == 0:
        return 'none'
    else:
        for n in range(i):
            selection.append(meats[random.randint(0, 5)])
    return ' & '.join(set(selection))

def calc_veggies():
    i = random.randint(0, 4)
    veggies = ['tomato', 'olives', 'onions', 'peppers', 'pineapple', 'mushrooms']
    selection = []
    if i == 0:
        return 'none'
    else:
        for n in range(i):
            selection.append(veggies[random.randint(0, 5)])
    return ' & '.join(set(selection))

def gen_pizza():
    sauce = calc_sauce()
    cheese = calc_cheese()
    meats = calc_meats()
    veggies = calc_veggies()
    return Pizza('', 0, sauce, cheese, meats, veggies)
    
def random_pizzas(quantity):
    pizzas = []
    o_id = str(uuid.uuid4().int)
    s_id = random.randint(1, 100)

    for _ in range(quantity):
        pizza = gen_pizza()
        pizza.order_id = o_id
        pizza.store_id = s_id
        pizzas.append(pizza)

    return pizzas

if __name__ == "__main__":
    gen_orders()        

