import sqlite3
import streamlit as st


st.set_page_config(
    page_title="EKİPLEN",
    page_icon="✨",
    layout="centered"
)


# =========================================================
# TASARIM
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #fffaf2;
        background-image:
            radial-gradient(circle at 10% 20%, rgba(255,190,220,0.35) 0 4px, transparent 5px),
            radial-gradient(circle at 80% 30%, rgba(180,210,255,0.35) 0 5px, transparent 6px),
            radial-gradient(circle at 30% 80%, rgba(210,190,255,0.35) 0 4px, transparent 5px),
            radial-gradient(circle at 90% 85%, rgba(255,220,160,0.35) 0 5px, transparent 6px);
        background-size: 180px 180px;
    }


    h1, h2, h3 {
        font-family: Georgia, serif !important;
        color: #76559b !important;
    }


    p, label, .stMarkdown {
        color: #333333;
    }


    .stButton > button {
        border-radius: 12px;
        border: none;
        background-color: #76559b;
        color: white !important;
        font-weight: bold;
        padding: 10px;
    }


    .stButton > button:hover {
        background-color: #644584;
        transform: scale(1.02);
    }


    .kart {
        background-color: rgba(255,255,255,0.82);
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 15px;
        box-shadow: 0 5px 20px rgba(120,90,160,0.12);
    }


    .avatar {
        font-size: 55px;
    }


    .sosyal-kutu {
        background: rgba(255,255,255,0.75);
        border-radius: 15px;
        padding: 12px;
        margin-top: 8px;
        border: 1px solid rgba(150,120,200,0.15);
    }


    /* Yazı yazılan kutular */

    .stTextInput input,
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #333333 !important;
        caret-color: #76559b !important;
        border: 1px solid rgba(120, 90, 160, 0.25) !important;
        border-radius: 12px !important;
    }


    .stTextInput input:focus,
    .stTextArea textarea:focus {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #a77ac7 !important;
        box-shadow: 0 0 0 2px rgba(167, 122, 199, 0.15) !important;
    }


    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #888888 !important;
        opacity: 1 !important;
    }


    /* =====================================================
       VIBE TESTİ CEVAPLARI
       ===================================================== */

    .stRadio label,
    .stRadio label p {
        color: #333333 !important;
    }


    .stRadio [data-testid="stMarkdownContainer"] p {
        color: #333333 !important;
    }


    .stRadio div[role="radiogroup"] label {
        color: #333333 !important;
    }


    .stRadio div[role="radiogroup"] label p {
        color: #333333 !important;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# VERİTABANI
# =========================================================

def veritabani():

    conn = sqlite3.connect("ekiplen.db")

    conn.row_factory = sqlite3.Row


    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS kullanicilar (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            kullanici_adi TEXT UNIQUE NOT NULL,

            sifre TEXT NOT NULL,

            avatar TEXT NOT NULL,

            vibe TEXT,

            instagram TEXT,

            tiktok TEXT,

            instagram_goster INTEGER DEFAULT 0,

            tiktok_goster INTEGER DEFAULT 0

        )
        """
    )


    # Eski veritabanlarında eksik kolonlar varsa ekle

    kolonlar = [
        "instagram_goster",
        "tiktok_goster"
    ]


    mevcut_kolonlar = [
        row["name"]
        for row in conn.execute(
            "PRAGMA table_info(kullanicilar)"
        ).fetchall()
    ]


    for kolon in kolonlar:

        if kolon not in mevcut_kolonlar:

            conn.execute(
                f"""
                ALTER TABLE kullanicilar
                ADD COLUMN {kolon} INTEGER DEFAULT 0
                """
            )


    # =====================================================
    # DEĞERLENDİRMELER TABLOSU
    # =====================================================

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS degerlendirmeler (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            kullanici_adi TEXT UNIQUE NOT NULL,

            arkadaslik_kurabildin_mi TEXT NOT NULL,

            testler_eglenceli_mi TEXT NOT NULL,

            neleri_gelistirebiliriz TEXT NOT NULL,

            neyi_begendin_veya_begenmedin TEXT NOT NULL,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """
    )


    conn.commit()

    return conn


conn = veritabani()


