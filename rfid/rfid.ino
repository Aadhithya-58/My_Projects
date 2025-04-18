#include <WiFi.h>
#include <Firebase_ESP_Client.h>
#include <SPI.h>
#include <MFRC522.h>

// 🔹 Wi-Fi Credentials
#define WIFI_SSID "RAJMALS_5G"
#define WIFI_PASSWORD "Super*12"

// 🔹 Firebase Credentials
#define API_KEY "AIzaSyCgcQ5m5xMxA0mnPEAeFU9dXQXSmt6cZtU"
#define DATABASE_URL "https://cloud-integration-c6dde-default-rtdb.asia-southeast1.firebasedatabase.app/"

// 🔹 RFID Module Pins
#define SS_PIN  5   // SDA pin of RFID
#define RST_PIN 27  // RST pin of RFID

// 🔹 Initialize Firebase & RFID
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;
MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
    Serial.begin(115200);
    SPI.begin();  
    mfrc522.PCD_Init();
    
    // ✅ Connect to Wi-Fi
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        Serial.print(".");
        delay(1000);
    }
    Serial.println("\nConnected to WiFi!");

    // ✅ Configure Firebase
    config.api_key = API_KEY;
    config.database_url = DATABASE_URL;
    Firebase.begin(&config, &auth);
    Firebase.reconnectWiFi(true);
}

void loop() {
    // ✅ Check for RFID Tag
    if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
        return;
    }

    String tagID = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
        tagID += String(mfrc522.uid.uidByte[i], HEX);
    }


    Serial.println("Tag Scanned: " + tagID);
    
    // ✅ Send to Firebase
    String path = "/RFID_Logs/" + tagID;
    if (Firebase.RTDB.setString(&fbdo, path.c_str(), "Detected")) {
        Serial.println("RFID Data sent to Firebase!");
    } else {
        Serial.println("Firebase Error: " + fbdo.errorReason());
    }

    delay(2000);  // Delay before next scan
}
