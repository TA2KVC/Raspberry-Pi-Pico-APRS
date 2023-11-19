import machine
import time
import network
import urequests as requests
try:
  import usocket as socket
except:
  import socket

led = machine.Pin('LED', machine.Pin.OUT) #Pico onBoard Led aktif
led.on()
time.sleep(3)
led.off()

def blink():
    for v in range(15):
        led.on()
        time.sleep(0.04)
        led.off()
        time.sleep(0.04)


# BME280 sensorum olmadigi icin Hava durumu bilgilerini openweather.org sitesinden aldim. Veri APRS kod paketi icin imperial birimde aliniyor,  
def openwe():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get('https://api.openweathermap.org/data/2.5/weather?id={Sehir kodu, ornek:Ankara=323786}&appid={API_SIFRE}&units=imperial', headers=headers)
    data = response.json()
    sick = (data['main']['temp'])
    sicak = ("%03d" % (sick,))
    hum = (data['main']['humidity'])
    nem = ("%03d" % (hum,))
    rzgynu = data['wind']['deg']
    rzgyon = ("%03d" % (rzgynu,))
    rzgsped = data['wind']['speed']
    rzghiz = ("%03d" % (rzgsped,))
    rzggust = data['wind']['gust']
    gust = ("%03d" % (rzggust,))
    pres = (data['main']['pressure'])
    pres1 = int(f"{pres}{'0'*1}")
    basnc = ("%05d" % (pres1,))
    return sicak, nem, rzgyon, rzghiz, gust, basnc

# Raspberry Pico Wifi Baglantisi
ssid = 'xxxxxxx'
password = 'xxxxxxxxxxxxxxxxx'
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(ssid, password)
print("Bağlanıyor...")
while sta_if.isconnected() == False:
    pass
print("Bağlandı!")
blink()
status1 = sta_if.config('ssid')
print( 'Wifi SSID :' + status1 )
status2 = sta_if.ifconfig()
print( 'IP Adresi :' + status2[0] )

a = 0 # ya da while True:
while a <= 9: # ya da while True:
  a += 1 # ya da while True:
  aprsUser = 'XX2XXX' #Amator Telsiz Cagri Isareti // Callsign
  aprsPass = 'xxxxx' #APRS cagri isareti temelli sifre --> http://n5dux.com/ham/aprs-passcode/
  formato = 'utf-8'
  sicak, nem, rzgyon, rzghiz, gust, basnc = openwe()
  callsign = 'XX2XXX'
  btext = ("!4000.30N/03237.02E_") #Konumun LORAN koordinatlari Derece, Dakika, Saniye
  btext += rzgyon
  btext += ("/")
  btext += rzghiz
  btext += ("g"+gust)
  btext += ("t"+sicak)
  btext += "r...p...P..."
  btext += ("b"+basnc)
  btext += ("h"+nem)
  btext += ("L000RPiPicoAPRS TA2KVC Pi Pico APRS")
  sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sck.connect(('85.214.83.187',14580)) #APRS Sunucu IP
  blink()
  sck.send(('user %s pass %s vers RPiPicoAPRS\n' % (aprsUser, aprsPass)).encode(formato))
  sck.send(('%s>APRS:%s\n' % (callsign, btext)).encode(formato))
  print(callsign, btext)
  blink()
  sck.close()
  time.sleep(600)
else:
  reset()
