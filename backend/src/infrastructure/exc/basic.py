from enum import Enum
from fastapi.responses import JSONResponse
from fastapi import Request


class ErrorCode(Enum):
    E1000_NOT_FOUND = 1000 # 404

    E2000_INVALID_TDATA = 2000 # 400
    E2001_USERNAME_REQ = 2001 # 400
    E2002_FILESIZE = 2002 # 400
    E2003_BADIMG = 2003 # 400

    E3000_UNREGISTERED = 3000 # 401
    E3001_ALREADY_REG = 3001 # 403
    E3002_VERIFY_RESTRICTION = 3002 # 403
    E3003_FOCUS_NOTSELECTED = 3003 # 403
    E3004_SUBSCRIPTION_REQ = 3004 # 403
    E3005_BANNED = 3005 # 403

class HTTPError(Exception):

    def __init__(
            self,
            http_code: int,
            error_code: ErrorCode,
            desc: str = None,
            additional: dict | None = None,
            headers: dict[str, str] | None = None
        ) -> None:
        self.http_code = http_code
        self.error_code = error_code
        self.desc = desc
        self.additional = additional or {}
        self.headers = headers or {}

    def __str__(self) -> str:
        return f"{self.http_code}_{self.error_code!r}: {self.desc}"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(http_code={self.http_code!r}, error_code={self.error_code!r}, desc={self.desc!r})"
    
    @staticmethod
    async def handler(request: Request, exc: "HTTPError") -> JSONResponse:
        return JSONResponse(
            content={
                "code": exc.error_code.value,
                **({"desc": exc.desc} if exc.desc else {}),
                **exc.additional
            },
            status_code=exc.http_code,
            headers=exc.headers
        )

class NotFound(HTTPError):
    def __init__(self) -> None:
        super().__init__(404, ErrorCode.E1000_NOT_FOUND, "Not Found")