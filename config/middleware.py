from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from fastapi import Request

import logging


class LogMiddleware(BaseHTTPMiddleware):
    """
    Middleware для логирования HTTP-запросов и ответов.
    """
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        Обрабатывает входящий HTTP-запрос и передает его следующему обработчику.
        Логирует информацию о запросе, включая метод и URL, а также статус
        ответа, возвращаемого после обработки запроса.

        :param request: объект запроса, представляющий входящий HTTP-запрос
        :param call_next: функция, которая обрабатывает запрос и возвращает ответ
        :return: объект ответа, полученный от следующего обработчика
        """
        logging.info(f'Request: {request.method} {request.url}')
        response = await call_next(request)
        logging.info(f'Response: {response.status_code}')
        return response
