import xch
from flask import Flask, request, jsonify
from time import strftime
import traceback

import xch.views.index
import xch.views.actions
import xch.views.extras

import xch.models.inject.config

#Run the main app...
if __name__ == '__main__':
    xch.app.run(threaded=True)

#Run the main app...
if __name__ == '__main__':
    xch.app.run()
