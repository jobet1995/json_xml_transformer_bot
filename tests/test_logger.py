import unittest
import logging
from src.logger import get_logger

class TestLogger(unittest.TestCase):
    """Unit tests for logger.py"""

    def test_logger_creation(self):
        """Test that get_logger returns a logging.Logger instance"""
        logger = get_logger("test_logger")
        self.assertIsInstance(logger, logging.Logger)

    def test_logger_levels(self):
        """Test logging messages at different levels"""
        logger = get_logger("test_logger_levels")
        # Should not raise exceptions
        try:
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")
            logger.critical("Critical message")
        except Exception as e:
            self.fail(f"Logging raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
