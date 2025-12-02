import json
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

print('GET /health')
r = client.get('/health')
print(r.status_code)
try:
    print(json.dumps(r.json(), indent=2))
except Exception:
    print(r.text)

print('\nGET /docs')
r = client.get('/docs')
print(r.status_code)
print('Length of content:', len(r.text))

print('\nPOST /api/v1/auth/register')
payload = {
    'username': 'testuser@example.com',
    'email': 'testuser@example.com',
    'password': 'TestPassword123!',
    'full_name': 'Test User'
}
r = client.post('/api/v1/auth/register', json=payload)
print(r.status_code)
try:
    print(json.dumps(r.json(), indent=2))
except Exception:
    print(r.text)

print('\nPOST /api/v1/auth/login')
login = {'username': 'testuser@example.com', 'password': 'TestPassword123!'}
r = client.post('/api/v1/auth/login', json=login)
print(r.status_code)
try:
    print(json.dumps(r.json(), indent=2))
except Exception:
    print(r.text)
