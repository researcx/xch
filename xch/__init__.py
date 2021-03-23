from flask import request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask import Flask
from flask.views import MethodView

import uuid, time, os, re, signal
import pkg_resources, platform
import humanize
import logging as logging
logger = logging.getLogger('werkzeug')

config = ""
config_path = "config.json" # all configuration variables available via xch.config['group']['key']

try:
     with open(config_path) as config_file:
          config = json.load(config_file)
except:
     logger.info(f"*** Could not load the config from {config_path}.")
     os.kill(os.getpid(), signal.SIGTERM)
else:
     logger.info(f"* Successfully loaded the config from {config_path}.")

app = Flask(__name__)

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI=config['server']['database'],
    SQLALCHEMY_TRACK_MODIFICATIONS="false",
    SECRET_KEY=config['server']['secret']
))
app.jinja_env.cache = {}

if config['cache']['type'] == "redis":
     print(" * Cache: Redis")
     cache = Cache(app, config={
          'CACHE_TYPE': 'redis',
          'CACHE_KEY_PREFIX': config['redis']['prefix'],
          'CACHE_REDIS_HOST': config['redis']['host'],
          'CACHE_REDIS_PORT': config['redis']['port'],
          'CACHE_REDIS_URL': config['redis']['url']
     })
else:
     print(" * Cache: " + config['cache']['type'])
     cache = Cache(app,config={'CACHE_TYPE': config['cache']['type']})

import xch.initialize
