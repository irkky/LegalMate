import logging
from logging.handlers import RotatingFileHandler

def configure_logging(app):
    handler = RotatingFileHandler(
        'legalmate.log',
        maxBytes=1024*1024*10,  # 10MB
        backupCount=10
    )
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s'
    )
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)