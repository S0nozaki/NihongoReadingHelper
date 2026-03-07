import flet as ft
import config
import easyocr
from pynput.mouse import Listener
from PIL import ImageGrab
import json
import asyncio

def load_json(filename):
    with open(filename, encoding="utf-8") as f:
        d = json.load(f)
    return d

kanji2element = load_json("kanji2element.json")
kanji2radical = load_json("kanji2radical.json")
element2kanji = load_json("element2kanji.json")
radical2kanji = load_json("radical2kanji.json")

def home_page(page):
    extracted_text = ft.TextField(label='Extracted text', read_only=True, value="Extracting text from selected area", visible=False, width=700)
    kanji_card_grid = ft.GridView(expand=1, runs_count=8, spacing=5, controls=None)

    app_title_field = ft.Container(
        content=ft.Column(
            controls=[ft.Text(value="Nihongo Reading Helper", theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM, weight=ft.FontWeight.BOLD),
                      ft.Text("Stuck on an unknown kanji while reading? Just select an area of the screen and get the kanji present!")],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            tile_mode=ft.GradientTileMode.MIRROR,
            colors=[ft.Colors.PURPLE_600, ft.Colors.DEEP_PURPLE_900],
        ),
        padding=20,
        width=700
    )

    def get_image_text(img_path):
        reader = easyocr.Reader(['ja','en'], gpu=False)
        result = reader.readtext(img_path, detail=0)
        return result
    
    def get_selected_area_text(img_path):
        extracted_text.visible = True
        page.update()
        img_text = ''.join(get_image_text(img_path))
        extracted_text.value = img_text
        get_kanji()
        page.update()

    async def get_area(e):
        def on_click(x, y, button, pressed):
            if button == button.left:
                if pressed:
                    screenshot_initial_point.append(x)
                    screenshot_initial_point.append(y)
                if not pressed:
                    area_final = [x,y]
                    area = ImageGrab.grab(bbox=(screenshot_initial_point[0], screenshot_initial_point[1], area_final[0], area_final[1]))
                    area.save(config.SAVE_TO_PATH, "JPEG")
                    get_selected_area_text(config.SAVE_TO_PATH)
                    page.window.opacity = 1.0
                    page.window.full_screen = False
                    page.update()
                    return False
        page.window.opacity = 0.01
        #for some reason 0.0 opacity not only makes it invisible, but treates it as non-existant
        page.window.full_screen = True
        page.update()
        screenshot_initial_point = []
        await asyncio.sleep(1)
        with Listener(on_click=on_click) as listener:
            listener.join()
        
    button = ft.Button("Select area to extract text", on_click=get_area)

    def get_kanji():
        if extracted_text.value == "":
            return False

        kanji_to_show = extract_all_kanji(extracted_text.value)
        
        kanji_cards = []
        for kanji in kanji_to_show:
            kanji_cards.append(ft.Container(
                content=ft.Text(kanji, theme_style=ft.TextThemeStyle.DISPLAY_SMALL),
                alignment=ft.Alignment.CENTER,
                gradient=ft.LinearGradient(
                    begin=ft.Alignment.TOP_LEFT,
                    end=ft.Alignment.BOTTOM_RIGHT,
                    tile_mode=ft.GradientTileMode.MIRROR,
                    colors=[ft.Colors.PURPLE_600, ft.Colors.DEEP_PURPLE_900],
                ),
                width=150,
                height=150,
                margin=10,
                padding=10,
                border_radius=10,
            ))
        kanji_card_grid.controls = kanji_cards

    return ft.View(
        route = "/",
        controls=[ft.Column(
            controls=[app_title_field, button, extracted_text, kanji_card_grid],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )]
    )

def extract_all_kanji(word):
    kanji_list = []
    for letter in word:
        if letter in kanji2element or letter in radical2kanji:
            kanji_list.append(letter)
    return kanji_list