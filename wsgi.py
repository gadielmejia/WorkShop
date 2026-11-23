# Entry point for Gunicorn and other WSGI servers.
# Imports the app instance from the src.app module.

from src.app import app  # noqa: F401
