"""ASGI entrypoint."""

from vittavaan.boundary.api import create_app

app = create_app()
