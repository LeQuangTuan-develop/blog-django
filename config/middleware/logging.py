import logging

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log request information here
        logger.info(
            f"Method: {request.method}, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR')}")

        response = self.get_response(request)

        return response
