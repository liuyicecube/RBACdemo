"""Unit tests for utility modules"""

import pytest


class TestValidators:
    """Test validators utility"""

    def test_import_validators(self):
        """Test that validators can be imported"""
        from App.Utils.Validators import Validators
        assert Validators is not None


class TestLogger:
    """Test logger utility"""

    def test_import_logger(self):
        """Test that logger can be imported"""
        from App.Utils.Logger import logger
        assert logger is not None


class TestResponseUtils:
    """Test response utility"""

    def test_import_response_utils(self):
        """Test that response utils can be imported"""
        from App.Utils.Response import ResponseUtils
        assert ResponseUtils is not None
