import ast # Turns text into a Python list
import sqlite3
import pandas as pd

#Load cleaned data

df = pd.read_csv("data/02-processed/steam_games.csv")

df = df.rename(columns = {
    "AppID": "app_id",
    "Price": "price",
    "Estimated owners": "estimated_owners",
    "Peak CCU": "peak_ccu",
    "Average playtime forever": "avg_playtime",
    "Average playtime two weeks": "avg_playtime_2wk",
    "Median playtime forever": "median_playtime",
    "Median playtime two weeks": "median_playtime_2wk",
    "Positive": "positive",
    "Negative": "negative",
})

#Build "games" table
games = df.drop(columns = {
    "genres", "categories"
})

#Build genres table
genre_rows = []
for app_id, genre_text in zip(df["app_id"], df["genres"]):
    for genre in ast.literal_eval(genre_text):
        genre_rows.append({"app_id": app_id, "genre": genre})
game_genres = pd.DataFrame(genre_rows)

#Save tables to database file

conn = sqlite3.connect("steam.db")

games.to_sql("games", conn, if_exists="replace", index=False)
game_genres.to_sql("game_genres", conn, if_exists="replace", index=False)

conn.execute("CREATE INDEX IF NOT EXISTS idx_game_genres_app_id ON game_genres(app_id)")

conn.commit()
conn.close()

print(f"Games: {len(games)} rows, game_genres: {len(game_genres)} rows -> steam.db")