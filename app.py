import sqlite3
import streamlit as st


# =========================================================
# SAYFA AYARLARI
# =========================================================

st.set_page_config(
    page_title="EKİPLEN",
    page_icon="✨",
    layout="centered"
)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: #fffaf2;
    color: #333333;
}

/* Hareketli noktalar */

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;

    background-image:
        radial-gradient(
            circle,
            rgba(255,190,120,0.30) 2px,
            transparent 3px
        ),
        radial-gradient(
            circle,
            rgba(190,150,255,0.25) 2px,
            transparent 3px
        );

    background-size: 80px 80px, 110px 110px;

    animation: moveDots 20s linear infinite;
}

@keyframes moveDots {

    from {
        background-position: 0 0, 30px 30px;
    }

    to {
        background-position: 160px 160px, 200px 200px;
    }

}


/* Başlık */

h1,
h2,
h3 {
    font-family: Georgia, serif;
}


/* Butonlar */

.stButton > button {

    border-radius: 12px;
    border: none;

    padding: 10px 18px;

    font-weight: 600;

    transition: 0.2s;
}

.stButton > button:hover {

    transform: translateY(-2px);

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


/* Yazı yazarken kutunun görünümü */

.stTextInput input:focus,
.stTextArea textarea:focus {

    background-color: #ffffff !important;

    color: #333333 !important;

    border: 1px solid #a77ac7 !important;

    box-shadow: 0 0 0 2px rgba(167, 122, 199, 0.15) !important;

}


/* Placeholder yazısı */

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {

    color: #888888 !important;

    opacity: 1 !important;

}


/* Kart */

.kart {

    background: rgba(255,255,255,0.90);

    border-radius: 20px;

    padding: 20px;

    margin: 15px 0;

    box-shadow:
        0 5px 20px rgba(0,0,0,0.08);

}


/* Avatar */

.avatar {

    font-size: 55px;

    text-align: center;

}


/* Sosyal medya kutuları */

.sosyal-kutu {

    background: rgba(255,255,255,0.75);

    border-radius: 15px;

    padding: 12px;

    margin-top: 8px;

    border: 1px solid rgba(150,120,200,0.15);

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# VERİTABANI
# =========================================================

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

    # Eski veritabanında yeni sütunlar yoksa ekle

    kolonlar = conn.execute(
        "PRAGMA table_info(kullanicilar)"
    ).fetchall()

    kolon_isimleri = [
        kolon["name"]
        for kolon in kolonlar
    ]

    if "instagram_goster" not in kolon_isimleri:

        conn.execute("""
            ALTER TABLE kullanicilar
            ADD COLUMN instagram_goster INTEGER DEFAULT 0
        """)

    if "tiktok_goster" not in kolon_isimleri:

        conn.execute("""
            ALTER TABLE kullanicilar
            ADD COLUMN tiktok_goster INTEGER DEFAULT 0
        """)


    # =====================================================
    # DEĞERLENDİRME TABLOSU
    # =====================================================

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
# DEĞERLENDİRME KONTROLÜ
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
# EŞLEŞME KONTROLÜ
# =========================================================

def eslesme_var_mi(kullanici_adi):

    kullanici = kullanici_getir(
        kullanici_adi
    )

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
# KVKK METNİ
# =========================================================

def kvkk_metni():

    st.markdown("""
### 📜 EKİPLEN KVKK Aydınlatma Metni

**1. Veri Sorumlusu**

EKİPLEN projesi kapsamında kullanıcı bilgilerinin güvenli
şekilde işlenmesine önem veriyoruz.

**2. İşlenen Kişisel Veriler**

Uygulama içerisinde aşağıdaki bilgiler işlenebilir:

- Kullanıcı adı
- Şifre
- Seçilen avatar
- Vibe Testi sonucu
- Kullanıcının isteğe bağlı olarak eklediği Instagram kullanıcı adı
- Kullanıcının isteğe bağlı olarak eklediği TikTok kullanıcı adı
- Sosyal medya bilgilerinin eşleşen kişilere gösterilmesine ilişkin tercih
- EKİPLEN değerlendirme anketine verilen cevaplar

**3. Kişisel Verilerin İşlenme Amaçları**

Bu bilgiler;

- Kullanıcı hesabının oluşturulması,
- Kullanıcının uygulamaya giriş yapabilmesi,
- Profilinin oluşturulması,
- Vibe Testi sonucunun kaydedilmesi,
- Benzer Vibe sonucuna sahip kullanıcıların eşleştirilmesi,
- Kullanıcının kendi isteğiyle eklediği sosyal medya bilgilerinin
  eşleşme sonuçlarında gösterilmesi,
- EKİPLEN deneyiminin değerlendirilmesi ve geliştirilmesi

amaçlarıyla kullanılmaktadır.

**4. Sosyal Medya Bilgileri**

Instagram ve TikTok kullanıcı adlarının eklenmesi isteğe bağlıdır.

Kullanıcı bu bilgileri eklemediği takdirde uygulamayı kullanmaya
devam edebilir.

Kullanıcı sosyal medya hesabını eklese bile,
hesabını eşleştiği kişilere gösterip göstermemeyi ayrıca seçebilir.

**5. Profil Fotoğrafı**

Kullanıcıların özel profil fotoğrafı yüklemesine izin verilmemektedir.

Profil için yalnızca EKİPLEN tarafından sunulan hazır avatarlar
kullanılmaktadır.

**6. Değerlendirme Anketi**

Kullanıcılar bir eşleşme gerçekleştikten sonra EKİPLEN deneyimini
değerlendirmek amacıyla kısa bir değerlendirme anketini doldurur.

Anket içerisinde arkadaşlık kurma durumu, testlerin eğlenceli olup
olmadığı ve kullanıcının geliştirme önerileri ile beğendiği veya
beğenmediği noktalar sorulmaktadır.

**7. Veri Güvenliği**

Kişisel verilerin güvenliğinin sağlanması amacıyla gerekli teknik
ve idari tedbirlerin alınması hedeflenmektedir.

**8. Kullanıcının Hakları**

İlgili kişiler, 6698 sayılı Kişisel Verilerin Korunması Kanunu'nun
11. maddesi kapsamında kanunda belirtilen haklarını kullanabilir.

**9. İletişim**

Kişisel verilerinizle ilgili sorularınız için EKİPLEN proje ekibi
ile iletişime geçebilirsiniz.

> Not: Bu metin teknik proje için örnek bir aydınlatma metnidir.
> Yayına almadan önce proje ekibinizin gerçek bilgileriyle
> güncellenmesi ve gerektiğinde hukuki uzman görüşü alınması gerekir.
""")


# =========================================================
# GİRİŞ EKRANI
# =========================================================

if not st.session_state.giris_yapildi:

    st.title("✨ EKİPLEN")

    st.subheader(
        "Lise Arkadaşlık ve Sosyal Ağ Platformu"
    )

    st.write(
        "Burada kendini tanıyabilir, sana benzeyen insanlarla "
        "eşleşebilir ve yeni arkadaşlıklar keşfedebilirsin. 💜"
    )

    st.divider()


    # -----------------------------------------------------
    # KULLANICI ADI
    # -----------------------------------------------------

    kullanici_adi = st.text_input(
        "👤 Kullanıcı adı",
        placeholder="Kullanıcı adını yaz..."
    )


    # -----------------------------------------------------
    # ŞİFRE
    # -----------------------------------------------------

    col1, col2 = st.columns([5, 1])

    with col1:

        sifre_tipi = (
            "default"
            if st.session_state.sifreyi_goster
            else "password"
        )

        sifre = st.text_input(
            "🔐 Şifre",
            type=sifre_tipi,
            placeholder="Şifreni yaz...",
            key="sifre_input"
        )

    with col2:

        st.write("")

        if st.button(
            "🙈"
            if st.session_state.sifreyi_goster
            else "👁️",
            help="Şifreyi göster/gizle"
        ):

            st.session_state.sifreyi_goster = (
                not st.session_state.sifreyi_goster
            )

            st.rerun()


    st.caption(
        "👁️ Göz butonuyla şifreni gösterebilir veya gizleyebilirsin."
    )


    # -----------------------------------------------------
    # KVKK
    # -----------------------------------------------------

    st.divider()

    with st.expander(
        "📜 KVKK Aydınlatma Metnini Oku"
    ):

        kvkk_metni()


    kvkk_onay = st.checkbox(
        "KVKK Aydınlatma Metnini okudum."
    )


    st.divider()


    # -----------------------------------------------------
    # GİRİŞ
    # -----------------------------------------------------

    giris = st.button(
        "✨ Giriş Yap",
        use_container_width=True
    )


    if giris:

        if not kullanici_adi.strip() or not sifre.strip():

            st.warning(
                "Lütfen kullanıcı adı ve şifreyi doldur. 💜"
            )

        elif not kvkk_onay:

            st.warning(
                "Devam etmek için KVKK Aydınlatma Metnini "
                "okuduğunu onaylamalısın. 📜"
            )

        else:

            kullanici = kullanici_getir(
                kullanici_adi
            )


            # -------------------------------------------------
            # ESKİ KULLANICI
            # -------------------------------------------------

            if kullanici:

                if kullanici["sifre"] == sifre:

                    st.session_state.giris_yapildi = True

                    st.session_state.kullanici_adi = (
                        kullanici_adi
                    )

                    st.session_state.profil_tamamlandi = (
                        bool(
                            kullanici["instagram"] is not None
                            or
                            kullanici["tiktok"] is not None
                        )
                    )

                    st.success(
                        f"Tekrar hoş geldin, "
                        f"{kullanici_adi}! ✨"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Şifre yanlış. Tekrar kontrol eder misin? 🔐"
                    )


            # -------------------------------------------------
            # YENİ KULLANICI
            # -------------------------------------------------

            else:

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

                st.session_state.kullanici_adi = (
                    kullanici_adi
                )

                st.session_state.profil_tamamlandi = False

                st.success(
                    "Hesabın oluşturuldu! "
                    "Şimdi profilini oluşturalım. 🌸"
                )

                st.rerun()


    st.stop()


# =========================================================
# PROFİL OLUŞTURMA
# =========================================================

kullanici_adi = st.session_state.kullanici_adi

kullanici = kullanici_getir(
    kullanici_adi
)


if not kullanici:

    st.error("Kullanıcı bulunamadı.")

    st.stop()


if not st.session_state.profil_tamamlandi:

    st.title("🌸 Profilini Oluştur")

    st.write(
        f"Hoş geldin **{kullanici_adi}**! "
        "Önce kendine bir avatar seçelim."
    )

    st.info(
        "Özel profil fotoğrafı yüklenemez. "
        "Buradaki hazır avatarlardan birini seçebilirsin. 💜"
    )


    avatar = st.radio(
        "✨ Avatarını seç",
        AVATARLAR,
        horizontal=True
    )


    instagram = st.text_input(
        "📸 Instagram kullanıcı adın (isteğe bağlı)",
        placeholder="@kullaniciadi"
    )


    tiktok = st.text_input(
        "🎵 TikTok kullanıcı adın (isteğe bağlı)",
        placeholder="@kullaniciadi"
    )


    st.subheader(
        "🔒 Sosyal Medya Gizliliği"
    )


    instagram_goster = st.checkbox(
        "📸 Instagram hesabımı eşleştiğim kişiye göster",
        value=False
    )


    tiktok_goster = st.checkbox(
        "🎵 TikTok hesabımı eşleştiğim kişiye göster",
        value=False
    )


    st.caption(
        "Bu seçenekleri açmadığın sürece Instagram ve TikTok "
        "kullanıcı adların eşleşme sonuçlarında gösterilmez."
    )


    if st.button(
        "💜 Profilimi Oluştur",
        use_container_width=True
    ):

        conn.execute(
            """
            UPDATE kullanicilar

            SET
                avatar = ?,
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
                int(instagram_goster),
                int(tiktok_goster),
                kullanici_adi
            )
        )

        conn.commit()

        st.session_state.profil_tamamlandi = True

        st.success(
            "Profilin hazır! 🎉"
        )

        st.rerun()


    st.stop()


# =========================================================
# ANA KULLANICI BİLGİSİ
# =========================================================

kullanici = kullanici_getir(
    kullanici_adi
)


# =========================================================
# ZORUNLU DEĞERLENDİRME KONTROLÜ
# =========================================================

# Kullanıcı daha önce bir değerlendirme yapmadıysa
# ve en az bir kişiyle eşleşmişse değerlendirme açılır.

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


    # -----------------------------------------------------
    # SORU 1
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # SORU 2
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # SORU 3
    # -----------------------------------------------------

    st.subheader(
        "3. Neleri geliştirebiliriz?"
    )

    neleri_gelistirebiliriz = st.text_area(
        "Fikrini bizimle paylaş:",
        placeholder="Buraya düşüncelerini yazabilirsin...",
        key="degerlendirme_soru_3"
    )


    # -----------------------------------------------------
    # SORU 4
    # -----------------------------------------------------

    st.subheader(
        "4. Neyi beğendin veya beğenmedin?"
    )

    neyi_begendin_veya_begenmedin = st.text_area(
        "Düşüncelerini yaz:",
        placeholder="Beğendiğin veya beğenmediğin şeyleri yazabilirsin...",
        key="degerlendirme_soru_4"
    )


    st.divider()


    # -----------------------------------------------------
    # DEĞERLENDİRMEYİ GÖNDER
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # DEĞERLENDİRME TAMAMLANMADAN DEVAM EDİLEMEZ
    # -----------------------------------------------------

    st.stop()


# =========================================================
# ÜST BAŞLIK
# =========================================================

st.title("✨ EKİPLEN")

st.write(
    f"Hoş geldin **{kullanici_adi}** "
    f"{kullanici['avatar']}"
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🌸 EKİPLEN")

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
    "🚪 Çıkış Yap"
):

    st.session_state.giris_yapildi = False

    st.session_state.kullanici_adi = None

    st.session_state.profil_tamamlandi = False

    st.rerun()


# =========================================================
# ANA SAYFA
# =========================================================

if sayfa == "🏠 Ana Sayfa":

    st.header("🌷 Hoş geldin!")

    st.write(
        """
        EKİPLEN'de önce kendi Vibe'ını keşfedebilir,
        daha sonra sana benzeyen kişilerle eşleşebilirsin.
        """
    )

    st.info(
        "🧩 Önce Vibe Testi'ni tamamla. "
        "Sonrasında sana uyumlu kişileri "
        "Arkadaş Eşleştirme bölümünde görebilirsin."
    )


# =========================================================
# VIBE TESTİ
# =========================================================

elif sayfa == "🧩 Vibe Testi":

    st.header("🧩 Vibe Testi")

    st.write(
        "Sorulara sana en uygun cevabı ver. "
        "Sonunda hangi Vibe'a sahip olduğunu göreceksin. ✨"
    )


    sorular = [

        "Boş zamanında en çok ne yaparsın?",
        "Arkadaşların seni nasıl tanımlar?",
        "Bir hafta sonunu nasıl geçirirdin?",
        "En sevdiğin ortam hangisi?",
        "Yeni insanlarla tanışmak hakkında ne düşünüyorsun?",
        "Müzik senin için ne ifade ediyor?",
        "Kitap okumayı sever misin?",
        "Bir arkadaşında en çok neye önem verirsin?",
        "Bir sorun olduğunda ne yaparsın?",
        "Kalabalık ortamları sever misin?",
        "Hayalindeki tatil nasıl olurdu?",
        "En çok hangi özelliğine güveniyorsun?",
        "Yeni şeyler denemeyi sever misin?",
        "Arkadaşlık senin için ne demek?",
        "Kendini tek kelimeyle nasıl tanımlarsın?"

    ]


    cevaplar = [

        "Çok severim",
        "Bazen",
        "Pek değil",
        "Hiç sevmem"

    ]


    puan = 0


    for i, soru in enumerate(sorular):

        st.markdown(
            f"### {i + 1}. {soru}"
        )

        cevap = st.radio(
            "Cevabın:",
            cevaplar,
            key=f"soru_{i}"
        )


        if cevap == "Çok severim":

            puan += 4

        elif cevap == "Bazen":

            puan += 3

        elif cevap == "Pek değil":

            puan += 2

        else:

            puan += 1


    if st.button(
        "✨ Vibe'ımı Bul",
        use_container_width=True
    ):

        ortalama = (
            puan / len(sorular)
        )


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
            f"🎉 Senin Vibe'ın: **{vibe}**"
        )

        st.balloons()


# =========================================================
# ARKADAŞ EŞLEŞTİRME
# =========================================================

elif sayfa == "👥 Arkadaş Eşleştirme":

    st.header("👥 Arkadaş Eşleştirme")

    kullanici = kullanici_getir(
        kullanici_adi
    )


    if not kullanici["vibe"]:

        st.warning(
            "Önce Vibe Testi'ni tamamlamalısın. 🧩"
        )


    else:

        st.success(
            f"Senin Vibe'ın: **{kullanici['vibe']}**"
        )


        eslesenler = conn.execute(
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


        if not eslesenler:

            st.info(
                "Şimdilik seninle aynı Vibe'a sahip "
                "başka biri yok. Yeni kişiler katıldıkça "
                "burada görünecekler. 🌷"
            )


        else:

            st.subheader(
                "✨ Sana uyumlu kişiler"
            )


            for kisi in eslesenler:

                st.markdown(
                    f"""
                    <div class="kart">

                        <div class="avatar">
                            {kisi['avatar']}
                        </div>

                        <h3 style="text-align:center;">
                            {kisi['kullanici_adi']}
                        </h3>

                        <p style="text-align:center;">
                            🧩 {kisi['vibe']}
                        </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # -----------------------------------------
                # INSTAGRAM
                # -----------------------------------------

                if (
                    kisi["instagram"]
                    and
                    kisi["instagram_goster"]
                ):

                    instagram_adi = (
                        kisi["instagram"]
                        .strip()
                        .replace("@", "")
                    )

                    instagram_link = (
                        f"https://instagram.com/"
                        f"{instagram_adi}"
                    )

                    st.markdown(
                        f"📸 **Instagram:** "
                        f"[@{instagram_adi}]({instagram_link})"
                    )


                # -----------------------------------------
                # TIKTOK
                # -----------------------------------------

                if (
                    kisi["tiktok"]
                    and
                    kisi["tiktok_goster"]
                ):

                    tiktok_adi = (
                        kisi["tiktok"]
                        .strip()
                        .replace("@", "")
                    )

                    tiktok_link = (
                        f"https://www.tiktok.com/"
                        f"@{tiktok_adi}"
                    )

                    st.markdown(
                        f"🎵 **TikTok:** "
                        f"[@{tiktok_adi}]({tiktok_link})"
                    )


                if (
                    (
                        not kisi["instagram"]
                        or
                        not kisi["instagram_goster"]
                    )
                    and
                    (
                        not kisi["tiktok"]
                        or
                        not kisi["tiktok_goster"]
                    )
                ):

                    st.caption(
                        "Bu kullanıcı sosyal medya hesaplarını "
                        "eşleştiği kişilere göstermeyi seçmemiş."
                    )


                st.divider()


# =========================================================
# PROFİL
# =========================================================

elif sayfa == "👤 Profil":

    st.header("👤 Profilim")

    kullanici = kullanici_getir(
        kullanici_adi
    )


    st.markdown(
        f"""
        <div class="kart">

            <div class="avatar">
                {kullanici['avatar']}
            </div>

            <h2 style="text-align:center;">
                {kullanici['kullanici_adi']}
            </h2>

        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # VIBE
    # -----------------------------------------------------

    if kullanici["vibe"]:

        st.write(
            f"🧩 **Vibe:** {kullanici['vibe']}"
        )

    else:

        st.write(
            "🧩 Vibe testini henüz tamamlamadın."
        )


    st.divider()


    # -----------------------------------------------------
    # SOSYAL MEDYA
    # -----------------------------------------------------

    st.subheader("🔗 Sosyal Medya")


    if kullanici["instagram"]:

        instagram_adi = (
            kullanici["instagram"]
            .strip()
            .replace("@", "")
        )

        instagram_link = (
            f"https://instagram.com/"
            f"{instagram_adi}"
        )

        st.markdown(
            f"📸 **Instagram:** "
            f"[@{instagram_adi}]({instagram_link})"
        )

        if kullanici["instagram_goster"]:

            st.caption(
                "🔓 Eşleştiğin kişiler Instagram hesabını görebilir."
            )

        else:

            st.caption(
                "🔒 Instagram hesabın eşleştiğin kişilere gösterilmiyor."
            )


    if kullanici["tiktok"]:

        tiktok_adi = (
            kullanici["tiktok"]
            .strip()
            .replace("@", "")
        )

        tiktok_link = (
            f"https://www.tiktok.com/"
            f"@{tiktok_adi}"
        )

        st.markdown(
            f"🎵 **TikTok:** "
            f"[@{tiktok_adi}]({tiktok_link})"
        )

        if kullanici["tiktok_goster"]:

            st.caption(
                "🔓 Eşleştiğin kişiler TikTok hesabını görebilir."
            )

        else:

            st.caption(
                "🔒 TikTok hesabın eşleştiğin kişilere gösterilmiyor."
            )


    if (
        not kullanici["instagram"]
        and
        not kullanici["tiktok"]
    ):

        st.caption(
            "Henüz sosyal medya hesabı eklemedin."
        )


    st.divider()


    # -----------------------------------------------------
    # PROFİL DÜZENLE
    # -----------------------------------------------------

    st.subheader(
        "✏️ Profilini düzenle"
    )


    mevcut_avatar = kullanici["avatar"]


    yeni_avatar = st.radio(
        "Avatarını değiştir",

        AVATARLAR,

        index=(
            AVATARLAR.index(mevcut_avatar)
            if mevcut_avatar in AVATARLAR
            else 0
        ),

        horizontal=True
    )


    yeni_instagram = st.text_input(
        "📸 Instagram kullanıcı adın",
        value=kullanici["instagram"] or "",
        placeholder="@kullaniciadi"
    )


    yeni_tiktok = st.text_input(
        "🎵 TikTok kullanıcı adın",
        value=kullanici["tiktok"] or "",
        placeholder="@kullaniciadi"
    )


    st.subheader(
        "🔒 Sosyal Medya Gizliliği"
    )


    yeni_instagram_goster = st.checkbox(
        "📸 Instagram hesabımı eşleştiğim kişiye göster",
        value=bool(kullanici["instagram_goster"])
    )


    yeni_tiktok_goster = st.checkbox(
        "🎵 TikTok hesabımı eşleştiğim kişiye göster",
        value=bool(kullanici["tiktok_goster"])
    )


    st.caption(
        "Bu seçenekleri kapatırsan sosyal medya kullanıcı adların "
        "eşleşme sonuçlarında gösterilmez."
    )


    if st.button(
        "💾 Profili Kaydet",
        use_container_width=True
    ):

        conn.execute(
            """
            UPDATE kullanicilar

            SET
                avatar = ?,
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
                int(yeni_instagram_goster),
                int(yeni_tiktok_goster),
                kullanici_adi
            )
        )

        conn.commit()

        st.success(
            "Profilin güncellendi! 💜"
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

        <h2 style="text-align:center;">
            💜 High Five Ekibi
        </h2>

        <p>
        Merhaba! Biz <b>High Five ekibiyiz.</b> 👋
        </p>

        <p>
        Bu projeyi, <b>15-18 yaş arasındaki, yaşıtlarıyla
        iletişim kurmakta zorlanan kişiler</b> için geliştirdik.
        Amacımız, eğlenceli testlerimizi cevaplayarak kendinize
        uygun kişilerle tanışmanızı ve yeni arkadaşlıklar
        kurmanızı sağlamak.
        </p>

        <p>
        İsterseniz <b>Instagram</b>, isterseniz <b>TikTok</b>
        hesabınızı paylaşarak eşleştiğiniz kişilerle iletişime
        geçebilir ya da sadece testleri çözerek sizler için
        oluşturduğumuz <b>"Vibe Kartları"</b>nı kazanabilirsiniz. ✨
        </p>

        <p>
        Şimdiden iyi eğlenceler! 🌸
        </p>

        <p style="text-align:center;">
        <b>Sevgilerle,<br>
        High Five Ekibi 💜</b>
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# KVKK SAYFASI
# =========================================================

elif sayfa == "📜 KVKK":

    st.title("📜 KVKK Aydınlatma Metni")

    kvkk_metni()
