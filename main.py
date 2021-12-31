import socket
import sys
import time

lat_points = []
lon_points = []


call = b'N0CALL'
passcode = b''

server = 'noam.aprs2.net'
port = 14580
message = b'Hello, World'


def set_posit(connection: socket, lat: bytes, lon: bytes, message: bytes):
    packet = b'' + call + b'>APRS,TCPIP*:' + b'!' + \
        lat + b'/' + lon + b'/' + message + b'\n'
    connection.send(packet)
    print(b'sent:' + packet)
    time.sleep(5)


def main():
    points = 0
    if len(lat_points) == len(lon_points):
        points = len(lat_points)
    else:
        print('lat: ' + str(len(lat_points)) +
              '\nlon: ' + str(len(lon_points)))
        print('lat and lon points are not equal')
        sys.exit(1)

    connection: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    connection.connect((server, port))
    r = connection.recv(1024)
    print('server is running: ' + str(r))

    # Logs into the server
    connection.send(b'user ' + call + b' pass ' +
                    passcode + b' vers aprs-draw 0.0.0' b'\n')
    r = connection.recv(1024)
    print('logged in: ' + str(r))

    for i in range(points):
        lat = bytes(lat_points[i], 'utf-8')
        lon = bytes(lon_points[i], 'utf-8')
        set_posit(connection, lat, lon, message)

    connection.close()
    pass


if __name__ == '__main__':
    main()
