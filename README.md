# Project Base

A foundation for building enterprise-grade Python-native web applications with modern UI and efficient deployment.

## Features

- **Python-Native UI**: Build beautiful interfaces with pure Python code using NiceGUI or FastAPI with Jinja2 templates
- **Dual Framework Support**: Choose between FastAPI (default) or NiceGUI based on your project needs
- **Modern Design**: Clean, responsive layouts with appealing aesthetics
- **Auto-Scaling Deployment**: Optimized fly.io configuration with cost-saving auto-shutdown for inactive machines
- **Docker Support**: Production-ready containerization
- **Health Monitoring**: Built-in health check endpoints for reliability

## Project Structure

```
project_base/
├── app/                  # Main application package
│   ├── api/              # API endpoints
│   ├── core/             # Core configuration
│   ├── frontend/         # UI implementations
│   ├── models/           # Data models
│   ├── services/         # Business logic
│   ├── static/           # Static assets
│   └── templates/        # Jinja2 templates
├── logs/                 # Application logs
├── static/               # Global static assets
├── templates/            # Global templates
├── Dockerfile            # Container configuration
├── fly.toml              # fly.io deployment config
├── main.py               # Application entry point
├── requirements.txt      # Dependencies
└── run.py                # Alternative runner
```

## Framework Options

### FastAPI (Default)

The default framework is FastAPI, which provides a robust API-first approach with Jinja2 templating for server-side rendered views.

### NiceGUI

The enhanced NiceGUI implementation provides a modern, reactive UI built entirely with Python. The landing page features:

- Gradient hero section with call-to-action buttons
- Feature cards with hover effects
- Interactive demo components
- Responsive design for all device sizes

## Auto-Scaling Configuration

The `fly.toml` file includes optimized settings for cost-effective deployment:

- **Auto-stop**: Machines automatically stop when idle
- **Auto-start**: Machines start on-demand when requests arrive
- **Health checks**: Regular monitoring to ensure application health
- **Idle timeout**: Machines shut down after 60 minutes of inactivity
- **Minimum running machines**: Set to 0 to minimize costs when not in use

## Development

### Adding New Features

1. For API endpoints, add new routes in the `app/api/` directory
2. For UI components, modify `app/frontend/nicegui_app.py` (NiceGUI) or templates in `templates/` (FastAPI)
3. For business logic, add services in `app/services/`

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
FRAMEWORK=fastapi  # or nicegui
APP_ENV=development
PORT=8000
HOST=0.0.0.0
APP_RELOAD=true
```

```
project_root/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── logging_config.py
│   ├── frontend/
│   │   ├── __init__.py
│   │   ├── nicegui_app.py
│   │   ├── reactpy_app.py
│   │   ├── reflex_app.py
│   │   └── routes.py
│   ├── generated/
│   ├── models/
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   ├── static/
│   │   └── style.css
│   └── templates/
│       ├── base.html
│       ├── index.html
│       └── partials/
│           ├── footer.html
│           └── header.html
├── logs/
│   └── app.log
├── Dockerfile
├── fly.toml
├── main.py
├── requirements.txt
└── run.py
```

## Supported Frameworks

This project base supports multiple modern Python web frameworks:

1. **FastAPI** - Default framework for building APIs
2. **NiceGUI** - Python-based UI framework for building web interfaces
3. **ReactPy** - React-inspired UI library for Python
4. **Reflex** - Python-first web framework

## Getting Started
### Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Deployment Preparation

Before deploying the application, run the pre-deployment script to ensure all templates and static files are properly set up:

**On Windows:**
```bash
pre_deploy.bat
```

**On Linux/Mac:**
```bash
chmod +x pre_deploy.sh
./pre_deploy.sh
```

Alternatively, you can run the setup script directly:
```bash
python setup_deployment.py
```

This script will:
- Create necessary directories if they don't exist
- Copy templates and static files to the app directory structure
- Create default templates and static files if they don't exist

**Important Note:** If you encounter a blank screen after deployment, it's likely because the templates and static files were not properly copied to the app directory. Run the pre-deployment script before deploying to fix this issue.

### Docker Deployment

To build and run the application using Docker:

```bash
# Build the Docker image
docker build -t my-fastapi-app .

