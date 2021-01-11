from .errors import ERRORS
from django.http import JsonResponse

def return_json(errorCode, result=""):
    response = JsonResponse(
        {
            "status": ERRORS[errorCode]["status"],
            "statusCode": ERRORS[errorCode]["statusCode"],
            "statusMessage": ERRORS[errorCode]["statusMessage"],
            "result": result,
        }
    )
    return response
