from fastapi import FastAPI
from auth.controller import router as auth_router
from users.controller import router as users_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],      # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],      # Permite todos los headers
)

# Registrar los routers para las rutas de autenticación y usuarios
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])