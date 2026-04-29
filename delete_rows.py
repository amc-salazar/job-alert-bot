import sqlite3

conn = sqlite3.connect("jobs.db")
c = conn.cursor()

c.execute("DELETE FROM jobs")
conn.commit()

conn.close()

print("All rows deleted")