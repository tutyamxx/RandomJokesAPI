from app.main import app
from mangum import Mangum

# Wrap FastAPI app for serverless deployment
handler = Mangum(app)
