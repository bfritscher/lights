# -*- coding: utf-8 -*-
from websocket_server import WebsocketServer
import threading
import json
import time
import lights

PORT = 9001

DEFAULT_ANIM = 'TimeAnim'

ANIMATIONS = {
  'AudioAnim': {
    'description': 'Audio visualizer',
    'params': [
      {'type': 'audio'}
    ]
  },
  'SensorAnim': {
    'description': 'Sensor display',
    'params': []
  },
  'UpDownAnim': {
    'description': 'UpDown',
    'params': []
  },
  'WaterAnim': {
    'description': 'Water',
    'params': []
  },
  'TimeAnim': {
    'description': 'Digital clock',
    'params': []
  },
  'RectTestAnim': {
    'description': 'Test rectangle',
    'params': []
  },
  'TestAnim': {
    'description': 'Default arduino anim',
    'params': []
  },
  'CountdownAnim': {
    'description': 'Countdown',
    'params': [{
      'type': 'number',
      'name': 'n',
      'label': 'Seconds',
      'default': 30
    }]
  },
  'ScrollTextAnim': {
    'description': 'Scroll text',
    'params': [{
      'type': 'text',
      'name': 'text',
      'label': 'Text',
      'default': '2016'
    }, {
      'type': 'color',
      'name': 'color',
      'label': 'Color',
      'default': '#FF0000'
    }, {
      'type': 'number',
      'name': 'loop',
      'label': 'Nb times (-1=Loop)',
      'default': 1
    }]
  },
  'BallAnim': {
    'description': 'Ball pong',
    'params': [{
      'type': 'button',
      'label': 'launch random',
      'action': 'launch_random'
    },{
      'type': 'xyclick',
      'action': 'launch_at',
      'label': 'or click coordinate to launch'
    }]
  },
  'GlediatorAnim': {
    'description': 'Glediator ArtNet',
    'params': []
  },
  'DrawboardAnim': {
    'description': 'Interactive Drawboard',
    'params': [{
      'type': 'xyover',
      'action': 'draw_at',
      'label': 'Draw on board',
      'params': [{
        'type': 'color',
        'name': 'color',
        'label': 'Color',
        'default': '#FF0000'
      }]
    }]
  }
}

ANIM_QUEUE = []
QUEUE_ID = 1
CURRENT_ANIM = None


# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    #TO SEND current QUEUE
    server.send_message(client, json.dumps({
      'type': 'config',
      'client_id': client['id'],
      'queue': ANIM_QUEUE,
      'ANIMATIONS': ANIMATIONS,
      'MATRIX_HEIGHT': lights.MATRIX_HEIGHT,
      'MATRIX_WIDTH': lights.MATRIX_WIDTH
    }))


# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])
    CURRENT_ANIM.client_disconnected(client['id'])


def remove_animation(id):
    idx = (i for i, v in enumerate(ANIM_QUEUE) if v['id'] == id).next()
    if idx > 0:
        del ANIM_QUEUE[idx]
    send_queue()


def append_animation(name, params={}, force=False, client_id=None):
    global QUEUE_ID
    animation = {
      'id': QUEUE_ID,
      'name': name,
      'params': params,
      'client_id': client_id
    }
    QUEUE_ID +=1
    if len(ANIM_QUEUE) == 1 and ANIM_QUEUE[0]['name'] == DEFAULT_ANIM:
        force = True
    if force:
        ANIM_QUEUE.insert(1, animation)
        CURRENT_ANIM.stop()
    else:
        ANIM_QUEUE.append(animation)
    send_queue()


# Called when a client sends a message
def message_received(client, server, message):
    # print("Client(%d) said: %s" % (client['id'], message))
    try:
        msg = json.loads(message)

        if msg['type'] == 'anim':
            if ANIMATIONS.has_key(msg['name']):
                force = msg['force'] # can anybody force?
                append_animation(msg['name'], msg['params'], force, client['id'])

        elif msg['type'] == 'action':
            # TODO check that current animation supports action
            # ANIMATIONS[ANIM_QUEUE[0]['name']]['params']
            if hasattr(CURRENT_ANIM, msg['action']):
                getattr(CURRENT_ANIM, msg['action'])(client['id'], msg['params'])

        elif msg['type'] == 'next':
            # stop current anim and play next
            CURRENT_ANIM.stop()
        elif msg['type'] == 'remove':
            # remove anim with id
            remove_animation(msg['id'])
    except:
        print 'msg receive error' #TODO


def send_show_data(data):
    #should be done in thread to not block lights
    try:
        server.send_message_to_all(json.dumps({
          'type': 'data',
          'data': data
        }))
    except:
        pass


def send_queue():
    server.send_message_to_all(json.dumps({
        'type': 'queue',
        'data': ANIM_QUEUE
    }))

server = WebsocketServer(PORT, host='0.0.0.0')
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)


def light_thread():
    global CURRENT_ANIM
    lights.register_listener(send_show_data)
    while True:
        # if queue empty put default anim
        if len(ANIM_QUEUE) == 0:
            append_animation(DEFAULT_ANIM)
        # get first element of queue and play
        anim_data = ANIM_QUEUE[0]
        # TODO handle anim error
        class_ = getattr(lights, anim_data['name'])
        CURRENT_ANIM = class_(anim_data['client_id'], anim_data['params'])
        CURRENT_ANIM.start()
        # block until stopped
        ANIM_QUEUE.pop(0)
        send_queue()

thread = threading.Thread(target=light_thread)
thread.daemon = True
thread.start()


server.run_forever()
