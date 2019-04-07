"""

"""

import pythonosc.osc_server
import pythonosc.dispatcher
import threading

actions = {}

def log(msg):
    print("osc: {}".format(msg), file=open('/home/pi/log','a'))

class OSCDispatcher(pythonosc.dispatcher.Dispatcher):
    """This is the class of the OSC dispatcher."""

    def handlers_for_address(self, path):
        """yields Handler namedtuples matching the given OSC pattern."""
        def callback(path, *args):
            try:
                log('Calling {} for {}'.format(actions[path].__name__, path))
                actions[path](*args)
            except KeyError:
                log('No callback for {}'.format(path))

        yield pythonosc.dispatcher.Handler(callback, [])

def serve(adress, actions_):
    """
    Serve forever on the given adresses.

    Start to threading the osc server.
    """
    global actions
    actions = actions_

    dispatcher = OSCDispatcher()
    osc_server = pythonosc.osc_server.OSCUDPServer(adress, dispatcher)
    osc_server_thread = threading.Thread(target=osc_server.serve_forever)
    osc_server_thread.start()
    log("Serving at {}:{}".format(*adress))
    log("Handling {}".format(", ".join(actions.keys())))
