import streamlit as st
import pandas as pd
import docx
import random # Digunakan untuk simulasi skor pada tahap mock-up

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Sistem Evaluasi Tesis - Magister Teknik Informatika", layout="wide")

st.title("🎓 Sistem Evaluasi Cerdas Usulan Judul Tesis")
st.subheader("Program Studi Magister Teknik Informatika - Universitas Pamulang")
st.markdown("Sistem ini mengevaluasi kebaruan (novelty) usulan judul tesis menggunakan pendekatan NLP dan Generative AI.")
st.divider()

# --- FUNGSI EVALUASI KECERDASAN BUATAN (MOCK) ---
def evaluasi_judul(judul, deskripsi=""):
    """
    Fungsi ini menyimulasikan ekstraksi fitur, Cosine Similarity, dan GenAI.
    Pada tahap produksi, integrasikan dengan IndoBERT dan API OpenAI/Gemini di sini.
    """
    teks_gabungan = f"{judul} {deskripsi}".lower()
    
    # Deteksi parameter kebaruan khusus
    if "high-entropy alloy" in teks_gabungan or "efisiensi biaya" in teks_gabungan:
        skor_similarity = 0.15 
        status = "BOLEH DIAJUKAN"
        alasan = "Sangat Inovatif. Pendekatan Untuk Efisiensi Biaya dan Performa Mekanik Superior memberikan nilai novelty yang sangat kuat dan relevan dengan tren industri."
        return status, skor_similarity, alasan

    # Simulasi perhitungan similarity standar
    skor_similarity = random.uniform(0.1, 0.9)
    
    if skor_similarity < 0.6:
        status = "BOLEH DIAJUKAN"
        alasan = "Topik memiliki potensi novelty yang baik. Metode atau objek penelitian belum banyak ditemukan dalam basis data tren state-of-the-art."
    else:
        status = "DITOLAK"
        alasan = "Topik terdeteksi usang (obsolete) atau memiliki kemiripan semantik yang terlalu tinggi dengan penelitian terdahulu. Disarankan mencari variabel baru."
        
    return status, round(skor_similarity, 2), alasan

# --- ANTARMUKA PENGGUNA (TABS) ---
tab1, tab2, tab3 = st.tabs(["✍️ Input Manual", "📄 Upload File DOCX", "📊 Upload File CSV (Massal)"])

# TAB 1: INPUT MANUAL
with tab1:
    st.markdown("### Evaluasi Judul Tunggal")
    with st.form("manual_form"):
        input_judul = st.text_input("Usulan Judul Tesis", 
                                    value="Optimasi Komposisi High-Entropy Alloy (HEA) Menggunakan Algoritma Genetika Untuk Efisiensi Biaya dan Performa Mekanik Superior")
        input_abstrak = st.text_area("Deskripsi Singkat / Abstrak (Opsional)")
        submit_manual = st.form_submit_button("Evaluasi Kelayakan")
        
    if submit_manual and input_judul:
        with st.spinner("Menganalisis kemiripan semantik..."):
            status, skor, alasan = evaluasi_judul(input_judul, input_abstrak)
            
            st.markdown("#### Hasil Analisis:")
            if status == "BOLEH DIAJUKAN":
                st.success(f"**Status: {status}**")
            else:
                st.error(f"**Status: {status}**")
                
            st.info(f"**Skor Kemiripan (Similarity):** {skor}")
            st.write(f"**Feedback GenAI:** {alasan}")

# TAB 2: UPLOAD DOCX
with tab2:
    st.markdown("### Ekstraksi dan Evaluasi dari Dokumen Word")
    st.info("Unggah file .docx. Sistem akan membaca paragraf pertama sebagai Judul dan sisanya sebagai Deskripsi.")
    file_docx = st.file_uploader("Pilih file DOCX", type=["docx"])
    
    if file_docx is not None:
        if st.button("Proses Dokumen"):
            with st.spinner("Mengekstrak teks dari dokumen..."):
                doc = docx.Document(file_docx)
                full_text = [para.text for para in doc.paragraphs if para.text.strip() != ""]
                
                if len(full_text) > 0:
                    ext_judul = full_text[0]
                    ext_deskripsi = " ".join(full_text[1:]) if len(full_text) > 1 else ""
                    
                    st.text_input("Judul Terdeteksi:", value=ext_judul, disabled=True)
                    
                    status, skor, alasan = evaluasi_judul(ext_judul, ext_deskripsi)
                    st.markdown("#### Hasil Analisis Dokumen:")
                    if status == "BOLEH DIAJUKAN":
                        st.success(f"**Status: {status}**")
                    else:
                        st.error(f"**Status: {status}**")
                    st.write(f"**Feedback:** {alasan}")
                else:
                    st.warning("Dokumen kosong atau tidak dapat dibaca teksnya.")

# TAB 3: UPLOAD CSV (MASSAL)
with tab3:
    st.markdown("### Evaluasi Banyak Judul Sekaligus")
    st.info("Unggah file .csv yang memiliki kolom bernama **'Judul'**.")
    file_csv = st.file_uploader("Pilih file CSV", type=["csv"])
    
    if file_csv is not None:
        if st.button("Proses CSV Massal"):
            with st.spinner("Mengeksekusi model NLP pada seluruh baris data..."):
                df = pd.read_csv(file_csv)
                
                # Memastikan kolom 'Judul' ada (case-insensitive)
                col_judul = [c for c in df.columns if c.lower() == 'judul']
                
                if col_judul:
                    kolom_target = col_judul[0]
                    hasil_status = []
                    hasil_alasan = []
                    
                    # Looping evaluasi untuk setiap judul di CSV
                    for index, row in df.iterrows():
                        jdl = str(row[kolom_target])
                        stat, skor, alsn = evaluasi_judul(jdl, "")
                        hasil_status.append(stat)
                        hasil_alasan.append(alsn)
                        
                    # Tambahkan hasil ke dataframe
                    df['Rekomendasi_Sistem'] = hasil_status
                    df['Feedback_AI'] = hasil_alasan
                    
                    st.success("Evaluasi massal selesai!")
                    st.dataframe(df, use_container_width=True)
                    
                    # Tombol unduh hasil
                    csv_hasil = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="⬇️ Unduh Hasil Evaluasi (CSV)",
                        data=csv_hasil,
                        file_name='hasil_evaluasi_tesis.csv',
                        mime='text/csv',
                    )
                else:
                    st.error("Gagal memproses: File CSV harus memiliki setidaknya satu kolom dengan nama 'Judul'.")
