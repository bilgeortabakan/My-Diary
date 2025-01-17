import sqlite3

# Veritabanı bağlantısı
conn = sqlite3.connect('diary.db')
cursor = conn.cursor()

# Tablo listeleme
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in the database:")
for table in tables:
    print(table[0])

# Veritabanı bağlantısını kapat
conn.close()
