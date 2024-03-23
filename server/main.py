from http.server import ThreadingHTTPServer

import threading, time
import ssl, signal
import os, pathlib

os.chdir(str(pathlib.Path(__file__).parent))
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Internal
from utils.utils import logger
from handler.request_router import RequestRouter
from handler.redirect_request_router import RedirectRequestRouter

import config

# logger.set_level(logger.DEBUG)
# logger.set_file("abc.log")

""" Handle signal """
running = True
server  = None
def signal_handler(sig, _):
    global server, running
    if server is not None:
        threading.Thread(target=ThreadingHTTPServer.shutdown, args=[server]).start()
        threading.Thread(target=ThreadingHTTPServer.server_close, args=[server]).start()
        logger.info("Recvice '%s', Shutdown server on port %s" % (str(signal.Signals(sig).name), config.PORT))

    if running == False:
        logger.warn("Recvice '%s', Force exit" % str(signal.Signals(sig).name))
        exit(1)
    else: running = False

# Register SIGINT
signal.signal(signal.SIGINT, signal_handler)

def runRedirectHTTP(port=80):
    threading.Thread(target=ThreadingHTTPServer.serve_forever, args=[ThreadingHTTPServer(('', port), RedirectRequestRouter)]).start()
    logger.info('Redirect server running on http port %s' % port, cert_file = config.CERTIFICATE_PATH)

if __name__ == "__main__":
    server = ThreadingHTTPServer(('', config.PORT), RequestRouter)
    if config.USE_TLS:
        server.socket = ssl.wrap_socket(server.socket, server_side = True, certfile = config.CERTIFICATE_PATH, ssl_version = ssl.PROTOCOL_TLS)
        logger.info('Server running on https port %s' % config.PORT, cert_file = config.CERTIFICATE_PATH)
        runRedirectHTTP()
    else:
        logger.info('Server running on http port %s' % config.PORT)

    running_thread = threading.Thread(target=ThreadingHTTPServer.serve_forever, args=[server])
    running_thread.start()

    while running and running_thread.is_alive(): time.sleep(1)

    running_thread.join(1)
