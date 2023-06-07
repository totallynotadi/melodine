import os
import appdirs

APP_DIR = os.path.join(appdirs.user_data_dir(), ".melo")

CACHE_PATH = os.path.join(APP_DIR, ".cache")

TEMPFILES_DIR = os.path.join(APP_DIR, ".tempfiles")


# spotify credentials
CLIENT_ID = "22e27810dff0451bb93a71beb5e4b70d"
CLIENT_SECRET = "6254b7703d8540a48b4795d82eae9300"

# api key for pyyoutube (youtube data api usage)
YT_API_KEY = "AIzaSyCq47Zxsu4pN1MMWBNa04380TGDxT7hrQM"

# config options for YoutubeDL
YTDL_CONFIG = {"quiet": True}

# user-specific ytm cookies for ytmusicapi
YTMUSIC_COOKIE = "LOGIN_INFO=AFmmF2swRAIgHSN980c9f8lkxpke8TdftmbblS4jZ7yTp1YTiR4DLvsCICKFB1SIMxehNygfMgnGc1YN6vED-kFyi8MzTWG0SyfM:QUQ3MjNmejk0emRXVURCMmsyLXNxaGN2LUN3N2FfOVkyNHlDR3lDb0poVmhMV0xDMnVRQUdiaHlueWVkSTVNZHFNejY5SWdiVFJ6NTBNbGNuU2o3UXNjazRRMmVDYmlTZ3Zrc1pMZWF0ZE5oV0xzeWpFQXJKWHlHcXRESFIxQnAzX3VMT1FJOElUOHNFSHN5ZXZNaUNBMzk2TXB2U1YtLXNR; YSC=7NZkH35uUdQ; wide=1; VISITOR_INFO1_LIVE=uXbfIjvxy2w; DEVICE_INFO=ChxOekU0TnpZMk5EUTFOemN6TmpBM05qVXlNZz09EL7t/p0GGL7t/p0G; HSID=AtIKsWff0vXxu658I; SSID=Az_QJpTUxtwJEq-b5; APISID=kx9FpcdF6Q4OubJM/AIDl8JK9OSS3xkswa; SAPISID=SzcCYLaksCs1IEyn/Ak1IiNqTn2FptZNfc; __Secure-1PAPISID=SzcCYLaksCs1IEyn/Ak1IiNqTn2FptZNfc; __Secure-3PAPISID=SzcCYLaksCs1IEyn/Ak1IiNqTn2FptZNfc; PREF=tz=Asia.Calcutta&f6=40000000&f7=100&autoplay=true; SID=WwiVhFu2ELWeGjl5uuuER7dyzu3iKTQmUuUjdZahBhVTAkuz-8k6KSusNkZa2ZMcsY6evw.; __Secure-1PSID=WwiVhFu2ELWeGjl5uuuER7dyzu3iKTQmUuUjdZahBhVTAkuzvZzUYTB0JvC8_1pmITLcng.; __Secure-3PSID=WwiVhFu2ELWeGjl5uuuER7dyzu3iKTQmUuUjdZahBhVTAkuz1ob32iPCzOk3hJ3hD-Cpfw.; ST-mhbc14=; ST-1eyjsm5=; ST-jomz6n=; SIDCC=AP8dLty1RMWDYSVx5-WuYxRuP-OHv3w8n29ExJMcTh3K6v_EEvawezau05ClM7x1D_ktjSzvlt0; __Secure-1PSIDCC=AP8dLtx8pvT_bO5UJU9It7D8MN1W0AjiHYIFTyDAniUmcpsb8TL0LidapY93dkpeesZTugg74g; __Secure-3PSIDCC=AP8dLtxM1TI9kC8DAFdpckkPv-yUAgPn1I7Kb_wsiA-lgxbIwqVoeg3Vj0eNqk6Uq1NAGvvhqKg"
