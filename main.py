from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import certifi
import random
import os
load_dotenv()
first_names = [
    "Emily", "James", "Sophia", "Michael", "Olivia",
    "William", "Emma", "Alexander", "Isabella", "Benjamin",
    "Ava", "Daniel", "Mia", "Matthew", "Charlotte",
    "Lucas", "Amelia", "Ethan", "Harper", "Jacob"
]
last_names = [
    "Smith", "Johnson", "Williams", "Jones", "Brown",
    "Davis", "Miller", "Wilson", "Moore", "Taylor",
    "Anderson", "Thomas", "Jackson", "White", "Harris",
    "Martin", "Thompson", "Garcia", "Martinez", "Robinson"
]
size_list = ['8', '8.5', '9', '9.5', '10', '10.5', '11', '12', '13']
shoe_entry_data = []

client = MongoClient(os.environ['uri'], server_api=ServerApi(
    '1'), tlsCAFile=certifi.where())


def shoe_raffle():
    raffle_winners = db['winners']
    shoes_sizes_instock = {
        '8': 1,
        '8.5': 1,
        '9': 1,
        '9.5': 2,
        '10': 2,
        '10.5': 2,
        '11': 1,
        '12': 1,
        '13': 1,
    }
    for i in shoes_sizes_instock:
        winner = []
        for j in range(shoes_sizes_instock[i]):
            find_all_people_in_size = collection.find({'size': i})
            result = list(find_all_people_in_size)
            winner.append(random.choice(result))
        raffle_winners.insert_many(winner)


try:
    db = client.shoeraffles
    collection = db['shoes']

    for _ in range(50):
        first = random.randrange(0, 20)
        last = random.randrange(0, 20)
        random_phone = f'510-{str(random.randrange(0, 9))}{str(random.randrange(0, 9))}{str(random.randrange(0, 9))}-{str(random.randrange(0, 9))}{str(random.randrange(0, 9))}{str(random.randrange(0, 9))}{str(random.randrange(0, 9))}'
        random_name = f'{first_names[first]} {last_names[last]}'
        shoe_entry_data.append({
            "name": random_name,
            "size": size_list[random.randrange(0, len(size_list))],
            "phone_number": random_phone,
            "email": f"{first_names[first]}{last_names[last]}@yahoo.com"
        })

    entries_added = collection.insert_many(shoe_entry_data)
    shoe_raffle()

except Exception as e:
    print(f"An error occurred: {e}")
