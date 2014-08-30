#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from flask_peewee.utils import get_dictionary_from_model
from yapbl import PushBullet

from hookit import *

msg = '''
A github push has been received by our hook system.
The message delivery code was {delivery_code}.
The full repo name is {full_repo_name}
And the push was done to {ref} ({head}) by {pusher}

:)
'''

config = {
        'pb_key': 'YOUR_KEY_HERE'
        }

def pushbullet_reactor(config, context):
    key = config.get('pb_key')
    pb = PushBullet(key)
    pb.push_note('Github event detected', msg.format(**context))



def consume_event(event):
    event.dispatched = True
    event.save()
    return event


def process_events(events):
    for event in events:
        print event
        pushbullet_reactor(config, get_dictionary_from_model(event))
        consume_event(event)


if __name__ == '__main__':
    try:
        PushEvent.create_table()
        Recipe.create_table()
    except:
        pass

    events = PushEvent.select().where(PushEvent.dispatched==False)
    process_events(events)
