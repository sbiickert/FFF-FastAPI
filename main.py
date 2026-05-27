from fastapi import FastAPI

from api.routers import general, reporting, transactions

app = FastAPI(root_path="/FFF6")

app.include_router(general.router)
app.include_router(transactions.router)
app.include_router(reporting.router)