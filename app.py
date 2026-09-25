import sqlite3
import streamlit as st

YONETICI_SIFRE = "EKİPLENSİNN05"

st.set_page_config(page_title="EKİPLEN", page_icon="✨", layout="centered")

st.markdown("""
<style>
/* GENEL SAYFA */
.stApp {
    background-color: #171321;
    color: white;
}

/* BAŞLIKLAR */
h1, h2, h3, h4 {
    font-family: Georgia, serif;
    color: white !important;
}

/* NORMAL YAZILAR */
p, label, span, div {
    color: white;
}

/* RADIO VE CHECKBOX YAZILARI */
.stRadio label p,
.stCheckbox label p {
    color: white !important;
}

/* INPUTLAR */
.stTextInput input,
.stTextArea textarea {
    background-color: #241e2e !important;
    color: white !important;
    border: 1px solid #8f70ad !important;
    border-radius: 12px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #c9bfd2 !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #c49be8 !important;
}

/* BUTONLAR */
.stButton > button {
    background-color: #8f70ad;
    color: white !important;
    border-radius: 12px;
    border: none;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #a984c5;
    color: white !important;
    transform: translateY(-2px);
}

/* YAN MENÜ */
section[data-testid="stSidebar"] {
    background-color: #211b2b;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* KARTLAR */
.kart {
    background: #241e2e;
    color: white;
    border-radius: 20px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 5px 20px rgba(0,0,0,.35);
    border: 1px solid #3d304b;
}

.kart h2,
.kart h3,
.kart p {
    color: white !important;
}

/* AVATAR */
.avatar {
    font-size: 55px;
    text-align: center;
}

/* PUANTİYE ARKA PLAN */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;

    background-image:
        radial-gradient(circle, rgba(255,216,77,.25) 2px, transparent 3px),
        radial-gradient(circle, rgba(190,150,255,.20) 2px, transparent 3px);

    background-size: 80px 80px, 110px 110px;

    animation: hareket 20s linear infinite;
}

@keyframes hareket {
    from {
        background-position: 0 0, 30px 30px;
    }

    to {
        background-position: 160px 160px, 200px 200px;
    }
}

/* VIBE KARTI */
.vibe-kart {
    border-radius: 25px;
    padding: 30px 20px;
    margin-top: 25px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(0,0,0,.35);
}

.vibe-emoji {
    font-size: 58px;
}

.vibe-baslik {
    font-family: Georgia, serif;
    font-size: 30px;
    font-weight: bold;
    color: #3e3045 !important;
    margin-top: 5px;
}

.vibe-yazi {
    color: #4b414f !important;
    font-size: 16px;
    line-height: 1.6;
    margin-top: 10px;
}

.vibe-alt {
    color: #665b6d !important;
    font-size: 14px;
    margin-top: 15px;
}
</style>
""", unsafe_allow_html=True)


