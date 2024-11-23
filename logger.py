import logging

# Configure the root logger
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Create a logger for your application
logger = logging.getLogger(__name__)