# response.py
def success_response(message: str, data: dict = None, status_code: int = 200):
    return {
        "status_code": status_code,
        "message": message,
        "data": data,
        "error": None
    }

def error_response(message: str, error_type: str, status_code: int = 400):
    return {
        "status_code": status_code,
        "message": message,
        "data": None,
        "error": error_type
    }
