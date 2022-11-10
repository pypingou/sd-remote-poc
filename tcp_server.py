import dbus
import socketserver
import conf

bus = dbus.SystemBus()


def call_dbus(action, unit):

    systemd = bus.get_object(
        'org.freedesktop.systemd1',
        '/org/freedesktop/systemd1'
    )

    manager = dbus.Interface(
        systemd,
        'org.freedesktop.systemd1.Manager'
    )
    action = action.lower()

    output = "No processed"
    if action == "status":
        unitobj = manager.LoadUnit(unit)
        obj = bus.get_object('org.freedesktop.systemd1', str(unitobj))
        interface = dbus.Interface(obj, dbus_interface='org.freedesktop.DBus.Properties')
        status = interface.Get('org.freedesktop.systemd1.Unit', 'ActiveState')
        output = str(status)
    elif action == "state":
        unit_state = manager.GetUnitFileState(unit)
        output = str(unit_state)
    elif action == "start":
        output = manager.StartUnit(unit, "fail")
    elif action == "stop":
        output = manager.StopUnit(unit, "fail")
    return output


class MyTCPHandler(socketserver.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        data = self.rfile.readline().strip()
        print("{} wrote:".format(self.client_address[0]))
        print(" ", data)
        data = data.decode("utf-8")
        action, unit = data.split(" ", 1)
        if action in ["status", "state", "start", "stop"]:
            self.request.sendall(f"Executing {data}".encode("utf-8"))
            output = call_dbus(action, unit)
            print(output)
            self.request.sendall(output.encode("utf-8"))
            self.request.sendall(b"\nEOT")


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", conf.PORT

    # Create the server, binding to localhost on port 9999
    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        try:
            server.serve_forever()
        finally:
            server.server_close()
