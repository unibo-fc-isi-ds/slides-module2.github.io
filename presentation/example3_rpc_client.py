from snippets.lab3 import Client, address
from snippets.lab4.users import *
from snippets.lab4.example1_presentation import serialize, deserialize, Request, Response


class ClientStub:
    def __init__(self, server_address: tuple[str, int]):
        self.__server_address = address(*server_address) # memorize the server address

    def rpc(self, name, *args):
        client = Client(self.__server_address) # create a new TCP client instance
        try:
            print('# Connected to %s:%d' % client.remote_address)
            request = Request(name, args) # create a new request
            print('# Marshalling', request, 'towards', "%s:%d" % client.remote_address)
            request = serialize(request) # serialize the request
            print('# Sending message:', request.replace('\n', '\n# '))
            client.send(request) # send the request
            response = client.receive() # receive the response
            print('# Received message:', response.replace('\n', '\n# '))
            response = deserialize(response) # deserialize the response
            assert isinstance(response, Response)
            print('# Unmarshalled', response, 'from', "%s:%d" % client.remote_address)
            if response.error: # if an error occurred:
                raise RuntimeError(response.error) # raise the error
            return response.result # otherwise, return the result
        finally: # in any case, before exiting:
            client.close() # close the connection
            print('# Disconnected from %s:%d' % client.remote_address)


class RemoteUserDatabase(ClientStub, UserDatabase):
    def __init__(self, server_address):
        super().__init__(server_address)

    # notice how the following methods are implemented by RPC

    def add_user(self, user: User):
        return self.rpc('add_user', user)

    def get_user(self, id: str) -> User:
        return self.rpc('get_user', id)

    def check_password(self, credentials: Credentials) -> bool:
        return self.rpc('check_password', credentials)
