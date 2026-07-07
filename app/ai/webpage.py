import re
import requests
from bs4 import BeautifulSoup


def clean_text(text):
    text = re.sub(r"\s+", " ", text or "")
    return text.strip()


def extract_text(url, max_chars=5000):
    if not url or str(url).lower() == "nan":
        return ""

    url = str(url).strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "203local Data Engine"},
        )
    except Exception as e:
        return f"ERROR: {e}"

    if response.status_code != 200:
        return f"ERROR: Status code {response.status_code}"

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    text = soup.get_text(" ")
    text = clean_text(text)

    return text[:max_chars]


if __name__ == "__main__":
    print(extract_text("https://losalebrijesct.com"))

    