# =========================================================
# AVATARLAR
# =========================================================

AVATARLAR = [
    "🌙",
    "⭐",
    "🌸",
    "🦋",
    "🐱",
    "🐼",
    "🦊",
    "🐨",
    "🌻",
    "🍀"
]


# =========================================================
# VIBE SONUÇLARI
# =========================================================

VIBE_SONUCLARI = [
    "Enerjik Kaşif",
    "Sakin Ruh",
    "Kitap Kurdu",
    "Müzik Tutkunu",
    "Sosyal Kelebek"
]


# =========================================================
# SESSION STATE
# =========================================================

if "giris_yapildi" not in st.session_state:

    st.session_state.giris_yapildi = False


if "kullanici_adi" not in st.session_state:

    st.session_state.kullanici_adi = None


if "profil_tamamlandi" not in st.session_state:

    st.session_state.profil_tamamlandi = False


if "sifreyi_goster" not in st.session_state:

    st.session_state.sifreyi_goster = False


# =========================================================
# KULLANICI GETİR
# =========================================================

def kullanici_getir(kullanici_adi):

    return conn.execute(
        """
        SELECT *
        FROM kullanicilar
        WHERE kullanici_adi = ?
        """,
        (kullanici_adi,)
    ).fetchone()


# =========================================================
# DEĞERLENDİRME VAR MI?
# =========================================================

def degerlendirme_var_mi(kullanici_adi):

    sonuc = conn.execute(
        """
        SELECT id
        FROM degerlendirmeler
        WHERE kullanici_adi = ?
        """,
        (kullanici_adi,)
    ).fetchone()


    return sonuc is not None


# =========================================================
# EŞLEŞME VAR MI?
# =========================================================

def eslesme_var_mi(kullanici_adi):

    kullanici = kullanici_getir(kullanici_adi)


    if not kullanici or not kullanici["vibe"]:

        return False


    sonuc = conn.execute(
        """
        SELECT id
        FROM kullanicilar
        WHERE vibe = ?
        AND kullanici_adi != ?
        """,
        (
            kullanici["vibe"],
            kullanici_adi
        )
    ).fetchone()


    return sonuc is not None


# =========================================================
# GİRİŞ YAPILMADIYSA
# =========================================================

if not st.session_state.giris_yapildi:

    st.title("✨ EKİPLEN")

    st.write(
        "Yeni insanlarla tanış, vibe'ını keşfet "
        "ve sana uygun kişilerle eşleş! 💜"
    )


    st.divider()


    # =====================================================
    # KVKK
    # =====================================================

    kvkk_onay = st.checkbox(
        "KVKK metnini okudum ve kabul ediyorum."
    )


    st.markdown(
        """
        Kişisel verilerin işlenmesi hakkında bilgi almak için
        **KVKK** bölümünü inceleyebilirsin.
        """
    )


    kullanici_adi = st.text_input(
        "Kullanıcı adı"
    )


    if st.session_state.sifreyi_goster:

        sifre_tipi = "default"

    else:

        sifre_tipi = "password"


    sifre = st.text_input(
        "Şifre",
        type=sifre_tipi
    )


    sifre_goster = st.checkbox(
        "Şifreyi göster"
    )


    if sifre_goster != st.session_state.sifreyi_goster:

        st.session_state.sifreyi_goster = sifre_goster

        st.rerun()


    col1, col2 = st.columns(2)


    with col1:

        giris = st.button(
            "Giriş Yap",
            use_container_width=True
        )


    with col2:

        kayit = st.button(
            "Kayıt Ol",
            use_container_width=True
        )


    if giris:

        if not kvkk_onay:

            st.warning(
                "Devam etmek için KVKK metnini kabul etmelisin."
            )

        elif not kullanici_adi or not sifre:

            st.warning(
                "Kullanıcı adı ve şifreyi doldurmalısın."
            )

        else:

            kullanici = kullanici_getir(kullanici_adi)


            if kullanici and kullanici["sifre"] == sifre:

                st.session_state.giris_yapildi = True

                st.session_state.kullanici_adi = kullanici_adi

                st.session_state.profil_tamamlandi = True

                st.rerun()

            else:

                st.error(
                    "Kullanıcı adı veya şifre yanlış."
                )


    if kayit:

        if not kvkk_onay:

            st.warning(
                "Kayıt olmak için KVKK metnini kabul etmelisin."
            )

        elif not kullanici_adi or not sifre:

            st.warning(
                "Kullanıcı adı ve şifreyi doldurmalısın."
            )

        else:

            try:

                conn.execute(
                    """
                    INSERT INTO kullanicilar
                    (
                        kullanici_adi,
                        sifre,
                        avatar
                    )
                    VALUES (?, ?, ?)
                    """,
                    (
                        kullanici_adi,
                        sifre,
                        AVATARLAR[0]
                    )
                )


                conn.commit()


                st.session_state.giris_yapildi = True

                st.session_state.kullanici_adi = kullanici_adi

                st.session_state.profil_tamamlandi = False

                st.success(
                    "Kayıt başarılı! Şimdi profilini tamamlayabilirsin. 💜"
                )

                st.rerun()


            except sqlite3.IntegrityError:

                st.error(
                    "Bu kullanıcı adı zaten alınmış."
                )


    st.stop()


