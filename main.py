import streamlit as st
import pandas as pd
import datetime
from database import init_db, tambah_transaksi, tampilkan_data
import plotly.express as px

# Konfigurasi halaman
st.set_page_config(page_title="SmartBudget", page_icon="💸", layout="wide")

# Inisialisasi database
init_db()

# Gaya CSS custom untuk tampilan modern
st.markdown("""
    <style>
        body {
            background-color: #0e1117;
            color: white;
        }
        .stApp {
            background-color: #0e1117;
        }
        h1, h2, h3 {
            color: #f0f2f6;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 1rem;
        }
        div[data-testid="stMetricValue"] {
            font-size: 28px;
            color: #00e6ac;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("💸 Catatan Keuangan Bahtiar")
st.markdown("---")

# Sidebar
menu = ["📥 Input Transaksi", "📊 Laporan & Grafik"]
choice = st.sidebar.radio("Navigasi", menu)

if choice == "📥 Input Transaksi":
    st.header("Tambah Transaksi Baru")
    col1, col2 = st.columns(2)

    with col1:
        tanggal = st.date_input("Tanggal", datetime.date.today())
        kategori = st.selectbox("Kategori", ["Makan", "Transportasi", "Kuliah", "Hiburan", "Lainnya"])
        jenis = st.radio("Jenis", ["Pemasukan", "Pengeluaran"])

    with col2:
        nominal = st.number_input("Nominal (Rp)", min_value=0.0, step=1000.0, format="%.2f")
        keterangan = st.text_input("Keterangan")

        if st.button("💾 Simpan Transaksi", use_container_width=True):
            tambah_transaksi(str(tanggal), kategori, jenis, nominal, keterangan)
            st.success("✅ Transaksi berhasil disimpan!")

elif choice == "📊 Laporan & Grafik":
    st.header("Laporan Keuangan")
    df = tampilkan_data()

    if df.empty:
        st.warning("Belum ada data transaksi.")
    else:
        # Ringkasan keuangan
        total_masuk = df[df['jenis'] == 'Pemasukan']['nominal'].sum()
        total_keluar = df[df['jenis'] == 'Pengeluaran']['nominal'].sum()
        saldo = total_masuk - total_keluar

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Pemasukan", f"Rp {total_masuk:,.0f}")
        with col2:
            st.metric("Pengeluaran", f"Rp {total_keluar:,.0f}")
        with col3:
            st.metric("Saldo", f"Rp {saldo:,.0f}")

        st.markdown("---")
        st.subheader("📅 Detail Transaksi")
        st.dataframe(df.style.format({'nominal': 'Rp{:,.0f}'}), use_container_width=True)

        st.markdown("---")
        st.subheader("📈 Tren Keuangan")

        # Konversi kolom tanggal ke datetime
        df['tanggal'] = pd.to_datetime(df['tanggal'])

        # Urutkan data berdasarkan tanggal
        df = df.sort_values('tanggal')

        # Agregasi data
        df_tren = df.groupby(['tanggal', 'jenis'])['nominal'].sum().reset_index()

        # Grafik garis dengan Plotly
        fig = px.line(df_tren, x='tanggal', y='nominal', color='jenis',
                      title='Tren Keuangan Harian',
                      markers=True,
                      color_discrete_map={"Pemasukan": "#00cc96", "Pengeluaran": "#ff4b4b"})

        fig.update_layout(
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117",
            font_color="#f0f2f6",
            xaxis_title="Tanggal",
            yaxis_title="Nominal (Rp)",
            legend_title="Jenis",
            hovermode="x unified",
            title_x=0.5
        )

        st.plotly_chart(fig, use_container_width=True)
