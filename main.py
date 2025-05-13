from fastapi import FastAPI
from auth.controller import router as auth_router
from users.controller import router as users_router

app = FastAPI()

# Registrar los routers para las rutas de autenticación y usuarios
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])

@app.get("/")
def root():
    return {"message": "API User operativa 🚀"}
