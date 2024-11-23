import httpx

def driver_story():
    client = httpx.Client("http://167.71.53.45/")
    
    print('The driver signs up using his wallet and verifies is signup.')
    response = client.get('/api/auth/verify?role=driver')
    print(response)

if __name__ == '__main__':
    driver_story()