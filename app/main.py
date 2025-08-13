from app.database import Base, engine
from app.scraper import scrape_transfermarkt

def main():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    base_url = "https://www.transfermarkt.com/premier-league/marktwerte/wettbewerb/GB1/pos//detailpos/0/altersklasse/alle/land_id/0/plus/1"
    scrape_transfermarkt(base_url)

if __name__ == "__main__":
    main()