def veritabani():
    conn = sqlite3.connect("ekiplen.db")
    conn.row_factory = sqlite3.Row
    
    conn.execute("""
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
    """)
    
    kolonlar = conn.execute("PRAGMA table_info(kullanicilar)").fetchall()
    kolon_isimleri = [x["name"] for x in kolonlar]
    
    if "instagram_goster" not in kolon_isimleri:
        conn.execute("ALTER TABLE kullanicilar ADD COLUMN instagram_goster INTEGER DEFAULT 0")
    if "tiktok_goster" not in kolon_isimleri:
        conn.execute("ALTER TABLE kullanicilar ADD COLUMN tiktok_goster INTEGER DEFAULT 0")
        
    conn.execute("""
        CREATE TABLE IF NOT EXISTS degerlendirmeler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_adi TEXT UNIQUE NOT NULL,
            arkadaslik_kurabildin_mi TEXT NOT NULL,
            testler_eglenceli_mi TEXT NOT NULL,
            neleri_gelistirebiliriz TEXT NOT NULL,
            neyi_begendin_veya_begenmedin TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Kullanıcı şikayetleri
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sikayetler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_adi TEXT NOT NULL,
            konu TEXT NOT NULL,
            mesaj TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    return conn


conn = veritabani()

AVATARLAR = ["🌙", "⭐", "🌸", "🦋", "🐱", "🐼", "🦊", "🐨", "🌻", "🍀"]


# Session state kontrolleri
if "giris_yapildi" not in st.session_state:
    st.session_state.giris_yapildi = False

if "kullanici_adi" not in st.session_state:
    st.session_state.kullanici_adi = None

if "profil_tamamlandi" not in st.session_state:
    st.session_state.profil_tamamlandi = False

if "sifreyi_goster" not in st.session_state:
    st.session_state.sifreyi_goster = False

if "yonetici_giris" not in st.session_state:
    st.session_state.yonetici_giris = False


def kullanici_getir(ad):
    return conn.execute(
        "SELECT * FROM kullanicilar WHERE kullanici_adi = ?",
        (ad,)
    ).fetchone()


def degerlendirme_var_mi(ad):
    sonuc = conn.execute(
        "SELECT id FROM degerlendirmeler WHERE kullanici_adi = ?",
        (ad,)
    ).fetchone()

    return sonuc is not None


def eslesme_var_mi(ad):
    kisi = kullanici_getir(ad)

    if not kisi or not kisi["vibe"]:
        return False

    sonuc = conn.execute(
        "SELECT id FROM kullanicilar WHERE vibe = ? AND kullanici_adi != ?",
        (kisi["vibe"], ad)
    ).fetchone()

    return sonuc is not None


def kvkk_metni():
    st.markdown("""
### 📜 EKİPLEN KVKK Aydınlatma Metni

**1. Veri Sorumlusu:** EKİPLEN projesinde verilerinizin güvenliğine önem veriyoruz.

**2. İşlenen Bilgiler:** Kullanıcı adı, şifre, avatar, Vibe sonucu ve isteğe bağlı sosyal medya hesapları.

**3. Amaç:** Platform içi arkadaş eşleştirmesi ve deneyimi iyileştirme.

**4. Sosyal Medya & Avatar:** Tamamen isteğe bağlıdır, standart avatarlar kullanılır.

**5. Haklarınız:** 6698 sayılı KVKK kapsamındaki haklara sahipsiniz.
""")


# Giriş Ekranı
if not st.session_state.giris_yapildi:

    st.title("✨ EKİPLEN")

    st.subheader("Lise Arkadaşlık ve Sosyal Ağ Platformu")

    st.write(
        "Kendini tanıyabilir, sana benzeyen kişilerle eşleşebilir "
        "ve yeni arkadaşlıklar keşfedebilirsin. 💜"
    )

    st.divider()

    kullanici_adi = st.text_input(
        "👤 Kullanıcı adı",
        placeholder="Kullanıcı adını yaz..."
    )

    col1, col2 = st.columns([5, 1])

    with col1:
        sifre = st.text_input(
            "🔐 Şifre",
            type="default" if st.session_state.sifreyi_goster else "password",
            placeholder="Şifreni yaz..."
        )

    with col2:
        st.write("")

        if st.button(
            "🙈" if st.session_state.sifreyi_goster else "👁️"
        ):
            st.session_state.sifreyi_goster = not st.session_state.sifreyi_goster
            st.rerun()

    with st.expander("📜 KVKK Aydınlatma Metni"):
        kvkk_metni()

    kvkk_onay = st.checkbox(
        "KVKK Aydınlatma Metnini okudum ve onaylıyorum."
    )

    if st.button("✨ Giriş Yap", use_container_width=True):

        if not kullanici_adi.strip() or not sifre.strip():
            st.warning("Kullanıcı adı ve şifreyi doldurmalısın.")

        elif not kvkk_onay:
            st.warning("Devam etmek için KVKK metnini onaylamalısın.")

        else:
            kisi = kullanici_getir(kullanici_adi.strip())

            if kisi:

                if kisi["sifre"] == sifre:
                    st.session_state.giris_yapildi = True
                    st.session_state.kullanici_adi = kullanici_adi.strip()
                    st.session_state.profil_tamamlandi = True

                    st.success(
                        f"Tekrar hoş geldin, {kullanici_adi}! ✨"
                    )

                    st.rerun()

                else:
                    st.error("Şifre yanlış.")

            else:

                conn.execute(
                    """
                    INSERT INTO kullanicilar
                    (kullanici_adi, sifre, avatar)
                    VALUES (?, ?, ?)
                    """,
                    (
                        kullanici_adi.strip(),
                        sifre,
                        AVATARLAR[0]
                    )
                )

                conn.commit()

                st.session_state.giris_yapildi = True
                st.session_state.kullanici_adi = kullanici_adi.strip()
                st.session_state.profil_tamamlandi = False

                st.success("Hesabın oluşturuldu! 🌸")
                st.rerun()

    st.stop()


kullanici_adi = st.session_state.kullanici_adi
kullanici = kullanici_getir(kullanici_adi)

if not kullanici:
    st.error("Kullanıcı bulunamadı.")
    st.stop()


# Profil Oluşturma Ekranı
if not st.session_state.profil_tamamlandi:

    st.title("🌸 Profilini Oluştur")

    st.write(
        f"Hoş geldin **{kullanici_adi}**! Önce kendine bir avatar seç."
    )

    avatar = st.radio(
        "✨ Avatar seç",
        AVATARLAR,
        horizontal=True
    )

    instagram = st.text_input(
        "📸 Instagram kullanıcı adın",
        placeholder="@kullaniciadi"
    )

    tiktok = st.text_input(
        "🎵 TikTok kullanıcı adın",
        placeholder="@kullaniciadi"
    )

    st.subheader("🔒 Sosyal Medya Tercihleri")

    instagram_goster = st.checkbox(
        "Instagram hesabımı eşleştiğim kişiye göster"
    )

    tiktok_goster = st.checkbox(
        "TikTok hesabımı eşleştiğim kişiye göster"
    )

    if st.button(
        "💜 Profilimi Oluştur",
        use_container_width=True
    ):

        conn.execute("""
            UPDATE kullanicilar
            SET avatar = ?,
                instagram = ?,
                tiktok = ?,
                instagram_goster = ?,
                tiktok_goster = ?
            WHERE kullanici_adi = ?
        """, (
            avatar,
            instagram.strip(),
            tiktok.strip(),
            int(instagram_goster),
            int(tiktok_goster),
            kullanici_adi
        ))

        conn.commit()

        st.session_state.profil_tamamlandi = True

        st.success("Profilin hazır! 🎉")
        st.rerun()

    st.stop()


# Değerlendirme Ekranı
if eslesme_var_mi(kullanici_adi) and not degerlendirme_var_mi(kullanici_adi):

    st.title("⭐ Bizi Değerlendir")

    st.write(
        "Bir eşleşme gerçekleştirdin! EKİPLEN deneyimini "
        "kısaca değerlendirebilir misin?"
    )

    arkadaslik = st.radio(
        "1. Birisiyle arkadaşlık kurabildin mi?",
        ["Evet", "Hayır"]
    )

    testler = st.radio(
        "2. Testler sence eğlenceli mi?",
        ["Evet", "Hayır", "Biraz"]
    )

    gelistirme = st.text_area(
        "3. Neleri geliştirebiliriz?"
    )

    begendin = st.text_area(
        "4. Neyi beğendin veya beğenmedin?"
    )

    if st.button(
        "💜 Değerlendirmeyi Gönder",
        use_container_width=True
    ):

        if not gelistirme.strip() or not begendin.strip():
            st.warning("Lütfen boş bırakılan alanları doldur.")

        else:

            conn.execute("""
                INSERT INTO degerlendirmeler
                (
                    kullanici_adi,
                    arkadaslik_kurabildin_mi,
                    testler_eglenceli_mi,
                    neleri_gelistirebiliriz,
                    neyi_begendin_veya_begenmedin
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                kullanici_adi,
                arkadaslik,
                testler,
                gelistirme.strip(),
                begendin.strip()
            ))

            conn.commit()

            st.success(
                "Değerlendirmen için teşekkürler! 💜"
            )

            st.balloons()
            st.rerun()

    st.stop()


