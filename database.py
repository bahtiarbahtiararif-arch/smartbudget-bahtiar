import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect('data/keuangan.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transaksi (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tanggal TEXT,
                    kategori TEXT,
                    jenis TEXT,
                    nominal REAL,
                    keterangan TEXT
                )''')
    conn.commit()
    conn.close()

def tambah_transaksi(tanggal, kategori, jenis, nominal, keterangan):
    conn = sqlite3.connect('data/keuangan.db')
    c = conn.cursor()
    c.execute("INSERT INTO transaksi (tanggal, kategori, jenis, nominal, keterangan) VALUES (?, ?, ?, ?, ?)",
              (tanggal, kategori, jenis, nominal, keterangan))
    conn.commit()
    conn.close()

def tampilkan_data():
    conn = sqlite3.connect('data/keuangan.db')
    df = pd.read_sql_query("SELECT * FROM transaksi", conn)
    conn.close()
    return df
