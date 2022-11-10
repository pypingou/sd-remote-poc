import socket
import sys
import conf

data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
for node in conf.NODES:
    print(f"Connecting to {node}:{conf.PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((node, conf.PORT))
        sock.sendall(bytes(data + "\n", "utf-8"))
        print("Sent:     {}".format(data))
        stop = False
        while 1:

            # Receive data from the server and shut down
            received = str(sock.recv(1024), "utf-8")
            # print(received, received.encode("utf-8"))
            if "\nEOT" in received:
                received = received.replace("\nEOT", "")
                stop = True
            if received:
                print("Received: {}".format(received))
            if stop:
                break