# Ana Sayfa ve Menü
st.title("✨ EKİPLEN")

st.write(
    f"Hoş geldin **{kullanici_adi}** {kullanici['avatar']}"
)


sayfa = st.sidebar.radio(
    "Menü",
    [
        "🏠 Ana Sayfa",
        "🧩 Vibe Testi",
        "👥 Arkadaş Eşleştirme",
        "👤 Profil",
        "⚠️ Şikayet / Bildirim",
        "👋 Biz Kimiz?",
        "📜 KVKK",
        "🔐 Yönetici"
    ]
)


if st.sidebar.button("🚪 Çıkış Yap"):

    st.session_state.giris_yapildi = False
    st.session_state.kullanici_adi = None
    st.session_state.profil_tamamlandi = False
    st.session_state.yonetici_giris = False

    st.rerun()


if sayfa == "🏠 Ana Sayfa":

    st.header("🌷 Hoş geldin!")

    st.write(
        "EKİPLEN'de önce kendi Vibe'ını bulabilir, "
        "sonra sana benzeyen kişilerle eşleşebilirsin."
    )

    st.info(
        "🧩 Önce Vibe Testi'ni tamamla. "
        "Sonra Arkadaş Eşleştirme bölümüne bakabilirsin."
    )


elif sayfa == "🧩 Vibe Testi":

    st.header("🧩 Vibe Testi")

    st.write(
        "Sana en yakın cevabı seç. Test bitince Vibe'ın çıkacak. ✨"
    )

    sorular = [
        {
            "soru": "Boş zamanında en çok ne yaparsın?",
            "cevaplar": [
                ("Yeni yerler keşfetmeye çıkarım.", "Enerjik Kaşif"),
                ("Arkadaşlarımla buluşurum.", "Sosyal Kelebek"),
                ("Müzik dinler, yeni şarkılar bulurum.", "Müzik Tutkunu"),
                ("Kitap okur veya sakin bir şeyler yaparım.", "Kitap Kurdu")
            ]
        },
        {
            "soru": "Arkadaşların seni nasıl tanımlar?",
            "cevaplar": [
                ("Yerimde duramam, sürekli bir şey yapmak isterim.", "Enerjik Kaşif"),
                ("Konuşkan ve insanlarla kolay anlaşan biriyim.", "Sosyal Kelebek"),
                ("Müzik konusunda bayağı ilgiliyim.", "Müzik Tutkunu"),
                ("Sessiz, sakin ve düşünceli biriyim.", "Sakin Ruh")
            ]
        },
        {
            "soru": "Bir hafta sonunu nasıl geçirmek isterdin?",
            "cevaplar": [
                ("Daha önce gitmediğim bir yere giderdim.", "Enerjik Kaşif"),
                ("Arkadaş grubumla dışarı çıkardım.", "Sosyal Kelebek"),
                ("Konser veya müzik etkinliğine giderdim.", "Müzik Tutkunu"),
                ("Evde kitap okuyup dinlenirdim.", "Kitap Kurdu")
            ]
        },
        {
            "soru": "En sevdiğin ortam hangisi?",
            "cevaplar": [
                ("Doğa, geziler ve yeni yerler.", "Enerjik Kaşif"),
                ("Kalabalık ve eğlenceli ortamlar.", "Sosyal Kelebek"),
                ("Konser, müzik odası veya festival.", "Müzik Tutkunu"),
                ("Kütüphane veya sessiz bir kafe.", "Sakin Ruh")
            ]
        },
        {
            "soru": "Yeni insanlarla tanışmak hakkında ne düşünüyorsun?",
            "cevaplar": [
                ("Yeni insanlarla tanışmak bana macera gibi geliyor.", "Enerjik Kaşif"),
                ("Hemen sohbet başlatabilirim.", "Sosyal Kelebek"),
                ("Ortak müzik zevkimiz varsa daha kolay kaynaşırım.", "Müzik Tutkunu"),
                ("Önce biraz gözlemler, sonra konuşurum.", "Sakin Ruh")
            ]
        },
        {
            "soru": "Müzik senin için ne ifade ediyor?",
            "cevaplar": [
                ("Yolculuklarda çok iyi gidiyor.", "Enerjik Kaşif"),
                ("Arkadaşlarla beraber dinlemek daha güzel.", "Sosyal Kelebek"),
                ("Günümün büyük bir parçası.", "Müzik Tutkunu"),
                ("Sakinleşmek için dinlerim.", "Sakin Ruh")
            ]
        },
        {
            "soru": "Kitap okumayı seviyor musun?",
            "cevaplar": [
                ("Macera kitaplarını özellikle severim.", "Enerjik Kaşif"),
                ("Arkadaşlarımla kitap önerileri paylaşmayı severim.", "Sosyal Kelebek"),
                ("Müzik ve sanatla ilgili kitaplar ilgimi çeker.", "Müzik Tutkunu"),
                ("Kitap okumak benim için vazgeçilmez.", "Kitap Kurdu")
            ]
        },
        {
            "soru": "Bir arkadaşında en çok neye önem verirsin?",
            "cevaplar": [
                ("Birlikte yeni şeyler deneyebilmemize.", "Enerjik Kaşif"),
                ("Eğlenceli ve konuşkan olmasına.", "Sosyal Kelebek"),
                ("Ortak ilgi alanlarımız olmasına.", "Müzik Tutkunu"),
                ("Beni anlayıp güven vermesine.", "Sakin Ruh")
            ]
        },
        {
            "soru": "Bir sorun olduğunda ne yaparsın?",
            "cevaplar": [
                ("Hemen çözüm bulmaya çalışırım.", "Enerjik Kaşif"),
                ("Bir arkadaşıma anlatırım.", "Sosyal Kelebek"),
                ("Biraz müzik dinleyip kafamı toparlarım.", "Müzik Tutkunu"),
                ("Önce yalnız kalıp düşünürüm.", "Sakin Ruh")
            ]
        },
        {
            "soru": "Kalabalık ortamlar hakkında hangisi sana daha yakın?",
            "cevaplar": [
                ("Yeni şeyler olduğu için hoşuma gider.", "Enerjik Kaşif"),
                ("Kalabalık ve eğlenceli yerleri severim.", "Sosyal Kelebek"),
                ("Konser veya festivalse kesinlikle giderim.", "Müzik Tutkunu"),
                ("Daha küçük ve sakin ortamları tercih ederim.", "Sakin Ruh")
            ]
        },
        {
            "soru": "Hayalindeki tatil nasıl olurdu?",
            "cevaplar": [
                ("Farklı şehirler ve ülkeler keşfetmek.", "Enerjik Kaşif"),
                ("Arkadaş grubumla bol bol eğlenmek.", "Sosyal Kelebek"),
                ("Müzik festivali veya konsere gitmek.", "Müzik Tutkunu"),
                ("Sessiz bir yerde kitap okuyup dinlenmek.", "Kitap Kurdu")
            ]
        },
        {
            "soru": "En çok hangi özelliğine güveniyorsun?",
            "cevaplar": [
                ("Meraklı ve cesur olmama.", "Enerjik Kaşif"),
                ("İnsanlarla kolay iletişim kurmama.", "Sosyal Kelebek"),
                ("Yaratıcılığıma ve müzik zevkime.", "Müzik Tutkunu"),
                ("Düşünceli ve sakin olmama.", "Sakin Ruh")
            ]
        },
        {
            "soru": "Yeni şeyler denemek konusunda nasılsın?",
            "cevaplar": [
                ("İlk deneyenlerden biri olurum.", "Enerjik Kaşif"),
                ("Arkadaşlarımla beraber denerim.", "Sosyal Kelebek"),
                ("Müzikle ilgiliyse kesin denerim.", "Müzik Tutkunu"),
                ("Önce araştırır, sonra karar veririm.", "Kitap Kurdu")
            ]
        },
        {
            "soru": "Arkadaşlık senin için en çok ne demek?",
            "cevaplar": [
                ("Birlikte macera yaşamak.", "Enerjik Kaşif"),
                ("Sürekli iletişimde olmak ve eğlenmek.", "Sosyal Kelebek"),
                ("Ortak ilgi alanları paylaşmak.", "Müzik Tutkunu"),
                ("Güvenmek ve rahatça konuşabilmek.", "Sakin Ruh")
            ]
        },
        {
            "soru": "Kendini en çok hangisine yakın hissediyorsun?",
            "cevaplar": [
                ("Meraklı ve keşfetmeyi seven.", "Enerjik Kaşif"),
                ("Sosyal ve hareketli.", "Sosyal Kelebek"),
                ("Yaratıcı ve müzik seven.", "Müzik Tutkunu"),
                ("Kitap okumayı ve düşünmeyi seven.", "Kitap Kurdu")
            ]
        }
    ]

    puanlar = {
        "Enerjik Kaşif": 0,
        "Sakin Ruh": 0,
        "Kitap Kurdu": 0,
        "Müzik Tutkunu": 0,
        "Sosyal Kelebek": 0
    }

    cevaplar = []

    for i, soru in enumerate(sorular):

        st.markdown(
            f"### {i + 1}. {soru['soru']}"
        )

        secenekler = [
            cevap for cevap, vibe in soru["cevaplar"]
        ]

        secim = st.radio(
            "Cevabın:",
            secenekler,
            key=f"soru_{i}"
        )

        cevaplar.append(secim)

    if st.button(
        "✨ Vibe'ımı Bul",
        use_container_width=True
    ):

        for i in range(len(sorular)):

            for cevap, vibe in sorular[i]["cevaplar"]:

                if cevap == cevaplar[i]:
                    puanlar[vibe] += 1

        en_yuksek = max(puanlar.values())

        kazananlar = [
            vibe
            for vibe, puan in puanlar.items()
            if puan == en_yuksek
        ]

        vibe = kazananlar[0]

        conn.execute(
            "UPDATE kullanicilar SET vibe = ? WHERE kullanici_adi = ?",
            (vibe, kullanici_adi)
        )

        conn.commit()

        bilgiler = {
            "Enerjik Kaşif": (
                "🧭",
                "#ffe5b4",
                "Yeni şeyler keşfetmeyi, gezmeyi ve farklı deneyimler yaşamayı seviyorsun. Yerinde durmak sana göre değil!"
            ),

            "Sakin Ruh": (
                "🌿",
                "#dcefe3",
                "Daha sakin ortamlardan hoşlanıyor, huzuru ve güveni önemsiyorsun. Kendi alanında vakit geçirmek sana iyi geliyor."
            ),

            "Kitap Kurdu": (
                "📚",
                "#e8ddf5",
                "Hayal gücün güçlü ve yeni şeyler öğrenmeyi seviyorsun. Kitaplar ve hikayeler senin dünyanda önemli."
            ),

            "Müzik Tutkunu": (
                "🎵",
                "#f3d9e8",
                "Müzik senin için sadece arka planda çalan bir şey değil. Ruh halini ve anılarını etkiliyor."
            ),

            "Sosyal Kelebek": (
                "🦋",
                "#ffe0d0",
                "İnsanlarla konuşmayı, birlikte vakit geçirmeyi ve yeni arkadaşlıklar kurmayı seviyorsun."
            )
        }

        emoji, renk, aciklama = bilgiler[vibe]

        st.markdown(f"""
        <div class="vibe-kart" style="background-color:{renk};">
            <div class="vibe-emoji">{emoji}</div>
            <div class="vibe-baslik">Senin Vibe'ın: {vibe}</div>
            <div class="vibe-yazi">{aciklama}</div>
            <div class="vibe-alt">✨ Bu sonuç cevaplarına göre oluşturuldu.</div>
        </div>
        """, unsafe_allow_html=True)

        st.balloons()


