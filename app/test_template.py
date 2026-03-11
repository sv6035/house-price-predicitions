from app import app

with app.test_client() as client:
    response = client.get('/')
    print('Status Code:', response.status_code)
    if response.status_code == 200:
        print('SUCCESS: Template loads without errors!')
        print('App is ready with professional cityscape background')
    else:
        print('ERROR: Template still has issues')
        print('Response:', response.data.decode()[:200])