from .basic import ErrorCode, HTTPError


class FocusNotSelected(HTTPError):
    def __init__(self) -> None:
        super().__init__(403, ErrorCode.E3003_FOCUS_NOTSELECTED, "Focus user not selected")