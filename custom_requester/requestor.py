import json
import logging
import os
from typing import Optional, Dict, Any

import requests


class CustomRequester:
    """
    Кастомный реквестер //
    """
    base_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def __init__(self, session: requests.Session, base_url: str):
        self.session = session
        self.base_url = base_url.rstrip("/")  # убираем лишний / в конце
        self.headers = self.base_headers.copy()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def send_request(
            self,
            method: str,
            endpoint: str,
            data: Optional[Dict] = None,
            params: Optional[Dict] = None,
            headers: Optional[Dict] = None,
            files: Optional[Dict] = None,
            expected_status: int = 200,
            need_logging: bool = True,
            **kwargs: Any,
    ) -> requests.Response:
        """
        Универсальный метод отправки запроса.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        # Формируем заголовки: базовые + переданные
        request_headers = self.headers.copy()
        if headers:
            request_headers.update(headers)

        response = self.session.request(
            method=method.upper(),
            url=url,
            json=data if data and method not in ("GET", "HEAD") else None,
            params=params,
            headers=request_headers,
            files=files,
            **kwargs
        )

        if need_logging:
            self.log_request_and_response(response)

        if response.status_code != expected_status:
            raise ValueError(
                f"Unexpected status code: {response.status_code}. Expected: {expected_status}\n"
                f"Response body: {response.text}"
            )

        return response

    def _update_session_headers(self, **kwargs) -> None:
        """
        Обновление заголовков сессии (например Authorization).
        """
        self.headers.update(kwargs)
        self.session.headers.update(self.headers)

    def log_request_and_response(self, response: requests.Response) -> None:
        try:
            request = response.request
            GREEN = '\033[32m'
            RED = '\033[31m'
            RESET = '\033[0m'

            # Формируем заголовки для curl
            headers_str = " \\\n".join([f"-H '{k}: {v}'" for k, v in request.headers.items()])

            full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"

            # Тело запроса (для POST/PUT/PATCH)
            body = ""
            if hasattr(request, 'body') and request.body is not None:
                if isinstance(request.body, bytes):
                    try:
                        body = request.body.decode('utf-8')
                    except UnicodeDecodeError:
                        body = "[binary data]"
                else:
                    body = str(request.body)
                body = f"-d '{body}' \n" if body != '{}' else ""

            self.logger.info(f"\n{'=' * 40} REQUEST {'=' * 40}")
            self.logger.info(
                f"{GREEN}{full_test_name}{RESET}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers_str} \\\n"
                f"{body}"
            )

            response_data = response.text
            try:
                response_data = json.dumps(json.loads(response.text), indent=4, ensure_ascii=False)
            except json.JSONDecodeError:
                pass

            self.logger.info(f"\n{'=' * 40} RESPONSE {'=' * 40}")
            if not response.ok:
                self.logger.info(
                    f"\tSTATUS_CODE: {RED}{response.status_code}{RESET}\n"
                    f"\tDATA: {RED}{response_data}{RESET}"
                )
            else:
                self.logger.info(
                    f"\tSTATUS_CODE: {GREEN}{response.status_code}{RESET}\n"
                    f"\tDATA:\n{response_data}"
                )
            self.logger.info(f"{'=' * 80}\n")
        except Exception as e:
            self.logger.error(f"\nLogging failed: {type(e).__name__}: {e}")
