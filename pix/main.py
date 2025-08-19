from fastapi import FastAPI
from debt import router as debt_router
from fastapi.staticfiles import StaticFiles
#from admin import router as admin_router
#from auth import router as auth_router

app = FastAPI()

app.mount("/debt/static", StaticFiles(directory="debt/static"), name="debt_static")
app.mount("/admin/static", StaticFiles(directory="admin/static"), name="admin_static")

app.include_router(debt_router)
#app.include_router(admin_router)
#app.include_router(auth_router)