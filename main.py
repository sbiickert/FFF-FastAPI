from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

from api.routers import general, reporting, transactions

app = FastAPI()

app.include_router(general.router)
app.include_router(transactions.router)
app.include_router(reporting.router)