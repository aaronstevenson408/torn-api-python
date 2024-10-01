import logging
import os

def setup_logger(name='my_logger', level=logging.CRITICAL):
    """Sets up a logger with a specified name and level.

    Args:
        name (str): The name of the logger. Default is 'my_logger'.
        level (int): The logging level. Default is logging.DEBUG.

    Returns:
        tuple: A tuple containing the logger and its file handler.
    """
    # Create a directory for log files if it doesn't exist
    log_directory = 'logs'
    os.makedirs(log_directory, exist_ok=True)

    # Define the log file path based on the logger name
    log_file = os.path.join(log_directory, f'{name}.log')

    # Create a logger object with the specified name
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create a file handler that logs debug and higher level messages to the specified log file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    # Create a console handler that logs warning and higher level messages to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)

    # Create a formatter to specify the output format of log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)  # Set the formatter for the file handler
    console_handler.setFormatter(formatter)  # Set the formatter for the console handler

    # Add the file and console handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger, file_handler  # Return the logger and file handler for future use

def close_logger(logger, file_handler):
    """Closes the logger's handlers.

    Args:
        logger (logging.Logger): The logger to close.
        file_handler (logging.FileHandler): The file handler associated with the logger.
    """
    # Remove the file handler from the logger
    logger.removeHandler(file_handler)
    
    # Close the file handler to release any resources
    file_handler.close()
