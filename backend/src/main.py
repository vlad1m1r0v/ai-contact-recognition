from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from src.core.logging import setup_logging, get_logger
from src.core.config import settings
from src.core.exceptions.handlers import setup_exception_handlers
from src.presentation.api.router import api_router
from src.infrastructure.di import AppModuleProvider

logger = get_logger("app.main")


def create_app() -> FastAPI:
    # 1. Initialize system-wide logging with strict format and guidelines
    setup_logging()

    logger.executing("Initializing FastAPI Application bootstrap")

    # 2. Instantiate FastAPI
    app = FastAPI(
        title="Multimodal Contact Recognition API",
        version="1.0.0",
        description=(
            "A Clean Architecture FastAPI service that extracts contact cards and core service tags "
            "from various types of images (business cards, event posters, flyers, etc.) using "
            "the Llama-4-Scout Vision LLM on Groq."
        ),
        debug=settings.debug,
    )

    # 3. Configure CORS for frontend access
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:9211",
            "http://localhost:9210",
            "http://localhost",
            "http://83.229.86.141:9210",
            "http://83.229.86.141:9211",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 4. Setup core API exception handlers
    setup_exception_handlers(app)

    # 5. Bind routers
    app.include_router(api_router)

    # 5. Bootstrap Dishka Dependency Injection Container
    logger.executing("Wiring Dishka DI container")
    container = make_async_container(AppModuleProvider())
    setup_dishka(container, app)

    logger.finished("FastAPI Application bootstrap completed successfully")
    return app


# Main ASGI application instance
app = create_app()