# Run the container
docker run -p 8000:8000 my-fastapi-app
```

The application will be available at http://localhost:8000

### Running the Application

You can run the application with different frameworks by setting the `FRAMEWORK` environment variable:

```bash
# Run with FastAPI (default)
python main.py

# Run with NiceGUI
FRAMEWORK=nicegui python main.py

# Run with ReactPy
FRAMEWORK=reactpy python main.py

# Run with Reflex
FRAMEWORK=reflex python main.py
```

Alternatively, you can set the framework in a `.env` file:

```
FRAMEWORK=nicegui
```

## Application Types

This project base supports various application types as described in the HST AI Python Engineer prompts:

### Web Applications
- FastAPI/Flask/Django web services
- RESTful APIs
- GraphQL APIs
- Modern UI frameworks (NiceGUI, ReactPy, Reflex)
- Server-side rendered applications

### AI/ML Applications
- Chatbots and conversational agents
- Natural language processing systems
- Computer vision applications
- Recommendation systems
- Fraud detection systems

### Data Processing
- ETL pipelines
- Data analysis scripts
- Reporting systems
- Big data processing

### Automation
- Task automation scripts
- Workflow automation
- Scheduled jobs
- System monitoring

## Core Principles

This project follows these key principles:

1. **Code Quality and Organization**
   - Small, focused functions and classes (< 50 lines)
   - Type hints for type safety
   - PEP 8 style guidelines
   - Modular designs
   - Extensive logging for debugging

2. **Component Creation**
   - Separate files for each module
   - Established Python libraries
   - SOLID principles
   - Proper package organization

3. **State Management**
   - Appropriate data structures
   - Proper database models and ORM
   - Minimal global state
   - Response caching when appropriate

4. **Error Handling**
   - Proper exception handling
   - Logging for errors
   - User-friendly error messages
   - Custom exceptions when appropriate

5. **Performance**
   - Code optimization
   - Async/await for I/O-bound operations
   - Efficient data structures and algorithms
   - Minimal unnecessary computations

6. **Security**
   - Input validation
   - Proper authentication
   - Data sanitization
   - Security best practices

7. **Testing**
   - Unit tests for critical functions
   - Integration tests
   - Pytest for testing
   - Error handling verification

8. **Documentation**
   - Docstrings for complex functions
   - Up-to-date README
   - Setup instructions
   - API endpoint documentation

## Improvements for Code Generation\n\n1. **Ensure Parameter Order**: Always place parameters without defaults before those with defaults in function definitions.\n2. **Consistent Naming Conventions**: Use consistent naming conventions across generated code to avoid confusion.\n3. **Error Handling**: Include basic error handling in generated code to prevent runtime errors.\n4. **Testing and Validation**: Automatically generate basic tests to validate generated code.\n   - Implement custom validators when needed\n   - Provide clear error messages\n   - Validate at the API boundary\n5. **Dependency Management**: Ensure all necessary dependencies are added to `requirements.txt` and installed during setup.\n- **Initial Error-Free Execution**: Prioritize generating applications that run without errors in the first iteration, ensuring all dependencies are correctly set up and configurations are validated.\n- **Focus on Core Functionality and UI**: Leverage language models to generate essential components and configurations necessary for a functional application, avoiding unnecessary overhead from testing features that are not immediately visible.\n- **Dependency Management**: Ensure all necessary dependencies are added to `requirements.txt` and installed during setup.\n- **Finalize and Test**: Ensure the application runs correctly and meets the requirements.\n\nRemember to prioritize delivering working code that meets the user's core requirements first, then enhance it with additional features as needed. Focus on creating a minimal viable product before adding complexity.