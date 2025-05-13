import chainlit as cl
from chainlit.input_widget import Select, Slider

@cl.on_settings_update
async def setup_settings(settings):
    """Handle settings updates."""
    cl.user_session.set("settings", settings)

def setup_custom_ui():
    """Set up custom UI elements for Chainlit."""
    # Set a custom title
    cl.title = "AI Evaluation Assistant"
    
    # Set a custom logo (base64 encoded SVG)
    cl.logo_url = "https://img.icons8.com/fluency/96/artificial-intelligence.png"
    
    # Set a custom favicon
    cl.favicon_url = "https://img.icons8.com/fluency/48/artificial-intelligence.png"
    
    # Disable download buttons
    cl.user_settings.disable_download_button = True
    
    # Keep content fully expanded
    cl.user_settings.expandable_messages = False
    
    # Add custom settings
    cl.input_widget(
        Select(
            id="theme",
            label="Theme",
            values=["Light", "Dark", "System"],
            initial_value="System",
        )
    )
    
    cl.input_widget(
        Slider(
            id="temperature",
            label="AI Temperature",
            initial=0.0,
            min=0.0,
            max=1.0,
            step=0.1,
        )
    )

# Run setup when this module is imported
setup_custom_ui() 