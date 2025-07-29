import os

# Default to 'dev' unless DJANGO_ENV is explicitly set to 'prod'
ENV = os.getenv("DJANGO_ENV", "dev")

if ENV == "prod":
    from .prod import *
else:
    from .dev import *