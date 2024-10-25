from snippets.lab3 import Server
from snippets.lab4.users.impl import InMemoryUserDatabase
from snippets.lab4.example1_presentation import serialize, deserialize, Request, Response
import traceback


class ServerStub(Server):
    def __init__(self, port):
        super().__init__(port, self.__on_connection_event) # start listening on port upon creation, call callback upon incoming connections
        self.__user_db = InMemoryUserDatabase() # hold a reference to the actual server

    def __on_connection_event(self, event, connection, address, error): # whenever a connection event occurs...
        match event:
            case 'listen': # ... if it's the server starting to listen:
                print('Server listening on %s:%d' % address) # then log the address it's listening on
            case 'connect': # ... if it's a new connection:
                connection.callback = self.__on_message_event # then set the callback for incoming messages (this will start a thread under the hood)
            case 'error': # ... if an error occurs while handling the connection:
                traceback.print_exception(error) # then log it
            case 'stop': # ... if the server stops listening:
                print('Server stopped') # log this information before quitting

    def __on_message_event(self, event, payload, connection, error): # whenever a message event occurs...
        match event:
            case 'message': # ... if it's a new message:
                print('[%s:%d] Open connection' % connection.remote_address) # log the connection
                request = deserialize(payload) # deserialize the ingoing message
                assert isinstance(request, Request) # make sure it's a Request object (raise an error if not)
                print('[%s:%d] Unmarshall request:' % connection.remote_address, request) # log the request
                response = self.__handle_request(request) # handle the request, compute the response
                connection.send(serialize(response)) # serialize the response and send it back
                print('[%s:%d] Marshall response:' % connection.remote_address, response) # log the response
                connection.close() # close the connection (this RPC is over!)
            case 'error': # ... if an error occurs while handling the message:
                traceback.print_exception(error) # log it
            case 'close': # ... if the connection closes:
                print('[%s:%d] Close connection' % connection.remote_address) # log this information

    def __handle_request(self, request): # this is where the actual function to execute is selecte and executed
        try:
            method = getattr(self.__user_db, request.name) # get the method from the user database
            result = method(*request.args) # call the method with the arguments, store the result
            error = None # no error occurred in this case
        except Exception as e: # if an error occurs:
            result = None # no result in case of an error
            error = " ".join(e.args) # store the error message
        return Response(result, error) # return a Response object with the result and the error message


if __name__ == '__main__':
    import sys
    server = ServerStub(int(sys.argv[1])) # server stub will listen on the port provided as argument
    while True:
        try:
            input('Close server with Ctrl+D (Unix) or Ctrl+Z (Win)\n')
        except (EOFError, KeyboardInterrupt):
            break
    server.close()
