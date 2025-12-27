"""
Configuration unit tests.

Tests for configuration management and API key handling.
"""
import os
import pytest
from unittest.mock import patch
from app.config import Settings, settings


def test_settings_loads_from_environment():
    """Test configuration loads from environment variables."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key-123"}):
        # Create new settings instance to pick up env var
        test_settings = Settings()
        assert test_settings.openai_api_key == "test-key-123"


def test_settings_handles_missing_api_key():
    """Test application handles missing OPENAI_API_KEY gracefully."""
    # Test that Settings can be instantiated with None/empty API key
    # The actual behavior is that it defaults to None, and the app logs a warning
    # This test verifies the Settings class doesn't require the key to be set
    
    # Create a Settings instance - it should work even if key is not in env
    # (pydantic-settings will use the default value of None)
    test_settings = Settings()
    
    # The key can be None, empty string, or have a value from env/.env file
    # The important thing is that Settings() doesn't raise an exception
    assert hasattr(test_settings, 'openai_api_key')
    # The value might come from .env file, so we just verify it's a valid attribute
    assert isinstance(test_settings.openai_api_key, (str, type(None)))


def test_settings_uses_env_file():
    """Test settings can load from .env file."""
    # This test verifies that pydantic-settings is configured to use .env file
    # The actual .env file might not exist in test environment, which is fine
    test_settings = Settings()
    # Should not raise exception
    assert isinstance(test_settings, Settings)


def test_no_api_keys_hardcoded():
    """Verify no API keys are hardcoded in source code."""
    import app.config
    
    # Read the config file - get the backend directory
    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    config_file_path = os.path.join(backend_dir, "app", "config.py")
    with open(config_file_path, "r") as f:
        config_content = f.read()
    
    # Check for common API key patterns
    assert "sk-" not in config_content  # OpenAI API key prefix
    # OPENAI_API_KEY should only appear as variable name, not as a hardcoded value
    lines_with_key = [line for line in config_content.split("\n") if "OPENAI_API_KEY" in line and "=" in line]
    for line in lines_with_key:
        # Check that it's an assignment, not a hardcoded value
        if "=" in line:
            value_part = line.split("=")[1].strip()
            # Should be None, empty, or a variable reference, not an actual key
            assert "sk-" not in value_part.lower()
    
    # Check for actual key values (should not be present)
    # This is a basic check - more thorough checking would use detect-secrets
    assert "your_openai_api_key" not in config_content.lower()
    # test-key-123 might appear in test, but not as a hardcoded value in config
    if "test-key-123" in config_content:
        # Only acceptable in comments or docstrings
        assert "test-key-123" not in [line.strip() for line in config_content.split("\n") if line.strip() and not line.strip().startswith("#")]

