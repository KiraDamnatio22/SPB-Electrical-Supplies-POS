from pathlib import Path
import customtkinter as ctk
from PIL import Image


BASE_DIR = Path(__file__).resolve().parent
LABEL_DIR = BASE_DIR / "barcodes"
DB_DIR = BASE_DIR / "inventory.db"


# Icons
ICONS_DIR = BASE_DIR / "assets" / "icons"

ACCOUNT = ICONS_DIR / "account.png"
BACK_ARROW = ICONS_DIR / "back_arrow.png"
BACK_IOS = ICONS_DIR / "back_ios.png"
CHECK = ICONS_DIR / "check.png"
CHECK_CIRCLE = ICONS_DIR / "check_circle.png"
CLOSE = ICONS_DIR / "close.png"
DELETE = ICONS_DIR / "delete.png"
DOWNLOAD = ICONS_DIR / "download.png"
GO_IOS = ICONS_DIR / "go_ios.png"
HOME = ICONS_DIR / "home.png"
MENU = ICONS_DIR / "menu.png"
MORE_VERT = ICONS_DIR / "more_vert.png"
SAVE = ICONS_DIR / "save.png"
SEARCH = ICONS_DIR / "search.png"
SETTINGS = ICONS_DIR / "settings.png"
PRODUCT = ICONS_DIR / "product.png"

class IconPath():
    def __init__(self):
        self.title = "Where you find all icons."

        self.icons = {
            "account": ctk.CTkImage(light_image=Image.open(ACCOUNT), size=(38, 38)),
            "back_arrow": ctk.CTkImage(light_image=Image.open(BACK_ARROW), size=(20, 20)),
            "back_ios": ctk.CTkImage(light_image=Image.open(BACK_IOS), size=(35, 35)),
            "check": ctk.CTkImage(light_image=Image.open(CHECK), size=(20, 20)),
            "check_circle": ctk.CTkImage(light_image=Image.open(CHECK_CIRCLE), size=(20, 20)),
            "close": ctk.CTkImage(light_image=Image.open(CLOSE), size=(20, 20)),
            "delete": ctk.CTkImage(light_image=Image.open(DELETE), size=(20, 20)),
            "download": ctk.CTkImage(light_image=Image.open(DOWNLOAD), size=(20, 20)),
            "go_ios": ctk.CTkImage(light_image=Image.open(GO_IOS), size=(20, 20)),
            "home": ctk.CTkImage(light_image=Image.open(HOME), size=(20, 20)),
            "menu": ctk.CTkImage(light_image=Image.open(MENU), size=(35, 35)),
            "more_vert": ctk.CTkImage(light_image=Image.open(MORE_VERT), size=(35, 35)),
            "save": ctk.CTkImage(light_image=Image.open(SAVE), size=(20, 20)),
            "search": ctk.CTkImage(light_image=Image.open(SEARCH), size=(32, 32)),
            "settings": ctk.CTkImage(light_image=Image.open(SETTINGS), size=(20, 20)),
            "product": ctk.CTkImage(light_image=Image.open(PRODUCT), size=(60, 60)),
        }
    
    def get_icons(self):
        return self.icons
    
    def __repr__(self):
        return self.title
