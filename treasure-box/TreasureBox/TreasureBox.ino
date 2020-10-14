// for LCD display
#include <LiquidCrystal.h>
// for RFID reader
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_PN532.h>

// define pins for RFID shield
#define PN532_SCK  (4)
#define PN532_MOSI (7)
#define PN532_SS   (6)
#define PN532_MISO (5)
#define PN532_IRQ   (2)
#define PN532_RESET (3) 

// define pins and initialize lcd
LiquidCrystal lcd(13,12,11,10,9,8);
// initialize shield
Adafruit_PN532 nfc(PN532_IRQ, PN532_RESET);

// initialize total points
int total_points = 0;


void setup()
{
  Serial.begin(9600);
  while (!Serial) delay(10);
  // initialize nfc
  nfc.begin();
  uint32_t versiondata = nfc.getFirmwareVersion();
  if (! versiondata) {
    while (1); // halt
  }  
  // configure board to read RFID tags
  nfc.SAMConfig();
  // initialize lcd
  lcd.begin(16, 2);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Current points:");
  lcd.setCursor(0,1);
  lcd.print(total_points);
}

void loop() {
  //
  uint8_t success;
  uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };  // Buffer to store the returned UID
  uint8_t uidLength;
  //
  success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength);
  //
  if (success) {    
    if (uidLength == 4) {    
      // Now we need to try to authenticate it for read/write access
      uint8_t keya[6] = { 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF };
      // Start with block 4 (the first block of sector 1) since sector 0
      success = nfc.mifareclassic_AuthenticateBlock(uid, uidLength, 4, 0, keya);
      //
      if (success) {
        uint8_t data[16]; 
        // write to block 4
        // memcpy(data, (const uint8_t[]){ '1', ' ', 'p', 'o', 'i', 'n', 't', 0, 0, 0, 0, 0, 0, 0, 0, 0 }, sizeof data);
        // success = nfc.mifareclassic_WriteDataBlock (4, data);
        // Try to read the contents of block 4
        success = nfc.mifareclassic_ReadDataBlock(4, data);
        //
        char *clearcard = "clear points";
        char *point5 = "5 points";
        char *point3 = "3 points";
        char *point2 = "2 points";
        char *point1 = "1 point";
        // 
        if (success) {
          // Data seems to have been read ... spit it out
          if (strcmp(data, clearcard) == 0) {
            // Serial.println("redeem points");
            if (total_points < 50) {
                lcd.clear();
                lcd.setCursor(0,0);
                lcd.print("Not enough pts");
                lcd.setCursor(0,1);
                lcd.print("to redeem!");
                delay(2500);
                lcd.clear();
                lcd.print("Current points:");
                lcd.setCursor(0,1);
                lcd.print(total_points);
            } else {
              total_points = total_points - 50;
            }
          }
          if (strcmp(data, point5) == 0) {
            // Serial.println("5 points earned");
            total_points = total_points + 5;
          }
          if (strcmp(data, point3) == 0) {
            // Serial.println("3 points earned");
            total_points = total_points + 3;
          }
          if (strcmp(data, point2) == 0) {
            // Serial.println("2 points earned");
            total_points = total_points + 2;
          }
          if (strcmp(data, point1) == 0) {
            // Serial.println("1 point earned");
            total_points = total_points + 1;
          }             
          // Wait a bit before reading the card again
        }
      }
    }   
  }  
  // write to lcd
  lcd.setCursor(0,1);
  lcd.print(total_points);
  Serial.println(total_points);
  //
  delay(1000);

}
