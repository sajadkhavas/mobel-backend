from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None

    default_code = getattr(exc, "default_code", "api_error")
    response.data = {
        "error": {
            "code": default_code,
            "message": "Request could not be processed.",
            "details": response.data,
        }
    }
    return response
