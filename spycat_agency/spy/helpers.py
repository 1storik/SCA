import requests


def validate_breed(breed_name):
    response = requests.get('https://api.thecatapi.com/v1/breeds')
    if response.status_code == 200:
        breeds = response.json()
        return any(breed['name'].lower() == breed_name.lower() for breed in breeds)
    return False
