class ErrorResponseModel(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message
        }


class ValidationError(Exception):
    def __init__(self, loc=None, msg="", type_="unkown"):
        if loc is None: loc = []
        self.loc = loc
        self.msg = msg
        self.type_ = type_

    def to_dict(self):
        return {
            "loc": self.loc,
            "msg": self.msg,
            "type": self.type_
        }


class HTTPValidationError(Exception):
    code = 422

    def __init__(self, *args: ValidationError):
        self.detail = args

    def to_dict(self):
        return {
            "detail": [x.to_dict() for x in self.detail]
        }


class UnauthorizedUserError(Exception):
    code = 401
    title = "Response 401 Unauthorized User"

    def to_dict(self):
        return {
            "code": self.code,
            "title": self.title
        }

    # :TODO title
