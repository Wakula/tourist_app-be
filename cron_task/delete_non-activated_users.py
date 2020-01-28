import psycopg2
conn = psycopg2.connect(database="trip_db", user="postgres", password="password")
cursor = conn.cursor()
cursor.execute("DELETE FROM user_profile WHERE registration_time <= NOW() - INTERVAL '24 hours' AND is_active = false;")
conn.commit()
conn.close()
