import requests
import random
import json
import websocket
import os

TOKEN = 'Service code for you application'

def get_server_key(token):
    r=requests.get('https://api.vk.com/method/streaming.getServerUrl?access_token={}&v=5.80'.format(token))
    data=r.json()
    print(data)
    return {'server':data['response']['endpoint'], 'key':data['response']['key']}

def Stream_listen():
    websocket.enableTrace(True)
    ws=websocket.WebSocketApp('wss://{}/stream?key={} '.format(stream['server'], stream['key']), on_message = on_message, on_error = on_error, on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

def set_rule(rule):
    rule_params = {'rule':{'value':rule,'tag':'tag_'+str(random.randint(11111, 99999))}}
    headers = {'content-type': 'application/json'}
    r = requests.post("https://{}/rules?key={}".format(stream['server'], stream['key']), data=json.dumps(rule_params), headers=headers)
    data = r.json()
    if data['code'] == 200:
       print('Tag added')
       return True
    else:
       print('Error!', data)
       return False

def get_rules():
    r=requests.get('https://{}/rules?key={}'.format(stream['server'], stream['key']))
    data = r.json()
    if data['code'] != 200:
       print('Error!')
       return False

    elif data['rules'] == None:
       print('No current rules')
       return None

    rules='Current rules:\n'
    for rule in data['rules']:
        rules += (rule['value']+' (tag: '+rule['tag']+')\n')
    print (rules)
    return data['rules']

def delete_rule(tag):
    headers={'content-type':'application/json'}
    rule_params = {'tag':tag}
    r=requests.delete('https://{}/rules?key={}'.format(stream['server'], stream['key']), data = json.dumps(rule_params), headers=headers)
    data=r.json()
    if data['code'] == 200:
       print('Tag removed')
       return True
    else:
       print('Error!', data)
       return False

def delete_all_rules(rules):
    headers = {'content-type': 'application/json'}
    for rule in rules:
        rule_params = {'tag': rule['tag']}
        r=requests.delete('https://{}/rules?key={}'.format(stream['server'], stream['key']), data = json.dumps(rule_params), headers=headers)
        data = r.json()
        if data['code'] == 200:
           print('Tag {} removed'.format(rule['value']))
        else:
           print('Error!', data)

def on_message(ws, message):
    print('>>> recieve message', message)

def on_error(ws, error):
    print('>>> error thead', error)

def on_close(ws):
    print('>>> close thead')

def on_open(ws):
    print('>>> open thead')


if os.path.exists('stream.cfg'):
   f=open('stream.cfg')
   stream=dict()
   stream['server'] = f.readline().replace('\n', '')
   stream['key'] = f.readline().replace('\n', '')
   f.close()
else:
  stream = get_server_key(TOKEN)
  f=open('stream.cfg', 'w')
  f.write(stream['server']+'\n'+stream['key'])
  f.close()

menu = '> Change the new key(1)\n> Remove key(2)\n> Remove all keys(3)\n> Start listening(4)'
while True:
      rules=get_rules()
      print (menu)
      trig=input('>>> ')
      if trig == '1':
         key = input('Change the key: ')
         if key != '':
            set_rule(key)
      elif trig == '2':
           tag = input('Input the tag of key to delete: ')
           if tag != '':
              delete_rule(tag)
      elif trig == '3':
           trig2 = input('Are you sure(y/n)?')
           if trig2 in ['y', 'Y']:
              delete_all_rules(rules)
      elif trig == '4':
           Stream_listen()


