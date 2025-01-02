import os
import sys
import time
from appLogger import AppLogger
import subprocess
from datetime import datetime
from pathlib import Path

# Setup logger
appLogger = AppLogger()

# Constants and paths
PACKAGE_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))

# Function to run the main processing
def run_main_process():
    try:
        # Log that the process is starting
        appLogger.getLogger().debug(f"Starting the main process at {datetime.now()}")
        
        # Call the main.py script directly via subprocess
        command = ['python', '/code/src/greenproject/main.py']  # Assuming main.py is in the same directory
        subprocess.run(command, check=True)  # This will run the main script
        appLogger.getLogger().debug(f"Main process finished successfully at {datetime.now()}")
    
    except subprocess.CalledProcessError as e:
        appLogger.getLogger().error(f"Error occurred while running the main process: {e}")

# Function to schedule the main process
def schedule_process(interval=180):  # Default interval of 3 minutes (180 seconds)
    while True:
        run_main_process()
        # Wait for the next scheduled time
        appLogger.getLogger().debug(f"Waiting for next cycle at {datetime.now()}")
        time.sleep(interval)  # Sleep for the interval before calling the process again

if __name__ == "__main__":
    # Call the function to schedule the process with a 3-minute interval
    schedule_process(interval=180)  # 3 minutes = 180 seconds
