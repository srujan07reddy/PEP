"""Root ASGI entrypoint for local development."""

from apps.platform_console.backend.main import app

__all__ = ["app"]