elif sayfa == "👥 Arkadaş Eşleştirme":

    st.header("👥 Arkadaş Eşleştirme")

    kullanici = kullanici_getir(kullanici_adi)

    if not kullanici["vibe"]:

        st.warning(
            "Önce Vibe Testi'ni tamamlamalısın. 🧩"
        )

    else:

        st.success(
            f"Senin Vibe'ın: **{kullanici['vibe']}**"
        )

        kisiler = conn.execute(
            """
            SELECT * FROM kullanicilar
            WHERE vibe = ? AND kullanici_adi != ?
            """,
            (kullanici["vibe"], kullanici_adi)
        ).fetchall()

        if not kisiler:

            st.info(
                "Şimdilik seninle aynı Vibe'a sahip başka biri yok."
            )

        else:

            st.subheader("✨ Sana uyumlu kişiler")

            for kisi in kisiler:

                st.markdown(f"""
                <div class="kart">
                    <div class="avatar">{kisi['avatar']}</div>
                    <h3 style="text-align:center;">{kisi['kullanici_adi']}</h3>
                    <p style="text-align:center;">🧩 {kisi['vibe']}</p>
                </div>
                """, unsafe_allow_html=True)

                if kisi["instagram"] and kisi["instagram_goster"]:

                    ig = kisi["instagram"].strip().replace("@", "")

                    st.markdown(
                        f"📸 Instagram: [@{ig}](https://instagram.com/{ig})"
                    )

                if kisi["tiktok"] and kisi["tiktok_goster"]:

                    tt = kisi["tiktok"].strip().replace("@", "")

                    st.markdown(
                        f"🎵 TikTok: [@{tt}](https://www.tiktok.com/@{tt})"
                    )

                if (
                    (not kisi["instagram"] or not kisi["instagram_goster"])
                    and
                    (not kisi["tiktok"] or not kisi["tiktok_goster"])
                ):
                    st.caption(
                        "Bu kullanıcı sosyal medya hesaplarını göstermiyor."
                    )

                st.divider()


elif sayfa == "👤 Profil":

    st.header("👤 Profilim")

    kullanici = kullanici_getir(kullanici_adi)

    st.markdown(f"""
    <div class="kart">
        <div class="avatar">{kullanici['avatar']}</div>
        <h2 style="text-align:center;">{kullanici['kullanici_adi']}</h2>
    </div>
    """, unsafe_allow_html=True)

    if kullanici["vibe"]:
        st.write(
            f"🧩 **Vibe:** {kullanici['vibe']}"
        )
    else:
        st.write(
            "🧩 Vibe testini henüz tamamlamadın."
        )

    st.divider()

    st.subheader("🔗 Sosyal Medya")

    if kullanici["instagram"]:

        ig = kullanici["instagram"].strip().replace("@", "")

        st.markdown(
            f"📸 **Instagram:** [@{ig}](https://instagram.com/{ig})"
        )

        st.caption(
            "🔓 Eşleştiğin kişiler görebilir."
            if kullanici["instagram_goster"]
            else
            "🔒 Eşleştiğin kişiler göremez."
        )

    if kullanici["tiktok"]:

        tt = kullanici["tiktok"].strip().replace("@", "")

        st.markdown(
            f"🎵 **TikTok:** [@{tt}](https://www.tiktok.com/@{tt})"
        )

        st.caption(
            "🔓 Eşleştiğin kişiler görebilir."
            if kullanici["tiktok_goster"]
            else
            "🔒 Eşleştiğin kişiler göremez."
        )

    if not kullanici["instagram"] and not kullanici["tiktok"]:
        st.caption(
            "Henüz sosyal medya hesabı eklemedin."
        )

    st.divider()

    st.subheader("✏️ Profili Düzenle")

    avatar = st.radio(
        "Avatar",
        AVATARLAR,
        index=AVATARLAR.index(kullanici["avatar"])
        if kullanici["avatar"] in AVATARLAR else 0,
        horizontal=True
    )

    instagram = st.text_input(
        "📸 Instagram",
        value=kullanici["instagram"] or "",
        placeholder="@kullaniciadi"
    )

    tiktok = st.text_input(
        "🎵 TikTok",
        value=kullanici["tiktok"] or "",
        placeholder="@kullaniciadi"
    )

    instagram_goster = st.checkbox(
        "Instagram hesabımı eşleştiğim kişiye göster",
        value=bool(kullanici["instagram_goster"])
    )

    tiktok_goster = st.checkbox(
        "TikTok hesabımı eşleştiğim kişiye göster",
        value=bool(kullanici["tiktok_goster"])
    )

    if st.button(
        "💾 Profili Kaydet",
        use_container_width=True
    ):

        conn.execute("""
            UPDATE kullanicilar
            SET avatar = ?,
                instagram = ?,
                tiktok = ?,
                instagram_goster = ?,
                tiktok_goster = ?
            WHERE kullanici_adi = ?
        """, (
            avatar,
            instagram.strip(),
            tiktok.strip(),
            int(instagram_goster),
            int(tiktok_goster),
            kullanici_adi
        ))

        conn.commit()

        st.success(
            "Profil güncellendi! 💜"
        )

        st.rerun()


# Şikayet / Bildirim
elif sayfa == "⚠️ Şikayet / Bildirim":

    st.header("⚠️ Şikayet / Bildirim")

    st.write(
        "Sitede yaşadığın bir sorun varsa veya bildirmek "
        "istediğin bir durum varsa buradan bize ulaşabilirsin."
    )

    konu = st.text_input(
        "Konu",
        placeholder="Örneğin: Bir kullanıcı hakkında bildirim"
    )

    mesaj = st.text_area(
        "Mesajın",
        placeholder="Sorunu veya bildirmek istediğin durumu yaz..."
    )

    if st.button(
        "📩 Bildirimi Gönder",
        use_container_width=True
    ):

        if not konu.strip() or not mesaj.strip():

            st.warning(
                "Lütfen konu ve mesaj alanlarını doldur."
            )

        else:

            conn.execute(
                """
                INSERT INTO sikayetler
                (kullanici_adi, konu, mesaj)
                VALUES (?, ?, ?)
                """,
                (
                    kullanici_adi,
                    konu.strip(),
                    mesaj.strip()
                )
            )

            conn.commit()

            st.success(
                "Bildirimin yöneticiye gönderildi. Teşekkürler! 💜"
            )

            st.rerun()


elif sayfa == "👋 Biz Kimiz?":

    st.title("👋 Biz Kimiz?")

    st.markdown("""
    <div class="kart">
        <h2 style="text-align:center;">💜 High Five Ekibi</h2>

        <p>Merhaba! Biz <b>High Five ekibiyiz.</b> 👋</p>

        <p>
        Bu projeyi 15-18 yaş arasındaki kişilerin
        yaşıtlarıyla tanışabilmesi ve yeni arkadaşlıklar
        kurabilmesi için yaptık.
        </p>

        <p>
        Vibe testlerini çözerek kendine uygun kişileri
        bulabilir, istersen Instagram veya TikTok hesabını
        paylaşabilirsin.
        </p>

        <p>İyi eğlenceler! 🌸</p>

        <p style="text-align:center;">
            <b>Sevgilerle,<br>High Five Ekibi 💜</b>
        </p>
    </div>
    """, unsafe_allow_html=True)


elif sayfa == "📜 KVKK":

    st.title("📜 KVKK")

    kvkk_metni()


elif sayfa == "🔐 Yönetici":

    st.title("🔐 Yönetici Paneli")

    if not st.session_state.yonetici_giris:

        sifre = st.text_input(
            "Yönetici şifresi",
            type="password"
        )

        if st.button(
            "🔓 Giriş Yap",
            use_container_width=True
        ):

            if sifre == YONETICI_SIFRE:

                st.session_state.yonetici_giris = True
                st.rerun()

            else:

                st.error("Şifre yanlış.")

    else:

        # Toplam kullanıcı sayısı
        toplam_kullanici = conn.execute(
            "SELECT COUNT(*) FROM kullanicilar"
        ).fetchone()[0]

        st.metric(
            "👥 Toplam Kullanıcı",
            toplam_kullanici
        )

        st.divider()

        # Değerlendirmeler
        st.subheader("⭐ Değerlendirmeler")

        degerlendirmeler = conn.execute(
            """
            SELECT * FROM degerlendirmeler
            ORDER BY created_at DESC
            """
        ).fetchall()

        if not degerlendirmeler:

            st.info(
                "Henüz değerlendirme yok."
            )

        else:

            for d in degerlendirmeler:

                st.markdown(f"""
                <div class="kart">

                    <h3>👤 {d['kullanici_adi']}</h3>

                    <p>
                        <b>Arkadaşlık kurabildin mi?</b><br>
                        {d['arkadaslik_kurabildin_mi']}
                    </p>

                    <p>
                        <b>Testler eğlenceli mi?</b><br>
                        {d['testler_eglenceli_mi']}
                    </p>

                    <p>
                        <b>Neleri geliştirebiliriz?</b><br>
                        {d['neleri_gelistirebiliriz']}
                    </p>

                    <p>
                        <b>Neyi beğendin veya beğenmedin?</b><br>
                        {d['neyi_begendin_veya_begenmedin']}
                    </p>

                    <p>
                        <b>Tarih:</b> {d['created_at']}
                    </p>

                </div>
                """, unsafe_allow_html=True)

        # Şikayetler
        st.divider()

        st.subheader("⚠️ Kullanıcı Şikayetleri")

        sikayetler = conn.execute(
            """
            SELECT * FROM sikayetler
            ORDER BY created_at DESC
            """
        ).fetchall()

        if not sikayetler:

            st.info(
                "Henüz bir şikayet veya bildirim yok."
            )

        else:

            for s in sikayetler:

                st.markdown(f"""
                <div class="kart">

                    <h3>⚠️ {s['konu']}</h3>

                    <p>
                        <b>👤 Kullanıcı:</b>
                        {s['kullanici_adi']}
                    </p>

                    <p>
                        <b>💬 Mesaj:</b><br>
                        {s['mesaj']}
                    </p>

                    <p>
                        <b>📅 Tarih:</b>
                        {s['created_at']}
                    </p>

                </div>
                """, unsafe_allow_html=True)

        if st.button(
            "🚪 Yönetici Çıkışı",
            use_container_width=True
        ):

            st.session_state.yonetici_giris = False
            st.rerun()
