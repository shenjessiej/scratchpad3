import random, uuid

colors = ["red", "orange", "yellow", "blue", "green", "indigo", "violet", "brown", "sienna", "carnation", "citrus", "saffron", "lime", "lavender", "emerald"]
animals = ["cat", "dog", "hamster", "gecko", "ferret", "oppossum", "phoenix", "dinosaur", "spider", "camel", "unicorn", "thestral", "swan"]

def generate_random_url():
    color = colors[random.randint(0, 14)]
    animal = animals[random.randint(0, 12)]
    number = uuid.uuid1()

    return color + "-" + animal + "-" + str(number)