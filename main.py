import os
import sys
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Add the current directory to the path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Determine which framework to use based on environment variable
# Default to FastAPI if not specified
FRAMEWORK = os.getenv("FRAMEWORK", "fastapi").lower()
logger.info(f"Starting application with framework: {FRAMEWORK}")

# Import the appropriate application based on the framework
if FRAMEWORK == "nicegui":
    try:
        # Import the enhanced NiceGUI implementation
        from app.frontend.nicegui_app import ui, app as nicegui_app
        logger.info("NiceGUI framework initialized successfully")
        application = nicegui_app
        
        # Configure NiceGUI app settings
        nicegui_app.title = "Project Base - Python-Native Web Application"
        nicegui_app.favicon = "🚀"
    except ImportError as e:
        logger.error(f"Failed to initialize NiceGUI: {e}")
        print("NiceGUI not installed. Please install with: pip install nicegui")
        exit(1)
else:
    # Default to FastAPI
    from app import app
    logger.info("FastAPI framework initialized successfully")
    application = app

# This is used by ASGI servers like Uvicorn
app = application

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    
    # Run the application with uvicorn
    if FRAMEWORK == "nicegui":
        # Start NiceGUI directly
        ui.run(host=host, port=port, reload=True, title="Project Base")
    else:
        # Start FastAPI with uvicorn
        uvicorn.run("main:app", host=host, port=port, reload=True)