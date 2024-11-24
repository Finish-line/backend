import fastapi
from fastapi.middleware.cors import CORSMiddleware

from src.rest.router import router as rest_router

app = fastapi.FastAPI()

# setup middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include all api routers
app.include_router(rest_router)