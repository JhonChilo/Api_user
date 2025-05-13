from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.controller import router as auth_router
from users.controller import router as users_router

app = FastAPI()

# Habilitar CORS para cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar los routers para las rutas de autenticación y usuarios
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])

@app.get("/")
def root():
    return {"message": "API User operativa 🚀"}