from fastapi import Request
from fastapi.responses import HTMLResponse
from . import router
from .. import templates
import os
from datetime import datetime

@router.get('/', response_class=HTMLResponse)
async def index(request: Request):
    """Serves the main index page using Jinja2 templates."""
    import logging
    logger = logging.getLogger(__name__)

    if not templates:
        error_msg = "Templates support is not configured. Check app/__init__.py."
        logger.error(error_msg)
        # Consider raising an HTTPException or returning a more structured error
        return HTMLResponse(
            content=f"<html><body><h1>Configuration Error</h1><p>{error_msg}</p></body></html>",
            status_code=500
        )

    try:
        # The existence of 'templates' object implies it's configured.
        # FastAPI/Starlette's Jinja2Templates will raise an internal error if the specific template is not found.
        # This will be caught by the generic exception handler.
        logger.info(f"Attempting to render index.html")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception as e:
        # This will catch errors if index.html is missing or if there's a rendering error within the template itself.
        # The generic error handler in error_handling.py should ideally log this.
        error_msg = f"Error rendering template 'index.html': {str(e)}"
        logger.exception(error_msg) # Log with stack trace
        # It's often better to let the centralized error handlers deal with the response
        # For now, returning a simple HTML error for clarity during development.
        return HTMLResponse(
            content=f"<html><body><h1>Application Error</h1><p>Could not render the page. Please check logs.</p></body></html>",
            status_code=500
        )

# Add additional frontend routes here using the @router decorator