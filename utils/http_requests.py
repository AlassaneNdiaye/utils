import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def build_safe_http_request(default_timeout: int = 5, retries: int = 3):
    class TimeoutHTTPAdapter(HTTPAdapter):
        def send(self, request, **kwargs):
            timeout = kwargs.get('timeout')
            if timeout is None:
                kwargs['timeout'] = default_timeout
            return super().send(request, **kwargs)

    retry_strategy = Retry(
        total=retries,
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_factor=1  # exponential backoff
    )

    adapter = TimeoutHTTPAdapter(max_retries=retry_strategy)

    safe_http_request = requests.Session()
    safe_http_request.mount('https://', adapter)
    safe_http_request.mount('http://', adapter)

    return safe_http_request


safe_http_request = build_safe_http_request()
