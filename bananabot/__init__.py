# -*- coding: utf-8 -*-
#!/usr/bin/python
import sys
import socket
import os
import yaml
from time import localtime, strftime
VERSION = "0.0.1"
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def cur_time():
    return strftime("%m/%d/%Y %H:%M:%S", localtime())


config_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'config.yaml')

if os.path.exists(config_path):
    with open(config_path, 'rt', encoding='utf8') as config:
        config = yaml.safe_load(config.read())
        print("{} [!!] '{}' config loaded.".format(cur_time(), config_path))
else:
    print("No Config Found.")


def utf8encode(inputstr):
    return inputstr.encode(encoding='utf_8')


def utf8decode(inputstr):
    return inputstr.decode(encoding='utf_8')


def mySocket_send(inputstr):
    mySocket.send(utf8encode(inputstr))


def mySocket_msg(chan, msg):
    mySocket_send('PRIVMSG #{} :MrDestructoid {}\n'.format(chan, msg))


def mySocket_connect(config, server):
    if 'irc' not in config[server] or 'oauth' not in config[server] or 'username' not in config[server]:
        sys.exit("{} [!!] Please check your config.".format(cur_time()))

    mySocket.connect(tuple(config[server]['irc']))
    mySocket_send("PASS {} \r\n".format(config[server]['oauth']))
    mySocket_send("NICK {} \r\n".format(config[server]['username']))
    mySocket_send('JOIN #{} \r\n'.format(config[server]['channel']))

    print(
        '{} [OK] Connected to {}:{} as "{}"'.format(cur_time(), config[server][
            'irc'][0], config[server]['irc'][1], config[server]['username']))
