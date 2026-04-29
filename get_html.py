import requests

URL = "https://www.onlinejobs.ph/jobseekers/jobsearch?jobkeyword=data"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def save_html():
    response = requests.get(URL, headers=headers)

    # Save raw HTML
    with open("page.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    print("HTML saved as page.html")


if __name__ == "__main__":
    save_html()