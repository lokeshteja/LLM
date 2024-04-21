import logging
import os
from datetime import datetime

# Corrected the date format string
log_filename = datetime.now().strftime('%m_%d_%Y_%H_%M_%S') + '.log'

file_path = os.path.join(os.getcwd(), 'logs')
os.makedirs(file_path, exist_ok=True)

log_file_path = os.path.join(file_path, log_filename)

# Set up logging
logging.basicConfig(level=logging.INFO,  # Corrected the constant
                    filename=log_file_path,
                    format='%(asctime)s - %(levelname)s - %(message)s'  # Example format
                    )

# Example of using the logger
logging.info("This is an info message.")
