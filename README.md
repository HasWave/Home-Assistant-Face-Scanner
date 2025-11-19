# 🎭 Home Assistant Face Recognition

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.2-blue.svg)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2023.6%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**RTSP kameralar kullanarak yerel yüz tanıma yapan Home Assistant eklentisi**  
**Home Assistant add-on for local face recognition using RTSP cameras**

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https://github.com/HasWave/Home-Assistant-Yuz-Tanima)

</div>

---

## 📋 Özellikler

- 🎥 **RTSP Kamera Desteği** - IP kameralardan canlı video akışı
- 🧠 **Otomatik Yüz Öğrenme** - `/share/yuzler` klasöründen otomatik yüz tanıma
- 📡 **MQTT Entegrasyonu** - Home Assistant ile tam entegrasyon
- 🔒 **Yerel İşleme** - Tüm işlemler yerel ağda, internet gerektirmez
- 👥 **Çoklu Yüz Tanıma** - Aynı anda birden fazla kişiyi tanıyabilir
- ⚡ **Yüksek Performans** - Optimize edilmiş yüz tanıma algoritması
- 🔄 **Otomatik Yeniden Bağlanma** - Kamera bağlantı kopmalarında otomatik yeniden bağlanma

## 🚀 Hızlı Başlangıç

### 1️⃣ Repository Ekleme

Yukarıdaki **"Add add-on repository"** butonuna tıklayarak veya manuel olarak:

1. Home Assistant → **Supervisor** → **Add-on Store**
2. Sağ üstteki **⋮** menüsünden **Repositories** seçin
3. Şu URL'yi ekleyin:
   ```
   https://github.com/HasWave/Home-Assistant-Yuz-Tanima
   ```

### 2️⃣ Eklentiyi Yükleme

1. **HasWave Home Assistant Add-ons** repository'sini bulun
2. **HasWave Yuz Tanima** eklentisini seçin
3. **INSTALL** butonuna tıklayın

**⚠️ Önemli:** İlk kurulum **15-30 dakika** sürebilir. Bu normaldir çünkü `dlib` ve `opencv-python-headless` paketleri kaynak kodundan derlenmektedir. Lütfen sabırla bekleyin, build işlemi arka planda devam edecektir.

### 3️⃣ Yapılandırma

#### Yüz Fotoğraflarını Ekleme

1. Home Assistant → **File editor** veya Samba ile `/share/yuzler/` klasörüne erişin
2. Tanınacak kişilerin fotoğraflarını ekleyin:
   - Dosya adı kişinin adı olacaktır (örn: `ahmet.jpg`, `mehmet.png`)
   - Her fotoğrafta tek bir yüz olmalı
   - Önerilen: 200x200px veya daha büyük, iyi aydınlatılmış fotoğraflar

#### Eklenti Ayarları

```json
{
  "camera_url": "rtsp://kullanici:sifre@192.168.1.100:554/stream",
  "mqtt_host": "core-mosquitto",
  "mqtt_user": "mqtt",
  "mqtt_pass": "password",
  "tolerance": 0.6
}
```

- **camera_url**: RTSP kamera URL'iniz
- **mqtt_host**: MQTT broker adresi (genellikle `core-mosquitto`)
- **mqtt_user**: MQTT kullanıcı adı
- **mqtt_pass**: MQTT şifresi
- **tolerance**: Yüz tanıma hassasiyeti (0.0-1.0, düşük = daha hassas)

### 4️⃣ Başlatma

1. **START** butonuna tıklayın
2. Logları kontrol edin: **LOGS** sekmesi

## 📖 Kullanım

### MQTT Topic'leri

Eklenti şu MQTT topic'lerini kullanır:

#### `face_rec/result`
Tanınan kişiler bu topic'e gönderilir:

```json
{
  "person": "ahmet",
  "all": ["ahmet", "mehmet"],
  "timestamp": 1704067200.123
}
```

#### `face_rec/status`
Eklenti durumu: `online` veya `offline`

### Home Assistant Entegrasyonu

#### MQTT Sensor Oluşturma

`configuration.yaml` dosyanıza ekleyin:

```yaml
mqtt:
  sensor:
    - name: "Yuz Tanima"
      state_topic: "face_rec/result"
      value_template: "{{ value_json.person }}"
      json_attributes_topic: "face_rec/result"
      json_attributes_template: "{{ value_json | tojson }}"
      icon: "mdi:face-recognition"
```

#### Otomasyon Örneği

Belirli bir kişi tanındığında otomatik aksiyon:

```yaml
automation:
  - alias: "Ahmet Geldi"
    trigger:
      platform: mqtt
      topic: "face_rec/result"
    condition:
      condition: template
      value_template: "{{ value_json.person == 'ahmet' }}"
    action:
      - service: notify.mobile_app
        data:
          message: "Ahmet eve geldi!"
      - service: light.turn_on
        entity_id: light.living_room
```

#### Binary Sensor ile Kişi Tespiti

```yaml
mqtt:
  binary_sensor:
    - name: "Ahmet Evde"
      state_topic: "face_rec/result"
      value_template: "{{ 'ahmet' in value_json.all }}"
      device_class: presence
      off_delay: 300  # 5 dakika sonra "off" olur
```

## 🔧 Gelişmiş Kullanım

### Performans Optimizasyonu

- **tolerance** değerini ayarlayarak hassasiyeti değiştirebilirsiniz
- Daha fazla kişi için `/share/yuzler/` klasörüne daha fazla fotoğraf ekleyin
- RTSP stream kalitesini düşürerek performansı artırabilirsiniz

### Sorun Giderme

#### Kamera Bağlanamıyor
- RTSP URL'ini kontrol edin
- Kullanıcı adı ve şifrenin doğru olduğundan emin olun
- Kameranın aynı ağda olduğunu kontrol edin

#### Yüzler Tanınmıyor
- Fotoğrafların kaliteli olduğundan emin olun
- `tolerance` değerini artırmayı deneyin (örn: 0.7)
- Fotoğraflarda tek bir yüz olduğundan emin olun

#### MQTT Mesajları Gelmiyor
- MQTT broker ayarlarını kontrol edin
- Home Assistant → Supervisor → Mosquitto broker'ın çalıştığını kontrol edin
- Logları kontrol edin: `face-recognition` eklentisi → **LOGS**

## 📁 Dosya Yapısı

```
Home-Assistant-Yuz-Tanima/
├── face-recognition/
│   ├── config.json          # Eklenti yapılandırması
│   ├── Dockerfile           # Docker image tanımı
│   ├── main.py              # Ana uygulama kodu
│   ├── requirements.txt     # Python bağımlılıkları
│   └── run.sh               # Başlatma scripti
├── repository.json          # Repository yapılandırması
└── README.md               # Bu dosya
```

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen:

1. Bu repository'yi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Bir Pull Request açın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👨‍💻 Geliştirici

<div align="center">

**HasWave**

🌐 [haswave.com](https://haswave.com) | 📱 [Telegram @HasWAVE](https://t.me/HasWAVE) | 📦 [GitHub](https://github.com/HasWave)

</div>

---

<div align="center">

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!

Made with ❤️ by HasWave

</div>


