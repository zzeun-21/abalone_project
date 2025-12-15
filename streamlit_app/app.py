import streamlit as st
import requests

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Prediksi Umur Abalone",
    page_icon="🐚",
    layout="wide",
)

API_URL = "abalone_project.railway.internal/predict"

# =========================
# I18N (ID/EN)
# =========================
TEXT = {
    "id": {
        "nav_home": "Beranda",
        "nav_predict": "Prediksi",
        "nav_footer": "Footer",
        "hero_title": "Prediksi Umur Abalone",
        "hero_subtitle": "Sistem Prediksi Umur Biologis Abalone Berbasis Machine Learning",
        "about_title": "Tentang Abalone",
        "about_text": """
Abalone adalah moluska laut yang memiliki cangkang berbentuk telinga dengan permukaan yang indah dan berkilau. 
Hewan ini termasuk dalam kelas Gastropoda dan hidup di perairan laut yang dingin hingga hangat di seluruh dunia.

**Karakteristik Abalone:**
- Memiliki cangkang keras berbentuk oval dengan lubang respirasi di sepanjang tepinya
- Dagingnya dianggap sebagai makanan lezat dan memiliki nilai ekonomi tinggi
- Pertumbuhan lambat dengan umur yang bisa mencapai puluhan tahun
- Hidup menempel pada batuan di dasar laut

**Estimasi Umur Abalone:**
Penentuan umur abalone secara tradisional dilakukan dengan menghitung jumlah cincin (*rings*) pada cangkangnya, 
mirip dengan menghitung cincin pada pohon. Namun, metode ini memerlukan proses pemotongan cangkang yang 
merusak dan memakan waktu. 

Dengan teknologi Machine Learning, kita dapat memprediksi umur abalone berdasarkan karakteristik 
fisik seperti panjang, diameter, tinggi, dan berbagai pengukuran berat, tanpa merusak cangkang.
        """,
        "cta_predict": "Mulai Prediksi Sekarang",
        "section_predict_title": "Form Prediksi Umur Abalone",
        "form_instruction": "Masukkan data pengukuran fisik abalone di bawah ini untuk mendapatkan prediksi umur.",
        "sex": "Jenis Kelamin (Sex)",
        "sex_help": "M = Jantan, F = Betina, I = Infant (belum dewasa)",
        "length": "Length (mm)",
        "length_help": "Panjang cangkang terpanjang",
        "diameter": "Diameter (mm)",
        "diameter_help": "Diameter tegak lurus terhadap length",
        "height": "Height (mm)",
        "height_help": "Tinggi dengan daging di dalamnya",
        "whole_weight": "Whole Weight (gram)",
        "whole_weight_help": "Berat keseluruhan abalone",
        "shucked_weight": "Shucked Weight (gram)",
        "shucked_weight_help": "Berat daging saja",
        "viscera_weight": "Viscera Weight (gram)",
        "viscera_weight_help": "Berat usus (setelah dikeluarkan darah)",
        "shell_weight": "Shell Weight (gram)",
        "shell_weight_help": "Berat cangkang setelah dikeringkan",
        "btn_predict": "🔮 Prediksi Umur",
        "result_title": "Hasil Prediksi",
        "rings_label": "Jumlah Cincin (Rings)",
        "age_label": "Estimasi Umur",
        "years": "tahun",
        "footer_title": "MEMAHAMI HASIL PREDIKSI",
        "footer_content": """

**Cara Membaca Hasil Prediksi:**

1. **Jumlah Cincin (Rings):**  
   Nilai ini merepresentasikan jumlah cincin pertumbuhan pada cangkang abalone. Setiap cincin umumnya 
   terbentuk setiap tahun, mirip dengan cincin pertumbuhan pada pohon.

2. **Estimasi Umur (tahun):**  
   Umur biologis abalone dihitung menggunakan rumus standar:  
   **Umur = Jumlah Cincin + 1.5 tahun**
   
   Penambahan 1.5 tahun ini memperhitungkan periode awal pertumbuhan abalone sebelum cincin pertama 
   terbentuk.

**Contoh Interpretasi:**
- Jika prediksi menunjukkan **10 cincin**, maka estimasi umur = 10 + 1.5 = **11.5 tahun**
- Jika prediksi menunjukkan **15 cincin**, maka estimasi umur = 15 + 1.5 = **16.5 tahun**
        """,
        "footer_copyright": "© 2025 Abalone Age Predictor • Powered by Machine Learning",
        "api_down": "⚠️ API tidak dapat diakses. Pastikan Flask API berjalan di `python api\\app.py`",
        "api_error": "❌ Terjadi kesalahan saat memproses data.",
        "processing": "Memproses prediksi...",
        "lang_label": "Bahasa",
    },
    "en": {
        "nav_home": "Home",
        "nav_predict": "Prediction",
        "nav_footer": "Footer",
        "hero_title": "Abalone Age Prediction",
        "hero_subtitle": "Machine Learning-Based Abalone Biological Age Prediction System",
        "about_title": "About Abalone",
        "about_text": """
Abalone is a marine mollusk with an ear-shaped shell featuring a beautiful, iridescent surface. 
This animal belongs to the Gastropoda class and lives in cold to warm ocean waters worldwide.

**Abalone Characteristics:**
- Has a hard, oval shell with respiratory holes along its edge
- Its meat is considered a delicacy with high economic value
- Slow growth with a lifespan that can reach decades
- Lives attached to rocks on the ocean floor

**Estimating Abalone Age:**
Traditionally, abalone age is determined by counting the rings on its shell, similar to counting 
tree rings. However, this method requires cutting the shell, which is destructive and time-consuming.

With Machine Learning technology, we can predict abalone age based on physical characteristics 
such as length, diameter, height, and various weight measurements, without damaging the shell.
        """,
        "cta_predict": "Start Prediction Now",
        "section_predict_title": "Abalone Age Prediction Form",
        "form_instruction": "Enter the physical measurement data of the abalone below to get age prediction.",
        "sex": "Sex",
        "sex_help": "M = Male, F = Female, I = Infant (immature)",
        "length": "Length (mm)",
        "length_help": "Longest shell measurement",
        "diameter": "Diameter (mm)",
        "diameter_help": "Diameter perpendicular to length",
        "height": "Height (mm)",
        "height_help": "Height with meat inside",
        "whole_weight": "Whole Weight (grams)",
        "whole_weight_help": "Total weight of abalone",
        "shucked_weight": "Shucked Weight (grams)",
        "shucked_weight_help": "Weight of meat only",
        "viscera_weight": "Viscera Weight (grams)",
        "viscera_weight_help": "Gut weight (after bleeding)",
        "shell_weight": "Shell Weight (grams)",
        "shell_weight_help": "Shell weight after drying",
        "btn_predict": "🔮 Predict Age",
        "result_title": "Prediction Result",
        "rings_label": "Number of Rings",
        "age_label": "Estimated Age",
        "years": "years",
        "footer_title": "Understanding Prediction Results",
        "footer_content": """
**How to Read Prediction Results:**

1. **Number of Rings:**  
   This value represents the number of growth rings on the abalone shell. Each ring typically 
   forms annually, similar to growth rings in trees.

2. **Estimated Age (years):**  
   The biological age of abalone is calculated using the standard formula:  
   **Age = Number of Rings + 1.5 years**
   
   The addition of 1.5 years accounts for the initial growth period of the abalone before 
   the first ring forms.

**Interpretation Example:**
- If prediction shows **10 rings**, then estimated age = 10 + 1.5 = **11.5 years**
- If prediction shows **15 rings**, then estimated age = 15 + 1.5 = **16.5 years**
        """,
        "footer_copyright": "© 2025 Abalone Age Predictor • Powered by Machine Learning",
        "api_down": "⚠️ API is unreachable. Make sure Flask API is running at `python api\\app.py`",
        "api_error": "❌ An error occurred while processing data.",
        "processing": "Processing prediction...",
        "lang_label": "Language",
    },
}

if "lang" not in st.session_state:
    st.session_state.lang = "id"

if "show_result" not in st.session_state:
    st.session_state.show_result = False
    st.session_state.result_data = None

t = TEXT[st.session_state.lang]

# =========================
# STYLES
# =========================
st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
      * { font-family: 'Inter', sans-serif; }

      :root{
        --orange:#F47C20;
        --orange2:#FF9A3D;
        --text:#1f2937;
        --muted:#6b7280;
        --border:rgba(31,41,55,.12);
        --bg:#fafafa;
        --soft:#fff7f0;
      }

      .stApp { background: var(--bg); }
      .block-container { max-width: 1400px; padding-top: 1rem; padding-bottom: 3rem; }
      
      header[data-testid="stHeader"] { background: rgba(0,0,0,0); }
    #   div[data-testid="stToolbar"] { visibility: hidden; }

      /* Header with logo and language */
      .top-header{
        display:flex; align-items:center; justify-content:space-between;
        padding: 1rem 1.5rem;
        background: white;
        border-radius: 16px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,.04);
      }
      .logo{
        font-weight:800; font-size:1.5rem;
        display:flex; align-items:center; gap:.6rem;
        color: var(--text);
      }
      .logo-icon{
        width:42px; height:42px; border-radius:12px;
        background: linear-gradient(135deg,var(--orange),var(--orange2));
        display:flex; align-items:center; justify-content:center;
        font-size:1.5rem;
      }

      /* Navbar */
      .navbar{
        display:flex; justify-content:center; gap:1rem;
        padding: 0.8rem;
        background: white;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,.04);
      }
      .nav-btn{
        padding:.6rem 1.4rem;
        border-radius:10px;
        background: transparent;
        color: var(--text);
        font-weight:600;
        text-decoration:none;
        border: 2px solid transparent;
        transition: all .2s;
      }
      .nav-btn:hover{
        background: var(--soft);
        border-color: var(--orange);
        color: var(--orange);
      }

      /* Hero */
      .hero{
        background: linear-gradient(135deg, var(--orange), var(--orange2));
        border-radius: 24px;
        padding: 3rem 2rem;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(244,124,32,.25);
      }
      .hero h1{ 
        margin:0; font-size:2.8rem; font-weight:900;
        text-shadow: 0 2px 10px rgba(0,0,0,.1);
      }
      .hero p{ 
        margin:.8rem auto 0; 
        font-size:1.15rem; 
        opacity:.95;
        max-width: 700px;
      }

      /* Content sections */
    .content-section {
        background: white;
        border-radius: 20px;
        padding: 1rem 2rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 16px rgba(0,0,0,.06);
    }

    .section-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: var(--text);
        margin: 0;
        display: flex;
        align-items: center;
        gap: .6rem;
    }

      .title-icon{
        width:36px; height:36px;
        background: linear-gradient(135deg,var(--orange),var(--orange2));
        border-radius:10px;
        display:flex; align-items:center; justify-content:center;
        color:white; font-size:1.2rem;
      }

      /* About section */
      .about-grid{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        margin-top: 1.5rem;
      }
      .about-image{
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,.12);
      }
      .about-image img{
        width: 100%;
        height: 400px;
        object-fit: cover;
      }
      .about-content{
        color: var(--text);
        line-height: 1.8;
      }
      .about-content p{
        margin-bottom: 1rem;
      }
      .cta-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: .6rem;

    padding: .9rem 1.8rem;
    background: linear-gradient(135deg, var(--orange), var(--orange2));

    color: #fff !important;          /* PAKSA putih */
    text-decoration: none !important;/* HILANGKAN underline */

    border-radius: 12px;
    font-weight: 700;

    margin-top: 1.2rem;
    box-shadow: 0 8px 20px rgba(244,124,32,.3);
    transition: all .2s ease;
    }

    /* Pastikan semua state link bersih */
    .cta-button:link,
    .cta-button:visited,
    .cta-button:hover,
    .cta-button:active {
        color: #fff !important;
        text-decoration: none !important;
    }

    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px rgba(244,124,32,.4);
    }

    .about-text-box {
    background: #ffffff;
    border-radius: 14px;
    padding: 1.2rem 1.6rem;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
    
    color: var(--text);
    font-size: 1rem;
    line-height: 1.65;
}

    /* Rapikan elemen teks di dalamnya */
    .about-text-box p {
        margin-bottom: 0.8rem;
    }

    .about-text-box ul {
        margin: 0.6rem 0 0.8rem 1.2rem;
    }

    .about-text-box li {
        margin-bottom: 0.4rem;
    }

    .about-text-box strong {
        font-weight: 700;
    }



      /* Form styling */
      .form-grid{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin-top: 1.5rem;
      }
      
      /* Result card */
      .result-card{
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 2px solid #7dd3fc;
        border-radius: 16px;
        padding: 2rem;
        margin-top: 2rem;
      }
      .result-grid{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin-top: 1rem;
      }
      .result-item{
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,.08);
      }
      .result-label{
        font-size: .95rem;
        color: var(--muted);
        font-weight: 600;
        margin-bottom: .5rem;
      }
      .result-value{
        font-size: 2.5rem;
        font-weight: 900;
        color: var(--orange);
      }
      .result-unit{
        font-size: 1rem;
        color: var(--muted);
        margin-left: .3rem;
      }

      /* Footer */
      .footer-section{
        background: var(--text);
        color: white;
        border-radius: 20px;
        padding: 2.5rem 2rem;
        margin-top: 2rem;
      }
      .footer-title{
        font-size: 1.6rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: var(--orange);
        text-align: center;
      }
      .footer-content{
        line-height: 1.9;
        opacity: .9;
      }
      .footer-content strong{
        color: var(--orange2);
      }

      /* Buttons */
      .stButton > button{
        width:100%;
        border:0;
        border-radius: 12px;
        padding: .9rem 1.2rem;
        background: linear-gradient(135deg,var(--orange),var(--orange2));
        color:white;
        font-weight:800;
        font-size: 1.05rem;
        box-shadow: 0 8px 20px rgba(244,124,32,.3);
        transition: transform .2s;
      }
      .stButton > button:hover{ 
        transform: translateY(-2px);
        box-shadow: 0 12px 28px rgba(244,124,32,.4);
      }

      @media (max-width: 768px) {
        .about-grid, .form-grid, .result-grid {
          grid-template-columns: 1fr;
        }
        .hero h1 { font-size: 2rem; }
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# HEADER with Logo and Language Selector
# =========================
col_logo, col_lang = st.columns([0.9, 0.2])


with col_lang:
    st.markdown('<div style="padding-top:1.2rem;">', unsafe_allow_html=True)
    lang = st.selectbox(
        t["lang_label"],
        options=["id", "en"],
        format_func=lambda x: "🇮🇩 Indonesia" if x == "id" else "🇬🇧 English",
        index=0 if st.session_state.lang == "id" else 1,
    )
    if lang != st.session_state.lang:
        st.session_state.lang = lang
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

t = TEXT[st.session_state.lang]



# =========================
# HERO
# =========================
st.markdown('<div id="home"></div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="hero">
      <h1>{t["hero_title"]}</h1>
      <p>{t["hero_subtitle"]}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================
# ABOUT ABALONE SECTION
# =========================
st.markdown(
    f"""
    <div class="content-section">
      <div class="section-title">
        <div class="title-icon">📖</div>
        {t["about_title"]}
      </div>
    """,
    unsafe_allow_html=True,
)

# ROW 1 — IMAGE
st.image(
    "https://www.foodrepublic.com/img/gallery/what-exactly-is-abalone-and-how-do-you-eat-it/where-to-buy-abalone-1717527072.webp",
    use_container_width=True,
)

# ROW 2 — TEXT + CTA
st.markdown(
    f"""
    <div class="about-text-box">{t["about_text"]}</div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f'<a class="cta-button" href="#predict">{t["cta_predict"]} →</a>',
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)


# =========================
# PREDICTION SECTION
# =========================
st.markdown('<div id="predict"></div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="content-section">
      <div class="section-title">
        <div class="title-icon">🔮</div>
        {t["section_predict_title"]}
      </div>
      <p style="color:var(--muted); margin-bottom:1.5rem;">{t["form_instruction"]}</p>
    """,
    unsafe_allow_html=True,
)

# Form inputs
sex = st.selectbox(t["sex"], ["M", "F", "I"], help=t["sex_help"])

col1, col2 = st.columns(2)

with col1:
    length = st.number_input(
        t["length"],
        min_value=0.0,
        value=0.55,
        step=0.01,
        format="%.2f",
        help=t["length_help"],
    )
    diameter = st.number_input(
        t["diameter"],
        min_value=0.0,
        value=0.43,
        step=0.01,
        format="%.2f",
        help=t["diameter_help"],
    )
    height = st.number_input(
        t["height"],
        min_value=0.0,
        value=0.15,
        step=0.01,
        format="%.2f",
        help=t["height_help"],
    )
    whole_weight = st.number_input(
        t["whole_weight"],
        min_value=0.0,
        value=0.90,
        step=0.01,
        format="%.2f",
        help=t["whole_weight_help"],
    )

with col2:
    shucked_weight = st.number_input(
        t["shucked_weight"],
        min_value=0.0,
        value=0.38,
        step=0.01,
        format="%.2f",
        help=t["shucked_weight_help"],
    )
    viscera_weight = st.number_input(
        t["viscera_weight"],
        min_value=0.0,
        value=0.20,
        step=0.01,
        format="%.2f",
        help=t["viscera_weight_help"],
    )
    shell_weight = st.number_input(
        t["shell_weight"],
        min_value=0.0,
        value=0.25,
        step=0.01,
        format="%.2f",
        help=t["shell_weight_help"],
    )

predict_btn = st.button(t["btn_predict"], type="primary")

# =========================
# PREDICTION RESULT
# =========================
if predict_btn:
    payload = {
        "sex": sex,
        "length": float(length),
        "diameter": float(diameter),
        "height": float(height),
        "whole_weight": float(whole_weight),
        "shucked_weight": float(shucked_weight),
        "viscera_weight": float(viscera_weight),
        "shell_weight": float(shell_weight),
    }

    try:
        with st.spinner(t["processing"]):
            r = requests.post(API_URL, json=payload, timeout=10)
            r.raise_for_status()
            data = r.json()

        predicted_rings = data.get("predicted_rings", data.get("predicted_age", 0))
        
        if predicted_rings is not None:
            rings = float(predicted_rings)
            age_years = rings + 1.5
            
            st.markdown(
                f"""
                <div class="result-card">
                  <h3 style="margin:0 0 1rem 0; color:var(--text); font-weight:800;">
                    ✨ {t["result_title"]}
                  </h3>
                  <div class="result-grid">
                    <div class="result-item">
                      <div class="result-label">{t["rings_label"]}</div>
                      <div class="result-value">{rings:.2f}</div>
                    </div>
                    <div class="result-item">
                      <div class="result-label">{t["age_label"]}</div>
                      <div class="result-value">
                        {age_years:.2f}
                        <span class="result-unit">{t["years"]}</span>
                      </div>
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    except requests.exceptions.ConnectionError:
        st.error(t["api_down"])
    except requests.exceptions.Timeout:
        st.error("⏱️ Timeout. Please retry.")
    except requests.exceptions.HTTPError:
        st.error(f"❌ API error: {r.status_code}")
    except Exception as e:
        st.error(t["api_error"])

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# FOOTER - Understanding Results
# =========================
st.markdown('<div id="footer"></div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="footer-section">
      <div class="footer-title">{t["footer_title"]}</div>
      <div class="footer-content">{t["footer_content"]}</div>
      <div style="margin-top:2rem; padding-top:1.5rem; border-top:1px solid rgba(255,255,255,.2); 
                  text-align:center; opacity:.7;">
        {t["footer_copyright"]}
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)