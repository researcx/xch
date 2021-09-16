from flask import request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask import Flask
from flask.views import MethodView
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy

import uuid, time, os, re, signal
import pkg_resources, platform
import json
import logging as logging

logger = logging.getLogger('werkzeug')

config = ""
# all configuration variables available via xch.config['group']['key'] in code
# or {{ config()['group']['key'] }} in templates
if os.environ.get('XCH_DEBUG'):
     config_path = "xch/config/config.debug.json"
elif os.environ.get('XCH_DEMO'):
     config_path = "xch/config/config.demo.json"
else:
     config_path = "xch/config/config.json"

try:
     with open(config_path) as config_file:
          config = json.load(config_file)
except:
     logger.info(f"*** Could not load the config from {config_path}.")
     os.kill(os.getpid(), signal.SIGTERM)
else:
     logger.info(f"* Loaded config from {config_path}.")

app = Flask(__name__, static_url_path=config['site']['static_folder'])

app.config.update(dict(
     SQLALCHEMY_DATABASE_URI=config['server']['database'],
     SQLALCHEMY_TRACK_MODIFICATIONS="false",
     SQLALCHEMY_ECHO=True,
     SECRET_KEY=config['server']['secret'],
     STATIC_FOLDER=config['site']['static_folder'],
     RECAPTCHA_ENABLED=True,
     RECAPTCHA_SITE_KEY=config['hcaptcha']['key'],
     RECAPTCHA_SECRET_KEY=config['hcaptcha']['secret'],
     HCAPTCHA_ENABLED=True,
     HCAPTCHA_SITE_KEY=config['hcaptcha']['key'],
     HCAPTCHA_SECRET_KEY=config['hcaptcha']['secret']
))
app.jinja_env.cache = {}

app.static_url_path=config['site']['static_folder']
app.static_folder=app.root_path + app.static_url_path

logger.info(f"* static_url_path {app.static_url_path}.")
logger.info(f"* static_folder {app.static_folder}.")

logger.info(f"* Loaded database from {config['server']['database']}.")

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

db = SQLAlchemy(app)

if config['hcaptcha']['enabled']:
     from flask_hcaptcha import hCaptcha
     hcaptcha = hCaptcha(app)

import xch.initialize
