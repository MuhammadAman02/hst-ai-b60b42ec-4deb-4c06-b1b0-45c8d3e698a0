from nicegui import ui, app
import logging
import asyncio
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize counter for demo
count = 0

# Custom CSS for enhanced styling
ui.add_head_html("""
<style>
    .hero-gradient {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    .animate-pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: .7; }
    }
</style>
""")

# Define the main page with enhanced UI
@ui.page('/')
def main_page():
    """Main page of the NiceGUI application with modern, appealing UI."""
    # Hero section with gradient background
    with ui.column().classes('w-full hero-gradient text-white p-8'):
        ui.label('Project Base').classes('text-4xl font-bold mb-2')
        ui.label('A Python-Native Web Application Framework').classes('text-xl mb-4')
        ui.markdown('''
        Build powerful web applications with pure Python. No JavaScript required.
        ''')
        with ui.row().classes('mt-4'):
            ui.button('Get Started', on_click=lambda: ui.open('/docs')).props('color=white text-purple-700 push')
            ui.button('Learn More', on_click=lambda: ui.navigate('#features')).props('outline color=white push')
    
    # Features section
    with ui.column().classes('w-full max-w-6xl mx-auto p-8').id('features'):
        ui.label('Key Features').classes('text-3xl font-bold text-center mb-8')
        
        with ui.grid(columns=3).classes('gap-6'):
            # Feature cards with hover effects
            for title, icon, description in [
                ('Python-Native UI', '🐍', 'Build beautiful interfaces with pure Python code'),
                ('Real-time Updates', '⚡', 'Reactive components that update instantly'),
                ('FastAPI Integration', '🚀', 'Seamlessly combine with powerful API endpoints'),
                ('Type Safety', '✅', 'Leverage Python type hints for better code'),
                ('Modern Design', '🎨', 'Clean, responsive layouts out of the box'),
                ('Easy Deployment', '🌐', 'Deploy anywhere with Docker and fly.io')
            ]:
                with ui.card().classes('feature-card transition-all duration-300 h-full'):
                    ui.label(f'{icon} {title}').classes('text-xl font-bold mb-2')
                    ui.label(description).classes('text-gray-600')
        
        # Demo section with interactive components
    with ui.column().classes('w-full bg-gray-100 p-8'):
        ui.label('Interactive Demo').classes('text-3xl font-bold text-center mb-8')
        
        with ui.card().classes('w-full max-w-3xl mx-auto'):
            ui.label('Try it out').classes('text-xl font-bold mb-4')
            
            # Counter demo with improved styling
            with ui.row().classes('items-center justify-center mb-6'):
                ui.label('Counter:').classes('mr-2')
                label = ui.label(str(count)).classes('text-2xl font-bold px-4 py-2 bg-gray-200 rounded')
                
                def increment():
                    global count
                    count += 1
                    label.text = str(count)
                    logger.info(f"Counter incremented to {count}")
                
                def decrement():
                    global count
                    count -= 1
                    label.text = str(count)
                    logger.info(f"Counter decremented to {count}")
                
                ui.button('−', on_click=decrement).props('round color=red').classes('text-xl')
                ui.button('+', on_click=increment).props('round color=green').classes('text-xl')
            
            # Color picker demo
            ui.label('Color Picker Demo').classes('font-bold mt-4')
            color = ui.color_picker('Choose a color', value='#6366F1')
            
            with ui.row().classes('items-center mt-2'):
                ui.label('Selected color:')
                with ui.element('div').classes('w-8 h-8 rounded border border-gray-300').bind_style_from(color, 'background-color'):
                    pass
                ui.label().bind_text_from(color)
    
    # Call to action section
    with ui.column().classes('w-full bg-blue-900 text-white p-8 text-center'):
        ui.label('Ready to Build Your Python Web App?').classes('text-3xl font-bold mb-4')
        ui.label('Get started with Project Base today and create amazing web applications with pure Python').classes('text-xl mb-6')
        ui.button('Start Building Now', on_click=lambda: ui.notify('Project initialized!')).props('size=large color=white text-blue-900 push')
        
    # Footer
    with ui.footer().classes('w-full bg-gray-800 text-white p-4 text-center'):
        ui.label(f'© {datetime.now().year} Project Base. All rights reserved.')
        ui.label('Built with Python and NiceGUI').classes('text-sm text-gray-400 mt-1')
        with ui.card().classes('w-full mt-4'):
            ui.label('Sample Chart').classes('text-xl')
            chart = ui.chart({
                'title': {'text': 'Sample Data'},
                'xAxis': {'categories': ['Jan', 'Feb', 'Mar', 'Apr', 'May']},
                'series': [{
                    'name': 'Data Series 1',
                    'data': [29, 71, 106, 129, 144]
                }, {
                    'name': 'Data Series 2',
                    'data': [80, 120, 105, 110, 95]
                }]
            }).classes('h-64')

# API endpoints can be added with FastAPI
@app.get('/api/health')
def health_check():
    """Health check endpoint."""
    return {'status': 'ok'}

# Configure app
app.title = 'NiceGUI Application'

# This is needed for the main.py integration
if __name__ == '__main__':
    ui.run()