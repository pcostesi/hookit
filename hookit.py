#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello from Flask! (%s)' % datetime.now().strftime('%Y-%m-%d %H:%M:%S')
