# -*- coding: utf-8 -*-
#!/usr/bin/python
import click
import select
import re
import requests
import time
import select
from random import randint
from bananabot import *


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate


def pong():
    print('PONG :pingis')
    mySocket_send('PONG :pingis')


@static_vars(last_show=time.time())
def welcome():
    r = requests.get(config['api-3rdparty']['uptime'])
    if "offline" in utf8decode(r.content):
        return
    if len(config['msg']['onWelcome']) > 0:
        msg = config['msg']['onWelcome'][randint(
            0, len(config['msg']['onWelcome']) - 1)]
        print("{} [OK] {}".format(cur_time(), msg))
        mySocket_msg(config['twitch']['channel'], msg)
        welcome.last_show = time.time()


def check_cmd(msg):
    if msg == config['cmd']['help']:
        show_help()
    elif msg == config['cmd']['uptime']:
        show_uptime()


@static_vars(last_show=0)
def show_help():
    if show_help.last_show == 0 or (time.time() - show_help.last_show
                                    ) > config['cmd']['helpLimitSeconds']:
        show_help.last_show = time.time()
        mySocket_msg(config['twitch']['channel'], config['msg']['showHelp'])
    else:
        print("Limit show help rate")


@static_vars(last_show=0)
def show_uptime():
    if show_uptime.last_show == 0 or (time.time() - show_uptime.last_show
                                      ) > config['cmd']['uptimeLimitSeconds']:
        show_uptime.last_show = time.time()
        r = requests.get(config['api-3rdparty']['uptime'])
        if "offline" in utf8decode(r.content):
            mySocket_msg(config['twitch']['channel'],
                         config['msg']['onOffline'])
        else:
            mySocket_msg(config['twitch']['channel'],
                         config['msg']['showUptime'] + utf8decode(r.content))
    else:
        print("Limit show uptime rate")


@click.command()
def bananabot():
    mySocket_connect(config, 'twitch')
    mySocket_msg(config['twitch']['channel'],
                 config['msg']['onConnected2Channel'])

    privmsg = re.compile('@(.*).tmi.twitch.tv PRIVMSG #(.*) :(.*)\\r')
    onWelcomeEverySeconds = int(config['msg']['onWelcomeEverySeconds'])

    while 1:
        try:
            if (time.time() - welcome.last_show) > onWelcomeEverySeconds:
                welcome()

            sread, swrite, sexc = select.select([mySocket], [], [], 120)		          
            for s in sread:
                data = s.recv(1024)

                if data:
                    msg = utf8decode(data)
                    print(msg)

                    chat_msg = privmsg.findall(msg)
                    if len(chat_msg) > 0:
                        for c in chat_msg:
                            print("[#{}] {}: {}".format(c[1], c[0], c[2]))
                            check_cmd(c[2])

                    if 'PING :' in msg:
                        pong()
            sys.stdout.flush()
        except KeyboardInterrupt:
            mySocket_msg(config['twitch']['channel'],
                         config['msg']['onDisconnected2Channel'])
            mySocket.close()
            sys.exit(0)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise


if __name__ == "__main__":
    bananabot()
