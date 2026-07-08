from dataclasses import dataclass
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


@dataclass
class ValidationResult:
    reachable: bool
    status_code: int
    html: str


def fetch_homepage(url):
    try:
        request = Request(
            url,
            headers={
                "User-Agent": "203local Data Engine/1.0"
            },
        )

        with urlopen(request, timeout=15) as response:
            html = response.read().decode("utf-8", errors="ignore")

            return ValidationResult(
                reachable=True,
                status_code=response.status,
                html=html,
            )

    except (HTTPError, URLError):
        return ValidationResult(
            reachable=False,
            status_code=0,
            html="",
        )
