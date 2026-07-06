"""WSGI entry point used by Vercel and production WSGI servers."""
from app import create_app

app = create_app()
