# main.py

import wx
import sys
import logging
from controller import XlitToolController

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

logger = logging.getLogger(__name__)

def main():
    """Main application entry point with error handling."""
    try:
        setup_logging()
        logger.info("Starting xlit-tool application")
        app = wx.App()
        controller = XlitToolController()
        controller._view.Show()
        logger.info("Application started successfully")
        app.MainLoop()
    except ImportError as e:
        error_msg = f"Missing required dependency: {e}"
        logger.error(error_msg)
        print(f"Error: {error_msg}")
        print("Please ensure all required packages are installed.")
        sys.exit(1)
    except Exception as e:
        error_msg = f"Failed to start application: {e}"
        logger.error(error_msg)
        print(f"Error: {error_msg}")
        print("Please check the application logs for more details.")
        sys.exit(1)

if __name__ == '__main__':
    main()

