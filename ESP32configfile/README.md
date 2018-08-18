# ESP32の書き込めるファイルサイズを変更する

注意が必要なのでメモ

変更するべきファイルは

```
~/Arduino/hardware/espressif/esp32/tools/partitions/default.csv
~/Arduino/hardware/espressif/esp32/boards.txt
```

の2つ。(編集にメモ帳などは使用しないこと、文字コードのせいで死ぬ可能性が高い(1敗))

デフォルトの設定は

```
# Name, Type, SubType, Offset, Size, Flags
nvs,    data, nvs,     0x9000, 0x5000,
otadata,data, ota,     0xe000, 0x2000,
app0,   app, ota_0,    0x10000,0x140000,
app1,   app, ota_1,    0x150000,0x140000,
eeprom, data, 0x99,    0x2D0000,0x1000,
spiffs, data, spiffs,  0x2D1000,0x12F000
```

になる。


