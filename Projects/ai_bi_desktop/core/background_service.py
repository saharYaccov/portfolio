"""
Background Service
=================
Desktop background service with system tray icon
that monitors for files and launches the Gradio dashboard on demand.
"""

import sys
import threading
import time
from pathlib import Path
from typing import Optional
from loguru import logger
import psutil

# System tray and desktop integration
try:
    import pystray
    from pystray import MenuItem as item
    from PIL import Image, ImageDraw
except ImportError:
    logger.warning("pystray not available - system tray will not work")
    pystray = None

# File monitoring
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    logger.warning("watchdog not available - file monitoring will not work")
    Observer = None

from config.settings import app_config
from ui.gradio_app import launch_dashboard


class DesktopBackgroundService:
    """
    Background service that runs in the system tray
    """
    
    def __init__(self):
        self.icon = None
        self.dashboard_thread = None
        self.dashboard_running = False
        self.last_file_path: Optional[str] = None
        
        logger.info("Background Service initialized")
    
    def create_icon_image(self):
        """
        Create system tray icon image
        """
        # Create a simple icon (you can replace with actual icon file)
        width = 64
        height = 64
        color1 = (100, 200, 255)  # Light blue
        color2 = (50, 150, 200)   # Darker blue
        
        image = Image.new('RGB', (width, height), color1)
        dc = ImageDraw.Draw(image)
        
        # Draw a simple AI/Analytics symbol
        dc.rectangle([10, 10, 54, 54], fill=color2, outline=color1)
        dc.ellipse([20, 20, 44, 44], fill=color1)
        
        return image
    
    def open_dashboard(self, icon=None, item=None):
        """
        Open the Gradio dashboard
        """
        if self.dashboard_running:
            logger.info("Dashboard already running")
            return
        
        logger.info("Launching Gradio dashboard...")
        
        self.dashboard_thread = threading.Thread(
            target=launch_dashboard,
            kwargs={'share': False, 'port': app_config.gradio_port},
            daemon=True
        )
        self.dashboard_thread.start()
        self.dashboard_running = True
        
        logger.info(f"Dashboard launched at http://localhost:{app_config.gradio_port}")
    
    def analyze_last_file(self, icon=None, item=None):
        """
        Analyze the last uploaded file
        """
        if self.last_file_path:
            logger.info(f"Analyzing {self.last_file_path}")
            self.open_dashboard()
        else:
            logger.warning("No file to analyze")
    
    def show_about(self, icon=None, item=None):
        """
        Show about information
        """
        logger.info(f"{app_config.app_name} v{app_config.version}")
        print(f"\n{app_config.app_name}")
        print(f"Version: {app_config.version}")
        print("Intelligent BI & AutoML Desktop Assistant")
        print("\nPress Ctrl+C to quit\n")
    
    def quit_application(self, icon=None, item=None):
        """
        Quit the application
        """
        logger.info("Shutting down background service...")
        
        if icon:
            icon.stop()
        
        sys.exit(0)
    
    def run(self):
        """
        Run the background service with system tray
        """
        if pystray is None:
            logger.error("pystray not available - cannot run in system tray")
            logger.info("Running dashboard directly instead...")
            launch_dashboard(port=app_config.gradio_port)
            return
        
        # Create menu
        menu = pystray.Menu(
            item('📊 Open Dashboard', self.open_dashboard, default=True),
            item('🔄 Analyze Last File', self.analyze_last_file),
            pystray.Menu.SEPARATOR,
            item('ℹ️ About', self.show_about),
            item('❌ Quit', self.quit_application)
        )
        
        # Create icon
        image = self.create_icon_image()
        self.icon = pystray.Icon(
            name=app_config.app_name,
            icon=image,
            title=app_config.app_name,
            menu=menu
        )
        
        logger.info("Starting system tray service...")
        logger.info("Right-click the tray icon to access features")
        
        # Start monitoring resource usage
        monitor_thread = threading.Thread(
            target=self._monitor_resources,
            daemon=True
        )
        monitor_thread.start()
        
        # Run the icon (blocking)
        self.icon.run()
    
    def _monitor_resources(self):
        """
        Monitor system resource usage
        """
        process = psutil.Process()
        
        while True:
            try:
                mem_mb = process.memory_info().rss / (1024 * 1024)
                cpu_percent = process.cpu_percent(interval=1)
                
                # Check limits
                if mem_mb > app_config.max_memory_mb:
                    logger.warning(f"High memory usage: {mem_mb:.1f} MB")
                
                if cpu_percent > app_config.max_cpu_percent:
                    logger.warning(f"High CPU usage: {cpu_percent:.1f}%")
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Resource monitoring error: {e}")
                break


class FileMonitorHandler(FileSystemEventHandler):
    """
    Handler for file system events
    """
    
    def __init__(self, background_service: DesktopBackgroundService):
        self.service = background_service
        self.supported_extensions = {'.csv', '.xlsx', '.xls'}
    
    def on_created(self, event):
        """
        Called when a file is created
        """
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        if file_path.suffix.lower() in self.supported_extensions:
            logger.info(f"New data file detected: {file_path.name}")
            self.service.last_file_path = str(file_path)
            
            # Auto-open dashboard if configured
            if app_config.watch_downloads_folder:
                size_mb = file_path.stat().st_size / (1024 * 1024)
                
                if size_mb <= app_config.auto_analyze_threshold_mb:
                    logger.info(f"Auto-analyzing {file_path.name}")
                    self.service.open_dashboard()


def start_file_monitoring(background_service: DesktopBackgroundService, 
                         path: str = None):
    """
    Start monitoring a directory for new data files
    """
    if Observer is None:
        logger.warning("File monitoring not available")
        return
    
    if path is None:
        # Default to user's Downloads folder
        path = str(Path.home() / "Downloads")
    
    event_handler = FileMonitorHandler(background_service)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    
    logger.info(f"Monitoring {path} for new data files")


# ================================
# MAIN ENTRY POINT
# ================================

def main():
    """
    Main entry point for background service
    """
    # Setup logging
    logger.remove()  # Remove default handler
    logger.add(
        sys.stderr,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level=app_config.log_level
    )
    
    logger.add(
        "logs/ai_bi_desktop_{time}.log",
        rotation=app_config.log_rotation,
        retention=app_config.log_retention,
        level=app_config.log_level
    )
    
    logger.info("=" * 60)
    logger.info(f"{app_config.app_name} v{app_config.version}")
    logger.info("=" * 60)
    
    # Create background service
    service = DesktopBackgroundService()
    
    # Start file monitoring if enabled
    if app_config.watch_downloads_folder:
        monitoring_thread = threading.Thread(
            target=start_file_monitoring,
            args=(service,),
            daemon=True
        )
        monitoring_thread.start()
    
    # Run service
    try:
        if app_config.enable_background_service and app_config.tray_icon_enabled:
            service.run()
        else:
            logger.info("Running dashboard directly (background service disabled)")
            launch_dashboard(port=app_config.gradio_port)
    
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
        service.quit_application()
    
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
