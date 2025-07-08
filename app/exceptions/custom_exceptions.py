class AppException(Exception):
    def __init__(self, code: str, message: str, status_code: int):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class GameSessionNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            code="SESSION_NOT_FOUND",
            message="Game session not found",
            status_code=404,
        )


class NotOwnerException(AppException):
    def __init__(self):
        super().__init__(
            code="NOT_OWNER",
            message="You are not the owner of this game session",
            status_code=403,
        )


class SessionAlreadyStoppedException(AppException):
    def __init__(self):
        super().__init__(
            code="SESSION_ALREADY_STOPPED",
            message="This session has already been stopped",
            status_code=400,
        )


class InvalidCredentialsException(AppException):
    def __init__(self):
        super().__init__(
            code="INVALID_CREDENTIALS",
            message="Invalid email or password",
            status_code=401,
        )

class SessionExpiredException(AppException):
    def __init__(self):
        super().__init__(
            code="SESSION_EXPIRED",
            message="This game session has expired",
            status_code=410
        )

#for generic exceptions with a generic error message
class GenericException(AppException):
    def __init__(self, message: str):
        super().__init__(
            code="UNKNOW_ERROR",
            message=message,
            status_code=500,
        )