import threading
import socket

from src import router as Router


class Main:
    def __init__(self):
        self.router = Router.Router("Main Router")

    def run(self):
        host = '127.0.0.1'
        port = 12345

        with socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM) as interface:
            interface.bind((host,
                            port))
            interface.listen()

            while True:
                connection, address = interface.accept()
                t = threading.Thread(target=self.router.handle_connection,
                                     args=(connection, address))
                t.start()


if __name__ == '__main__':
    main = Main()
    main.run()
