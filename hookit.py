#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from flask import Flask, request

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return 'Hello from Flask! (%s)' % datetime.now().strftime('%Y-%m-%d %H:%M:%S')

@app.route('/github', methods=['GET', 'POST'])
def github():
    with open('test', 'w') as f:
        f.write(request.get_json())
    return ':)'


if __name__ == '__main__':
    app.run()
