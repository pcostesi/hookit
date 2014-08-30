#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from hookit import *

def consume_event(event):
    event.dispatched = True
    event.save()
    return event


def process_events(events):
    for event in events:
        print event
        #consume_event(event)
        #recipe = find_recipe(event)
        #run_recipe(recipe)


if __name__ == '__main__':
    try:
        PushEvent.create_table()
        Recipe.create_table()
    except:
        pass

    events = PushEvent.select().where(PushEvent.dispatched==False)
    process_events(events)
