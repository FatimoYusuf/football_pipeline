import requests
from bs4 import BeautifulSoup
from datetime import date  
from app.crud import upsert_player
from app.database import SessionLocal

def scrape_transfermarkt(base_url):
    db = SessionLocal()
    page = 1
    headers = {'User-Agent': 'Mozilla/5.0'}

    while True:
        url = f"{base_url}/page/{page}"
        print(f"Scraping page {page}...")
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table', {'class': 'items'})
        if not table:
            break

        rows = table.find_all('tr', {'class': ['odd', 'even']})
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 11:
                continue

            nationality_imgs = cols[5].find_all('img', {'class': 'flaggenrahmen'})
            nationalities = ', '.join([img['title'] for img in nationality_imgs])

            player_data = {
                "scraped_date": date.today(),  # <-- add this
                "name": cols[1].text.strip(),
                "position": cols[4].text.strip(),
                "club": row.select_one(".zentriert a[title]")["title"].strip() if row.select_one(".zentriert a[title]") else "N/A",
                "nationality": nationalities,
                "age": cols[6].text.strip(),
                "highest_value": cols[8].text.strip(),
                "last_update": cols[9].text.strip(),
                "market_value": cols[10].text.strip()
            }
            upsert_player(db, player_data)

        db.commit()

        next_page = soup.find('li', {'class': 'tm-pagination__list-item--icon-next-page'})
        if not next_page:
            break
        page += 1

    db.close()
