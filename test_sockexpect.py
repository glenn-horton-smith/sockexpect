"""Tests for sockexpect."""
import pytest
import sockexpect


@pytest.fixture(scope="session")
def server_connection():
    """A pytest test fixture that provides a test TCPServer."""
    # pylint: disable=import-outside-toplevel
    import socketserver
    import socket
    import threading
    class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
        """ThreadedTCPRequestHandler written along example in socketserver documentation."""
        def handle(self):
            """Handler loop."""
            while True:
                try:
                    data = self.request.recv(1024)
                except ConnectionResetError:
                    return
                if not data:
                    break
                if data.startswith(b'ID'):
                    response = b'ID check test received: '+data+b'\n'
                elif data.startswith(b'ADD '):
                    try:
                        _, s1, s2 = data.split()
                        i = int(s1) + int(s2)
                        response = (b'ADD test: ' + s1 + b'+' + s2 +
                                    b'=' + bytes(repr(i), 'ascii') + b'\n')
                    except Exception:
                        response = b'ADD parse failure\n'
                else:
                    response = b'Unknown command.\n'
                self.request.sendall(response)
    class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        """ThreadedTCPServer using mix-in, written along example in socketserver documentation."""
        # pass
    #
    server = ThreadedTCPServer(('localhost', 0), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)
    sock = socket.socket()
    sock.connect((ip, port))
    sock.settimeout(0.2)
    yield sock
    sock.close()

def test_0(server_connection): # pylint: disable=redefined-outer-name
    """A mono-test that checks send, sendline, and expect in several ways."""
    s = sockexpect.SockExpect(server_connection)
    s.send(b'ID\r\n')
    s.expect(br'ID')
    assert s.before == b''
    assert s.after == b'ID check test received: ID\r\n\n'
    s.sendline(b'ID gahs')
    s.expect(br'gahs')
    assert s.before.endswith(b'ID check test received: ID ')
    assert s.after == b'gahs\r\n\n'
    s.after.clear()
    s.sendline(b'ADD 2 3')
    s.expect(br'ADD test: 2\+3=5')  # Note + in regexp must be escaped.
    assert s.before == b''
    assert s.after == b'ADD test: 2+3=5\n'
    s.sendline(b'ID')
    with pytest.raises(Exception):
        s.expect(br'Hi!')
    assert s.after != 'Hi!'
