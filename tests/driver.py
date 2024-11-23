import httpx

def driver_story():
    client = httpx.Client(base_url="http://167.71.53.45/")
    
    print('The driver signs up using his wallet and verifies is signup.')
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

if __name__ == '__main__':
    driver_story()