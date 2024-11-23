import fastapi
from fastapi.middleware.cors import CORSMiddleware

from src.database import create_db_and_tables

from src.auth.router import router as auth_router
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

create_db_and_tables()

# include all api routers
app.include_router(auth_router)
app.include_router(rest_router)