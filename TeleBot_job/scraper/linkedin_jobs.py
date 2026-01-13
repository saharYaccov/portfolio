import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

BASE_URL = "https://www.linkedin.com/jobs/search/"

def fetch_jobs(keywords="data", location="Israel", limit=40):
    params = {
        "keywords": keywords,
        "location": location
    }

    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    cards = soup.find_all("div", class_="base-card", limit=limit)

    for card in cards:
        try:
            title = card.find("h3").get_text(strip=True)
            company = card.find("h4").get_text(strip=True)
            link = card.find("a")["href"]

            jobs.append({
                "title": title,
                "company": company,
                "link": link
            })
        except Exception:
            continue

    return jobs
