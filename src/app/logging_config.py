import logging

def configure_logging():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("app.log"),  # Save logs to a file
            logging.StreamHandler()  # Print logs to the console
        ]
    )
