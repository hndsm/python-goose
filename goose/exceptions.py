# -*- coding: utf-8 -*-

class ConnectionError(Exception):
    pass

class DatabaseError(Exception):
    pass

class NotAuthorizedError(Exception):
    pass

class NotFoundError(Exception):
    pass

class TimeoutError(Exception):
    pass

class TooManyRedirectsError(Exception):
    pass

class UnexpectedRedirectError(Exception):
    pass

class UnknownError(Exception):
    pass                             
