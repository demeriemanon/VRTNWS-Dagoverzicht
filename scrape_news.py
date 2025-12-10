# scrape_news.py

import requests
from bs4 import BeautifulSoup
import datetime

def get_news_summary():
    URL = "https://www.vrt.be/vrtnws/nl.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(URL, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Zoek naar de artikelen in de hoofdsectie.
        articles = soup.select('.vrt-cluster-item__body a[href^="/vrtnws/nl/"]') 

        news_items = []

        # Neem de top 5 artikelen
        for article in articles[:5]:
            title = article.get_text(strip=True)
            link = "https://www.vrt.be" + article.get('href')

            if title and len(title) > 10:
                news_items.append(f"- **{title}**\n  (Lees meer: {link})")

        if not news_items:
            return "Kon geen nieuwsartikelen vinden. De selector (HTML pad) is mogelijk veranderd of de pagina laadt niet correct."

        vandaag = datetime.date.today().strftime("%d-%m-%Y")
        summary = f"# 📰 VRT NWS Dagoverzicht van {vandaag}\n\nDe belangrijkste feiten:\n\n"
        summary += "\n".join(news_items)
        summary += "\n\n---\n*Automatisch gegenereerd door GitHub Actions.*"

        with open('news_output.txt', 'w', encoding='utf-8') as f:
            f.write(summary)

        return "news_output.txt"

    except requests.exceptions.RequestException as e:
        fout_tijd = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fout_bericht = f"# 🛑 FOUT bij het Ophalen van Nieuws ({fout_tijd})\n\nEr is een fout opgetreden bij het verbinden met VRT NWS:\n\n```\n{e}\n```\n\nControleer de internetverbinding of de URL."

        with open('news_output.txt', 'w', encoding='utf-8') as f:
            f.write(fout_bericht)

        return "news_output.txt"


if __name__ == "__main__":
    get_news_summary()