# =========================================================
# KULLANICI BİLGİLERİ
# =========================================================

kullanici_adi = st.session_state.kullanici_adi

kullanici = kullanici_getir(kullanici_adi)


# =========================================================
# ZORUNLU PROFİL
# =========================================================

if not st.session_state.profil_tamamlandi:

    st.title("👤 Profilini Tamamla")

    st.write(
        "EKİPLEN'e devam etmek için birkaç küçük bilgi ekleyelim. 💜"
    )


    avatar = st.radio(
        "Avatarını seç:",
        AVATARLAR,
        horizontal=True
    )


    instagram = st.text_input(
        "Instagram kullanıcı adın (isteğe bağlı)"
    )


    tiktok = st.text_input(
        "TikTok kullanıcı adın (isteğe bağlı)"
    )


    instagram_goster = st.checkbox(
        "Instagram hesabımı eşleştiğim kişiler görebilsin."
    )


    tiktok_goster = st.checkbox(
        "TikTok hesabımı eşleştiğim kişiler görebilsin."
    )


    if st.button(
        "💜 Profili Kaydet",
        use_container_width=True
    ):

        conn.execute(
            """
            UPDATE kullanicilar

            SET avatar = ?,
                instagram = ?,
                tiktok = ?,
                instagram_goster = ?,
                tiktok_goster = ?

            WHERE kullanici_adi = ?
            """,
            (
                avatar,
                instagram.strip(),
                tiktok.strip(),
                1 if instagram_goster else 0,
                1 if tiktok_goster else 0,
                kullanici_adi
            )
        )


        conn.commit()


        st.session_state.profil_tamamlandi = True

        st.success(
            "Profilin hazır! ✨"
        )

        st.rerun()


    st.stop()


# =========================================================
# ZORUNLU DEĞERLENDİRME
# =========================================================

