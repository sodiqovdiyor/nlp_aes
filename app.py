import streamlit as st
import pickle
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
from os import urandom

# AES shifrlash funksiyasi
def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_CBC)  # CBC rejasida AES
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))  # Matnni shifrlash
    iv = base64.b64encode(cipher.iv).decode('utf-8')  # IV ni base64 formatda kodlash
    ct = base64.b64encode(ct_bytes).decode('utf-8')  # Shifrlangan matnni base64 formatda kodlash
    return iv, ct

# Set the page configuration first
st.set_page_config(page_title="NLP Kategoriyalar Bashorati", page_icon="📊", layout="centered")

# Modelni yuklash
@st.cache_resource
def load_model():
    with open('nlp_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('tfidf_vectorizer.pkl', 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)
    return model, vectorizer

model, tfidf = load_model()

# Streamlit interfeysi sozlash
st.markdown(
    """
    <style>
    /* Umumiy fon uchun rangli gradient */
    .stApp {
        background: linear-gradient(135deg, #ffecd2, #fcb69f);
        color: #34495E;
        font-family: 'Arial', sans-serif;
    }

    /* Karta uchun quti ko'rinishi */
    .main {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 25px;
        box-shadow: 0px 15px 30px rgba(0, 0, 0, 0.2);
        max-width: 750px;
        margin: 20px auto;
        border: 2px solid #f39c12;
    }

    /* Sarlavha */
    h1 {
        color: #2E4053;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 25px;
        text-shadow: 2px 2px 5px #f39c12;
    }

    /* Matn maydoni sarlavhasi */
    .stTextArea>label {
        font-size: 1.3rem;
        color: #5D6D7E;
        font-weight: bold;
        margin-bottom: 10px;
    }

    /* Tugmalar */
    .stButton>button {
        background-color: #e74c3c !important;
        color: #ffffff !important;
        border-radius: 50px !important;
        padding: 15px 35px !important;
        font-size: 20px !important;
        font-weight: bold;
        border: none;
        box-shadow: 0px 8px 15px rgba(231, 76, 60, 0.4);
        transition: 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #c0392b !important;
        box-shadow: 0px 12px 20px rgba(192, 57, 43, 0.4);
        transform: scale(1.05);
    }

    /* Natijalar qutisi */
    .result-section {
        background-color: #f7f1e3;
        padding: 25px;
        border-radius: 20px;
        margin-top: 20px;
        box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);
    }

    .result-section h3 {
        font-size: 1.7rem;
        color: #34495E;
        font-weight: bold;
        margin-bottom: 15px;
    }

    .result-section p {
        font-size: 1.2rem;
        color: #2c3e50;
        margin-bottom: 10px;
    }

    /* Ikonalar */
    .icon {
        font-size: 1.8rem;
        margin-right: 10px;
        color: #2980b9;
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 50px;
        font-size: 14px;
        color: #6c757d;
    }

    /* Footer havolalar */
    .footer a {
        color: #007bff;
        text-decoration: none;
        margin: 0 10px;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sarlavha
st.title("NLP Kategoriyalar Bashorati")

# Matnni kiriting
st.markdown("<h3 style='color:#34495E;'>📝 Matnni kiriting:</h3>", unsafe_allow_html=True)
user_input = st.text_area(
    "Matnni kiriting (masalan: 'Yangiliklar sarlavhasi yoki qisqacha izoh')",
    "",
    placeholder="Matnni bu yerga yozing..."
)

# AES kalitini yaratish
key = urandom(16)  # 16 baytli tasodifiy kalit

# Bashorat qilish
if st.button("Bashorat qilish"):
    if user_input.strip():
        # Matnni vektorizatsiya qilish
        input_vectorized = tfidf.transform([user_input])
        
        # Model orqali bashorat qilish
        prediction = model.predict(input_vectorized)
        
        # Matnni AES bilan shifrlash
        iv, encrypted_data = encrypt_data(user_input, key)
        
        # Natijani ko'rsatish
        st.markdown(
            f"<div class='result-section'><h3>📋 Bashorat: {prediction[0]}</h3></div>",
            unsafe_allow_html=True,
        )
        
        st.markdown(
            f"<div class='result-section'><h3>🔒 Shifrlangan matn:</h3><p>IV: {iv}</p><p>Shifrlangan matn: {encrypted_data}</p></div>",
            unsafe_allow_html=True,
        )
    else:
        st.error("Iltimos, matn kiriting!")

# Footer
st.markdown(
    """
    <div class='footer'>
        Ushbu ilova sun'iy intellekt asosida ishlaydi. 👨‍💻 Diyor Sodiqov tomonidan yasalgan!<br>
        <a href='https://www.kaggle.com/datasets/nikhiljohnk/news-popularity-in-multiple-social-media-platforms' target='_blank'>
            📰 Foydalanasiz
        </a>
        <a href='tel:+998932797755'>
            📞 Aloqa: +998932797755
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)
