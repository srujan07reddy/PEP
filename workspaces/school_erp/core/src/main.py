from fastapi import FastAPI

app = FastAPI()

@app.get('/api/v1/status')
def get_status():
    return {'service': 'core', 'status': 'running'}