if (
    eslesme_var_mi(kullanici_adi)
    and
    not degerlendirme_var_mi(kullanici_adi)
):

    st.title("⭐ Bizi Değerlendir")


    st.write(
        "Bir eşleşme gerçekleştirdin! 🎉 "
        "Şimdi EKİPLEN deneyimini birkaç kısa soruyla "
        "değerlendirmeni istiyoruz."
    )


    st.info(
        "Bu değerlendirme zorunludur. "
        "Cevaplarını gönderdikten sonra EKİPLEN'i "
        "kullanmaya devam edebilirsin. 💜"
    )


    st.divider()


    # SORU 1

    st.subheader(
        "1. Birisiyle arkadaşlık kurabildin mi?"
    )


    arkadaslik_kurabildin_mi = st.radio(
        "Cevabını seç:",
        [
            "Evet",
            "Hayır"
        ],
        key="degerlendirme_soru_1"
    )


    # SORU 2

    st.subheader(
        "2. Testler sence eğlenceli mi?"
    )


    testler_eglenceli_mi = st.radio(
        "Cevabını seç:",
        [
            "Evet",
            "Hayır",
            "Biraz"
        ],
        key="degerlendirme_soru_2"
    )


    # SORU 3

    st.subheader(
        "3. Neleri geliştirebiliriz?"
    )


    neleri_gelistirebiliriz = st.text_area(
        "Fikrini bizimle paylaş:",
        placeholder="Buraya düşüncelerini yazabilirsin...",
        key="degerlendirme_soru_3"
    )


    # SORU 4

    st.subheader(
        "4. Neyi beğendin veya beğenmedin?"
    )


    neyi_begendin_veya_begenmedin = st.text_area(
        "Düşüncelerini yaz:",
        placeholder="Beğendiğin veya beğenmediğin şeyleri yazabilirsin...",
        key="degerlendirme_soru_4"
    )


    st.divider()


    if st.button(
        "💜 Değerlendirmeyi Gönder",
        use_container_width=True
    ):

        if not neleri_gelistirebiliriz.strip():

            st.warning(
                "Lütfen 3. soruyu cevapla. 💭"
            )

        elif not neyi_begendin_veya_begenmedin.strip():

            st.warning(
                "Lütfen 4. soruyu cevapla. 💭"
            )

        else:

            conn.execute(
                """
                INSERT INTO degerlendirmeler
                (
                    kullanici_adi,
                    arkadaslik_kurabildin_mi,
                    testler_eglenceli_mi,
                    neleri_gelistirebiliriz,
                    neyi_begendin_veya_begenmedin
                )

                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    kullanici_adi,
                    arkadaslik_kurabildin_mi,
                    testler_eglenceli_mi,
                    neleri_gelistirebiliriz.strip(),
                    neyi_begendin_veya_begenmedin.strip()
                )
            )


            conn.commit()


            st.success(
                "Değerlendirmen için çok teşekkür ederiz! 💜✨"
            )


            st.balloons()

            st.rerun()


    st.stop()


# =========================================================
# MENÜ
# =========================================================

sayfa = st.sidebar.radio(
    "Menü",
    [
        "🏠 Ana Sayfa",
        "🧩 Vibe Testi",
        "👥 Arkadaş Eşleştirme",
        "👤 Profil",
        "👋 Biz Kimiz?",
        "📜 KVKK"
    ]
)


# =========================================================
# ÇIKIŞ
# =========================================================

if st.sidebar.button(
    "🚪 Çıkış Yap",
    use_container_width=True
):

    st.session_state.giris_yapildi = False

    st.session_state.kullanici_adi = None

    st.session_state.profil_tamamlandi = False

    st.rerun()


# =========================================================
# ANA SAYFA
# =========================================================

if sayfa == "🏠 Ana Sayfa":

    st.title("✨ EKİPLEN")


    st.write(
        f"Hoş geldin, **{kullanici_adi}**! 💜"
    )


    st.markdown(
        """
        <div class="kart">

        <h3>Burada neler yapabilirsin?</h3>

        <p>
        🧩 Vibe testini çözerek kendini keşfedebilirsin.
        </p>

        <p>
        👥 Seninle benzer vibe'a sahip kişilerle eşleşebilirsin.
        </p>

        <p>
        👤 Profilini düzenleyebilirsin.
        </p>

        <p>
        ✨ Yeni arkadaşlıklar kurabilirsin.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# VIBE TESTİ
# =========================================================

elif sayfa == "🧩 Vibe Testi":

    st.title("🧩 Vibe Testi")


    st.write(
        "Soruları cevapla ve hangi vibe'a sahip olduğunu keşfet! ✨"
    )


    sorular = [

        "Yeni insanlarla tanışmayı sever misin?",

        "Arkadaşlarınla dışarı çıkmak hoşuna gider mi?",

        "Yeni şeyler denemeyi sever misin?",

        "Kitap okumaktan hoşlanır mısın?",

        "Müzik dinlemek günlük hayatında önemli mi?",

        "Kalabalık ortamlarda eğlenir misin?",

        "Sessiz ve sakin bir ortamı tercih eder misin?",

        "Bir konuda araştırma yapmayı sever misin?",

        "Yeni bir hobi edinmek ister misin?",

        "Arkadaşlarınla uzun sohbetler yapar mısın?",

        "Macera yaşamaktan hoşlanır mısın?",

        "Film veya dizi izlemekten hoşlanır mısın?",

        "Müzik hakkında konuşmayı sever misin?",

        "Yalnız başına vakit geçirmekten hoşlanır mısın?",

        "Yeni insanlarla ortak noktalar keşfetmek hoşuna gider mi?"

    ]


    cevaplar = [
        "Çok severim",
        "Bazen",
        "Pek değil",
        "Hiç sevmem"
    ]


    puanlar = {
        "Çok severim": 4,
        "Bazen": 3,
        "Pek değil": 2,
        "Hiç sevmem": 1
    }


    toplam_puan = 0


    for i, soru in enumerate(sorular):

        st.subheader(
            f"{i + 1}. {soru}"
        )


        cevap = st.radio(
            "Cevabın:",
            cevaplar,
            key=f"soru_{i}"
        )


        toplam_puan += puanlar[cevap]


    st.divider()


    if st.button(
        "✨ Vibe'ımı Bul",
        use_container_width=True
    ):

        ortalama = toplam_puan / len(sorular)


        if ortalama >= 3.5:

            vibe = "Enerjik Kaşif"

        elif ortalama >= 2.8:

            vibe = "Sosyal Kelebek"

        elif ortalama >= 2.2:

            vibe = "Müzik Tutkunu"

        elif ortalama >= 1.6:

            vibe = "Kitap Kurdu"

        else:

            vibe = "Sakin Ruh"


        conn.execute(
            """
            UPDATE kullanicilar

            SET vibe = ?

            WHERE kullanici_adi = ?
            """,
            (
                vibe,
                kullanici_adi
            )
        )


        conn.commit()


        st.success(
            f"Senin vibe'ın: **{vibe}** ✨"
        )


# =========================================================
# ARKADAŞ EŞLEŞTİRME
# =========================================================

elif sayfa == "👥 Arkadaş Eşleştirme":

    st.title("👥 Arkadaş Eşleştirme")


    kullanici = kullanici_getir(kullanici_adi)


    if not kullanici["vibe"]:

        st.info(
            "Önce Vibe Testini çözmelisin. 🧩"
        )

    else:

        st.write(
            f"Senin vibe'ın: **{kullanici['vibe']}** ✨"
        )


        eslesmeler = conn.execute(
            """
            SELECT *

            FROM kullanicilar

            WHERE vibe = ?

            AND kullanici_adi != ?
            """,
            (
                kullanici["vibe"],
                kullanici_adi
            )
        ).fetchall()


        if not eslesmeler:

            st.info(
                "Henüz seninle aynı vibe'a sahip biri yok. 💜"
            )

        else:

            for kisi in eslesmeler:

                st.markdown(
                    f"""
                    <div class="kart">

                    <div class="avatar">
                    {kisi["avatar"]}
                    </div>

                    <h3>
                    {kisi["kullanici_adi"]}
                    </h3>

                    <p>
                    Vibe: {kisi["vibe"]}
                    </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                if (
                    kisi["instagram"]
                    and
                    kisi["instagram_goster"]
                ):

                    st.markdown(
                        f"""
                        <div class="sosyal-kutu">

                        📸 Instagram:
                        <a href="https://instagram.com/{kisi["instagram"].lstrip("@")}"
                        target="_blank">

                        @{kisi["instagram"].lstrip("@")}

                        </a>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                if (
                    kisi["tiktok"]
                    and
                    kisi["tiktok_goster"]
                ):

                    st.markdown(
                        f"""
                        <div class="sosyal-kutu">

                        🎵 TikTok:
                        <a href="https://www.tiktok.com/@{kisi["tiktok"].lstrip("@")}"
                        target="_blank">

                        @{kisi["tiktok"].lstrip("@")}

                        </a>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


# =========================================================
# PROFİL
# =========================================================

elif sayfa == "👤 Profil":

    st.title("👤 Profilim")


    kullanici = kullanici_getir(kullanici_adi)


    st.markdown(
        f"""
        <div class="kart">

        <div class="avatar">
        {kullanici["avatar"]}
        </div>

        <h2>
        {kullanici["kullanici_adi"]}
        </h2>

        <p>
        Vibe: {kullanici["vibe"] or "Henüz belirlenmedi"}
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.subheader("Profili Düzenle")


    yeni_avatar = st.radio(
        "Avatar",
        AVATARLAR,
        index=AVATARLAR.index(kullanici["avatar"]),
        horizontal=True
    )


    yeni_instagram = st.text_input(
        "Instagram",
        value=kullanici["instagram"] or ""
    )


    yeni_tiktok = st.text_input(
        "TikTok",
        value=kullanici["tiktok"] or ""
    )


    yeni_instagram_goster = st.checkbox(
        "Instagram'ı eşleştiğim kişiler görebilsin.",
        value=bool(kullanici["instagram_goster"])
    )


    yeni_tiktok_goster = st.checkbox(
        "TikTok'u eşleştiğim kişiler görebilsin.",
        value=bool(kullanici["tiktok_goster"])
    )


    if st.button(
        "💜 Profili Güncelle",
        use_container_width=True
    ):

        conn.execute(
            """
            UPDATE kullanicilar

            SET avatar = ?,
                instagram = ?,
                tiktok = ?,
                instagram_goster = ?,
                tiktok_goster = ?

            WHERE kullanici_adi = ?
            """,
            (
                yeni_avatar,
                yeni_instagram.strip(),
                yeni_tiktok.strip(),
                1 if yeni_instagram_goster else 0,
                1 if yeni_tiktok_goster else 0,
                kullanici_adi
            )
        )


        conn.commit()


        st.success(
            "Profilin güncellendi! ✨"
        )


        st.rerun()


# =========================================================
# BİZ KİMİZ?
# =========================================================

elif sayfa == "👋 Biz Kimiz?":

    st.title("👋 Biz Kimiz?")


    st.markdown(
        """
        <div class="kart">

        <h3>High Five Ekibi 💜</h3>

        <p>
        Merhaba! Biz High Five ekibiyiz. 👋
        </p>

        <p>
        Bu projeyi, 15-18 yaş arasındaki, yaşıtlarıyla iletişim
        kurmakta zorlanan kişiler için geliştirdik.
        </p>

        <p>
        Amacımız, eğlenceli testlerimizi cevaplayarak kendinize
        uygun kişilerle tanışmanızı ve yeni arkadaşlıklar
        kurmanızı sağlamak.
        </p>

        <p>
        İsterseniz Instagram, isterseniz TikTok hesabınızı
        paylaşarak eşleştiğiniz kişilerle iletişime geçebilir
        ya da sadece testleri çözerek sizler için oluşturduğumuz
        "Vibe Kartları"nı kazanabilirsiniz. ✨
        </p>

        <p>
        Şimdiden iyi eğlenceler! 🌸
        </p>

        <p>
        Sevgilerle,<br>
        High Five Ekibi 💜
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# KVKK
# =========================================================

elif sayfa == "📜 KVKK":

    st.title("📜 KVKK")


    st.markdown(
        """
        <div class="kart">

        <h3>Kişisel Verilerin Korunması</h3>

        <p>
        EKİPLEN içerisinde kullanıcı adı, şifre, avatar seçimi,
        Vibe Testi sonucu ve kullanıcı tarafından isteğe bağlı
        olarak paylaşılan Instagram ve TikTok bilgileri
        işlenebilir.
        </p>

        <p>
        Instagram ve TikTok bilgilerinin diğer kullanıcılarla
        gösterilip gösterilmeyeceğine kullanıcı kendisi karar verir.
        </p>

        <p>
        Kullanıcıların değerlendirme bölümünde yazdığı cevaplar
        da uygulamanın geliştirilmesi amacıyla saklanabilir.
        </p>

        <p>
        Kişisel verilerin güvenliği için gerekli teknik ve idari
        önlemlerin alınması amaçlanmaktadır.
        </p>

        <p>
        Kullanıcılar, kişisel verileriyle ilgili yasal hakları
        kapsamında bilgi talep edebilir, düzeltme veya silme
        taleplerinde bulunabilir.
        </p>

        <p>
        EKİPLEN bir proje/teknik çalışma örneğidir. Gerçek kullanıcı
        verileriyle kullanıma açılmadan önce uygun güvenlik,
        gizlilik ve hukuki düzenlemelerin ayrıca değerlendirilmesi gerekir.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )
