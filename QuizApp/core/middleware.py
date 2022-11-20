import logging
import time


logger = logging.getLogger(__name__)


class TimingMiddleware:

    def __init__(self, get_response) -> None:
        self._get_response = get_response

    def __call__(self, request):
        previous_time = time.time()
        response = self._get_response(request)
        logger.info('User: %s, path: %s, Lead time: %s', request.user, request.path, time.time() - previous_time)
        return response