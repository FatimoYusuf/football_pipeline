from sqlalchemy.orm import Session
from app.models import Player
from datetime import date

def upsert_player(db: Session, player_data: dict):
    existing = db.query(Player).filter(
        Player.name == player_data["name"],
        Player.scraped_date == date.today()  # same player, same day
    ).first()

    if existing:
        for key, value in player_data.items():
            setattr(existing, key, value)
    else:
        new_player = Player(**player_data)
        db.add(new_player)
