

def error_response(code: int, message: str, details=None):
    return {
        "error": {
            "code": code,
            "message": message,
            "details": details
        }
    }