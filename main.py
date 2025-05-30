import easyocr
import config
import flet as ft

def get_image_text():
    reader = easyocr.Reader(['ja','en'])
    result = reader.readtext(config.IMG_PATH, detail = 0)
    return result


def gui(page: ft.Page):
    page.title = "Nihongo Reading Helper"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    tb = ft.TextField(label='Text extracted from image', read_only=True, value=get_image_text())
    page.add(tb)

ft.app(gui)