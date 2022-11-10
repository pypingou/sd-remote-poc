import dbus
import json
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop
import socket

import conf


def signal_handler(*args, **kwargs):
    for i, arg in enumerate(args):
        print("arg:%d        %s" % (i, str(arg)))
    print('kwargs:')
    print(kwargs)
    print('---end----')
    data = json.dumps({"args": [str(s) for s in args], "kwargs": {k:str(kwargs[k]) for k in kwargs}})

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((conf.MAINHOST, conf.PORT))
        sock.sendall(bytes(data + "\n", "utf-8"))


DBusGMainLoop(set_as_default=True)
bus = dbus.SystemBus()
#register your signal callback
bus.add_signal_receiver(
    signal_handler,
    bus_name='org.freedesktop.systemd1',
    interface_keyword='interface',
    member_keyword='member',
    path_keyword='path',
    message_keyword='msg',
)

loop = GLib.MainLoop()
loop.run()
