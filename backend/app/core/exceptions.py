from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
import traceback

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────
# Custom Exception Classes
# ─────────────────────────────────────────

class CRMBaseException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class HCPNotFoundException(CRMBaseException):
    def __init__(self, hcp_id: int = None, name: str = None):
        identifier = f"ID {hcp_id}" if hcp_id else f"name '{name}'"
        super().__init__(
            message=f"HCP with {identifier} not found",
            status_code=404
        )


class InteractionNotFoundException(CRMBaseException):
    def __init__(self, interaction_id: int):
        super().__init__(
            message=f"Interaction with ID {interaction_id} not found",
            status_code=404
        )


class AgentException(CRMBaseException):
    def __init__(self, detail: str):
        super().__init__(
            message=f"AI Agent error: {detail}",
            status_code=500
        )


class DatabaseException(CRMBaseException):
    def __init__(self, detail: str):
        super().__init__(
            message=f"Database error: {detail}",
            status_code=500
        )


class ValidationException(CRMBaseException):
    def __init__(self, detail: str):
        super().__init__(
            message=f"Validation error: {detail}",
            status_code=422
        )


class GroqAPIException(CRMBaseException):
    def __init__(self, detail: str):
        super().__init__(
            message=f"Groq API error: {detail}",
            status_code=503
        )


# ─────────────────────────────────────────
# Exception Handlers
# ─────────────────────────────────────────

async def crm_exception_handler(
    request: Request,
    exc: CRMBaseException
):
    logger.error(
        f"CRM Exception: {exc.message} | "
        f"Path: {request.url.path} | "
        f"Method: {request.method}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "type": exc.__class__.__name__,
                "message": exc.message,
                "path": str(request.url.path),
            }
        }
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " → ".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })

    logger.warning(
        f"Validation Error | "
        f"Path: {request.url.path} | "
        f"Errors: {errors}"
    )

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "type": "ValidationError",
                "message": "Request validation failed",
                "details": errors,
                "path": str(request.url.path),
            }
        }
    )


async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    logger.warning(
        f"HTTP Exception: {exc.detail} | "
        f"Status: {exc.status_code} | "
        f"Path: {request.url.path}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "type": "HTTPException",
                "message": exc.detail,
                "path": str(request.url.path),
            }
        }
    )


async def global_exception_handler(
    request: Request,
    exc: Exception
):
    # Log full traceback for unexpected errors
    logger.error(
        f"Unexpected Error | "
        f"Path: {request.url.path} | "
        f"Error: {str(exc)}\n"
        f"{traceback.format_exc()}"
    )
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "type": "InternalServerError",
                "message": "An unexpected error occurred",
                "path": str(request.url.path),
            }
        }
    )