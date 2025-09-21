from fastapi import HTTPException

class NotFound(HTTPException):
    def __init__(self, detail="Not found"):
        super().__init__(status_code=404, detail=detail)

class Conflict(HTTPException):
    def __init__(self, detail="Conflict"):
        super().__init__(status_code=409, detail=detail)

class BadRequest(HTTPException):
    def __init__(self, detail="Bad request"):
        super().__init__(status_code=400, detail=detail)
