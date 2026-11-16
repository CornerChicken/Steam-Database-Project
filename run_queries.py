import sqlite3
import pandas as pd

conn = sqlite3.connect("steam.db")

def run(title, sql):
    print(f"\n=== {title} ===")
    print(pd.read_sql_query(sql, conn).to_string(index=False))

# Query 1: SELECT, WHERE, ORDER BY, LIMIT

run("Top 10 games under $10 by positive reviews", """
    SELECT name, price, positive
    FROM games
    WHERE price < 10
    ORDER BY positive DESC
    LIMIT 10;
""")

# Query 2: COUNT and AVG

run("Free vs paid games", """
    SELECT
        SUM(CASE WHEN price = 0 THEN 1 ELSE 0 END) AS free_games,
        COUNT(*) AS total_games,
        ROUND(AVG(CASE WHEN price > 0 THEN price END), 2) AS avg_paid_price
    FROM games;
""")

# Query 3: JOIN GROUP BY, HAVING

run("Average price by genre", """
    SELECT gg.genre,
        COUNT(*) AS num_games,
        ROUND(AVG(g.price), 2) AS avg_price
    FROM game_genres AS gg
    JOIN games AS g ON g.app_id = gg.app_id
    GROUP BY gg.genre
    HAVING COUNT(*) >= 100
    ORDER BY avg_price DESC;
""")

# Query 4: Which genres are rated best?
run("Positive review % by genre (only games with 50+ reviews)", """
    SELECT gg.genre,
        COUNT(*) AS num_games,
        ROUND(SUM(g.positive) * 100.0 / SUM(g.positive + g.negative), 1) AS positive_pct
    FROM game_genres AS gg
    JOIN games AS g ON g.app_id = gg.app_id
    WHERE g.positive + g.negative >= 50
    GROUP BY gg.genre
    HAVING COUNT(*) >= 100
    ORDER BY positive_pct DESC;
""")

conn.close()