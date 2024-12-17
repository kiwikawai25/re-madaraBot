class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "6138142369"
    sudo_users = "6018803920"
    GROUP_ID = -1002392274240
    TOKEN = "7045334311:AAG4H2ErRsWPQoHiIN6YEQSdKHiFM53zFew"
    mongo_url = "mongodb+srv://manasmishra6000:manas@#123@cluster0.ocpf5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    PHOTO_URL = ["https://telegra.ph/file/b925c3985f0f325e62e17.jpg", "https://telegra.ph/file/4211fb191383d895dab9d.jpg"]
    SUPPORT_CHAT = "https://t.me/+q6eGZdsqxCpiMGY1"
    UPDATE_CHAT = "https://t.me/+q6eGZdsqxCpiMGY1"
    BOT_USERNAME = "Snatch_Your_Character_Bot"
    CHARA_CHANNEL_ID = "-1002133191051"
    api_id = "29348525"
    api_hash = "d815eb5b92d9ba6e35c45fa4a85db492"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
