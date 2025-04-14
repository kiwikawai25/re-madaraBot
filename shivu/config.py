class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "8156600797"
    sudo_users = "6675050163", "8156600797"
    GROUP_ID = -1002343417591
    TOKEN = "7683327822:AAG5cWtPN4zjdY5_BzMwNXDoq69CxDaubcw"
    mongo_url = "mongodb+srv://GBAN:GBANKACHODA@cluster0gban.ejxkvzo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0gban"
    PHOTO_URL = ["https://graph.org/file/90344336f0da2961141a8-9129c1a27bb0bf675f.jpg", "https://graph.org/file/3b8e66af1a005897f1ada-e290ec29df788f01cf.jpg"]
    SUPPORT_CHAT = "https://t.me/Anime_Circle_Club"
    UPDATE_CHAT = "https://t.me/+vDcCB_w1fxw1YTll"
    BOT_USERNAME = "Madara_X_Waifu_ProxyBot"
    CHARA_CHANNEL_ID = "-1002646820042"
    api_id = 28159105
    api_hash = "a0936ddf210a7e091e19947c7dc70c91"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
