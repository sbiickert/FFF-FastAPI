from fastapi import FastAPI

from api.routers import general, reporting, transactions

app = FastAPI()

app.include_router(general.router)
app.include_router(transactions.router)
app.include_router(reporting.router)