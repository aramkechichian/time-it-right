from fastapi import FastAPI
from app.routes import auth_routes, user_routes, game_session_routes, websocket_routes
from app.exceptions.custom_exceptions import AppException
from app.core.exception_handler import app_exception_handler

def create_app() -> FastAPI:
    app = FastAPI(title="Time It Right API by Aram Kechichian")
    app.add_exception_handler(AppException, app_exception_handler)
    # Routers
    app.include_router(auth_routes.router)
    app.include_router(user_routes.router)
    app.include_router(game_session_routes.router)
    app.include_router(websocket_routes.router)

    return app


app = create_app()