from http.server import BaseHTTPRequestHandler, HTTPServer
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import certifi
import random
import json
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
    db = client.shoeraffles
    raffle_winners = db.shoeraffles['winners']
    collection = db['shoes']
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


def run_program():
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


class PracticingPythonOnTheBackend(BaseHTTPRequestHandler):
    db = client.shoeraffles
    raffle_winners = db.shoeraffles['winners']
    collection = db['shoes']

    def set_handlers(self):
        def _set_headers(self):
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods',
                             'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()

        def do_OPTIONS(self):
            # Handle preflight requests for CORS
            self.send_response(204)
            self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            response = {'lol': 'lmao'}
            response_json = json.dumps(response)
            self.wfile.write(response_json.encode('utf-8'))

            print('hellowiefbguoifrboeirfherioe')

        elif self.path == '/size':

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Extract 'size' parameter from query string
            size = query_params.get('size', [None])[0]
            if size:
                try:
                    # Convert the size parameter to an integer
                    size = int(size)
                    response = f'The size is {size}'
                except ValueError:
                    response = 'Invalid size parameter. Please enter a valid integer.'
            else:
                response = 'No size parameter provided.'

                self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_POST(self):
        self.send_response(200)
        self._set_headers()

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        response = {'received': post_data.decode('utf-8')}
        response_json = json.dumps(response)
        self.wfile.write(response_json.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=PracticingPythonOnTheBackend, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}..')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
