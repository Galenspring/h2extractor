from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/extract_h2_headings", methods=["POST"])
def extract_h2_headings():
    data = request.get_json()
    url = data.get("url")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        h2s = [tag.get_text(strip=True) for tag in soup.find_all("h2")]
        return jsonify({
            "headings": h2s,
            "error": None
        })
    except Exception as e:
        return jsonify({
            "headings": [],
            "error": str(e)
        })

if __name__ == "__main__":
    app.run()
