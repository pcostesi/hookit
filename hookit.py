#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import datetime 
import hashlib
import hmac

from flask import Flask, request
from flask_peewee.db import Database
from peewee import TextField, DateTimeField, BooleanField

# settings

DATABASE = {
        'name': 'hooks.db',
        'engine': 'peewee.SqliteDatabase',
        }
DEBUG = True
SECRET_KEY = 'this should be a secret key'

# app

app = Flask(__name__)
app.config.from_object(__name__)
db = Database(app)


# models

class Event(db.Model):
    delivery_code = TextField()
    delivered = DateTimeField(default=datetime.datetime.now)
    dispatched = BooleanField(default=False)


class PushEvent(Event):
    full_repo_name = TextField()
    pusher = TextField()
    ref = TextField()
    head = TextField()

    def __repr__(self):
        return self.delivery_code, self.full_repo_name, self.pusher, self.ref, self.head

    def __str__(self):
        return str(self.__repr__())


class Recipe(db.Model):
    name = TextField()
    trigger = TextField()
    reactor = TextField()


# helpers

def verify_signature(sig, data):
    key = app.config['GH_SIGNATURE_KEY']
    hasher_name, code = sig.split('=')
    hasher = getattr(hashlib, hasher_name)
    the_hmac = hmac.new(key, data, hasher)
    return code == the_hmac.hexdigest()


def dispatch_event(event_type, delivery_code, message):
    event = None
    if event_type == 'push':
        # create PushEvent
        event = PushEvent(
                    delivery_code=delivery_code,
                    full_repo_name=message['repository']['full_name'],
                    pusher=message['pusher']['name'],
                    ref=message['ref'],
                    head=message['head_commit']['id']
                )
        event.save()
    return event


# routes and views and stuff

@app.route('/')
def index():
    return 'Hello from Flask! (%s)' % datetime.now().strftime('%Y-%m-%d %H:%M:%S')

@app.route('/github', methods=['GET', 'POST'])
def github():
    if request.method == 'POST':
        message = request.get_json()
        delivery_code = request.headers.get('X-GitHub-Delivery', 'unknown')
        event_type = request.headers.get('X-GitHub-Event', 'unknown')
        signature = request.headers.get('X-Hub-Signature', None)

        if not verify_signature(signature, request.data):
            return 'Invalid key', 500
        event = dispatch_event(event_type, delivery_code, message)
    return 'Ok'


if __name__ == '__main__':
    app.run()
