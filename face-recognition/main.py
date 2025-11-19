import face_recognition
import cv2
import numpy as np
import paho.mqtt.client as mqtt
import os
import json
import time

# Ayarlari Yukle
try:
    with open('/data/options.json', 'r') as f:
        config = json.load(f)
except:
    config = {}
    print("Config dosyasi bulunamadi, varsayilanlar kullanilacak.")

RTSP_URL = config.get('camera_url', '0')
MQTT_BROKER = config.get('mqtt_host', 'core-mosquitto')
MQTT_USER = config.get('mqtt_user', '')
MQTT_PASS = config.get('mqtt_pass', '')
TOLERANCE = float(config.get('tolerance', 0.6))

FACES_DIR = "/share/yuzler"

# MQTT Baglantisi
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("MQTT baglandi.")
        client.publish("face_rec/status", "online", qos=1, retain=True)
    else:
        print(f"MQTT baglanti hatasi: {rc}")

def on_disconnect(client, userdata, rc):
    print("MQTT baglantisi kesildi.")

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect

if MQTT_USER and MQTT_PASS:
    client.username_pw_set(MQTT_USER, MQTT_PASS)

try:
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_start()
    print("MQTT baglanti kuruluyor...")
    time.sleep(2)  # Baglanti icin bekle
except Exception as e:
    print(f"MQTT Baglanti Hatasi: {e}")
    print("MQTT olmadan devam ediliyor...")

# Yuzleri Ogrenme
known_face_encodings = []
known_face_names = []

if not os.path.exists(FACES_DIR):
    try:
        os.makedirs(FACES_DIR)
        print(f"{FACES_DIR} olusturuldu.")
    except:
        pass

print("Yuzler taraniyor...")
if os.path.exists(FACES_DIR):
    for filename in os.listdir(FACES_DIR):
        if filename.lower().endswith((".jpg", ".png", ".jpeg")):
            path = os.path.join(FACES_DIR, filename)
            try:
                image = face_recognition.load_image_file(path)
                encodings = face_recognition.face_encodings(image)
                if len(encodings) > 0:
                    known_face_encodings.append(encodings[0])
                    name = os.path.splitext(filename)[0]
                    known_face_names.append(name)
                    print(f"Ogrenildi: {name}")
            except Exception as e:
                print(f"Hata ({filename}): {e}")

print(f"Toplam {len(known_face_names)} kisi hafizada.")

# Kamera Dongusu
print(f"RTSP kamera baglaniliyor: {RTSP_URL}")
video_capture = cv2.VideoCapture(RTSP_URL)

# Kamera ayarlari (RTSP icin)
video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not video_capture.isOpened():
    print(f"HATA: Kamera acilamadi: {RTSP_URL}")
    print("Lutfen RTSP URL'ini kontrol edin.")
    exit(1)

print("Kamera baglandi, yuz tanima basladi...")
last_detection_time = 0
DETECTION_COOLDOWN = 3 

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Kamera akisi koptu, yeniden baglaniyor...")
        video_capture.release()
        time.sleep(5)
        video_capture = cv2.VideoCapture(RTSP_URL)
        video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        continue

    # Resim kucultme (Performans)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    found_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=TOLERANCE)
        name = "Bilinmiyor"
        
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
        
        found_names.append(name)

    if found_names and (time.time() - last_detection_time > DETECTION_COOLDOWN):
        primary = found_names[0]
        payload = json.dumps({"person": primary, "all": found_names, "timestamp": time.time()})
        try:
            if client.is_connected():
                client.publish("face_rec/result", payload, qos=1)
                print(f"MQTT gonderildi: {primary} (Toplam: {len(found_names)} kisi)")
            else:
                print(f"Yuz bulundu ama MQTT bagli degil: {primary}")
        except Exception as e:
            print(f"MQTT gonderim hatasi: {e}")
        last_detection_time = time.time()
