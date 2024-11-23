import random
from time import sleep
import httpx
from sqlmodel import true

def driver_story():
    client = httpx.Client(base_url="http://167.71.53.45/")
    
    print('The driver signs up using his wallet and verifies his signup.')
    did_token_header = {'Authorization' : 'Bearer 98ec2de73ece67922a9561fd120dfab6'}
    response = client.get('/api/auth/verify?role=driver', headers=did_token_header)
    jwt_headers = {'Authorization': 'Bearer ' + response.json()['access_token']}
    print(f'He gets a new JWT: {jwt_headers}')
    print()
    
    print('The driver registeres his account as a driver.')
    driver_data = {
        'car_type': 'Volvo XC70'
    }
    
    response = client.post('/api/driver', headers=jwt_headers, json=driver_data)
    print(response.json())
    print()
    
    print('He decides to drive. He is marked "active" and his position is updated every few seconds')
    driver_data = {
        'active': True,
        'position_lat': 48.149989,
        'position_long': 11.568190
    }
    response = client.put('/api/driver', headers=jwt_headers, json=driver_data)
    
    positions = [
        { 'position_lat': 48.156751, 'position_long': 11.565087 },
        { 'position_lat': 48.156280, 'position_long': 11.551689},
        { 'position_lat': 48.158583, 'position_long': 11.548644},
        { 'position_lat': 48.161421, 'position_long': 11.544314}
    ]
    print('He drives through munich waiting for a passenger ...')
    
    requests = client.get("/trip", headers=jwt_headers)
    print(f'Requests: {requests}')
    
    while(True):
        sleep(5)
        new_position = random.choice(positions)
        response = client.put('/api/driver', headers=jwt_headers, json=new_position)
        print(f'His location is updated! New location: {response.json()}')
        
        
    
    
if __name__ == '__main__':
    driver_story()