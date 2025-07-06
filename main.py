import easyocr
import config
import flet as ft
from pynput.mouse import Listener
from PIL import ImageGrab
import json

def load_json(filename):
    with open(filename, encoding="utf-8") as f:
        d = json.load(f)
    return d

kanji2element = load_json("kanji2element.json")
kanji2radical = load_json("kanji2radical.json")
element2kanji = load_json("element2kanji.json")
radical2kanji = load_json("radical2kanji.json")

def get_image_text(img_path):
    reader = easyocr.Reader(['ja','en'], gpu=False)
    result = reader.readtext(img_path, detail=0)
    return result

def gui(page: ft.Page):
    page.title = "Nihongo Reading Helper"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    def get_selected_area_text(img_path):
        extracted_text = ft.TextField(label='Extracted text', read_only=True, value="Extracting text from selected area")
        page.add(extracted_text)
        page.update()
        img_text = ''.join(get_image_text(img_path))
        extracted_text.value = img_text
        get_kanji()
        page.update()

    def get_area(e):
        page.window.opacity = 0.01
        #for some reason 0.0 opacity not only makes it invisible, but treates it as non-existant
        page.window.full_screen = True
        page.update()
        area_start = [0,0]
        area_final = [0,0]
        def on_click(x, y, button, pressed):
            if button == button.left:
                if pressed:
                    area_start[0] = x
                    area_start[1] = y
                else:
                    area_final[0] = x
                    area_final[1] = y
            if not pressed:
                listener.stop()
                page.window.full_screen = False
                page.window.opacity = 1.0
                page.update()
                area = ImageGrab.grab(bbox=(area_start[0], area_start[1], area_final[0], area_final[1]))
                area.save(config.SAVE_TO_PATH, "JPEG")
                get_selected_area_text(config.SAVE_TO_PATH)
                return True
        with Listener(on_click=on_click) as listener:
            listener.join()
    button = ft.Button("Select area to extract text", on_click=get_area)

    def get_kanji(e=False):
        text_field_to_inspect = ""
        text_fields = [field for field in page.controls if ('TextField' in str(type(field)))]
        for field in text_fields:
            text_field_to_inspect += field.value
        
        if text_field_to_inspect == "":
            return False

        kanji_to_show = extract_all_kanji(text_field_to_inspect)
        
        kanji_cards = []
        for kanji in kanji_to_show:
            kanji_cards.append(ft.Container(
                content=ft.Text(kanji),
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.AMBER,
                width=150,
                height=150,
                margin=10,
                padding=10,
                border_radius=10,
            ))
        
        page.add(ft.GridView(expand=1, runs_count=8, spacing=5, controls=kanji_cards))
        page.update()

    kanji_button = ft.Button("Extract kanji from selected text", on_click=get_kanji)
    page.add(button, kanji_button)


def extract_all_kanji(word):
    kanji_list = []
    for letter in word:
        if letter in kanji2element or letter in radical2kanji:
            kanji_list.append(letter)
    return kanji_list

ft.app(gui)