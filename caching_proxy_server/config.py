import os
from .logger import setup_logging

if not os.path.exists('data'):
    os.mkdir('data')
logger = setup_logging('data/proxy_server.log')
