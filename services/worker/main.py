"""Worker module marker; Celery loads the shared boundary application."""

from vittavaan.boundary.worker import celery_app

__all__ = ["celery_app"]
