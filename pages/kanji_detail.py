import flet as ft
import json
import asyncio

def load_json(filename):
    with open(filename, encoding="utf-8") as f:
        d = json.load(f)
    return d

kanjiapi = load_json("kanjiapi_full.json")
radkfile = load_json("radkfile-3.6.2.json")
kradfile = load_json("kradfile-3.6.2.json")

def kanji_detail(page, kanji: str, searched_sentence: str):
    standard_gradient = ft.LinearGradient(
        begin=ft.Alignment.TOP_LEFT,
        end=ft.Alignment.BOTTOM_RIGHT,
        tile_mode=ft.GradientTileMode.MIRROR,
        colors=[ft.Colors.PURPLE_600, ft.Colors.DEEP_PURPLE_900],
    )

    kanji_radicals_selected = []

    go_back_button = ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: asyncio.create_task(page.push_route("/searched_sentence/" + searched_sentence)), align=ft.Alignment.TOP_LEFT)

    kanji_header = ft.Container(
        content=ft.Text(value = kanji, theme_style=ft.TextThemeStyle.DISPLAY_LARGE, align=ft.Alignment.CENTER),
        gradient=standard_gradient,
        padding = 20
    )

    kanji_readings = ft.Container(
        content=ft.Row(
            controls=[
                ft.TextField(kanjiapi["kanjis"][kanji]["kun_readings"], label="Kun readings", read_only=True, multiline=True),
                ft.TextField(kanjiapi["kanjis"][kanji]["on_readings"], label="On readings", read_only=True, multiline=True),
                ft.TextField(kanjiapi["kanjis"][kanji]["name_readings"], label="Name readings", read_only=True, multiline=True),
                ft.TextField(kanjiapi["kanjis"][kanji]["meanings"], label="Meanings", read_only=True, multiline=True),
                ft.TextField(kanjiapi["kanjis"][kanji]["jlpt"], label="JLPT level", read_only=True, multiline=True),
                ft.TextField(kradfile["kanji"][kanji], label="Kanji Parts", read_only=True, multiline=True)
            ],
            wrap=True
        ),
    )

    kanji_parts = ft.Row(
        controls=[],
        wrap=True
    )

    kanji_parts_container = ft.Container(
        content=kanji_parts,
        padding=20
    )

    def generate_kanji_parts():
        kanji_parts_generated = []
        selected_gradient = None
        for radical in radkfile["radicals"].keys():
            if radical in kradfile["kanji"][kanji]:
                selected_gradient = standard_gradient
                kanji_radicals_selected.append(radical)
            else:
                selected_gradient = None
            kanji_parts_generated.append(ft.Container(
                    content=ft.Text(value=radical),
                    padding=10,
                    gradient=selected_gradient
                )
            )
        kanji_parts.controls = kanji_parts_generated
    
    wrong_kanji_button = ft.Button("Was it a different kanji? Adjust the radicals!", on_click=generate_kanji_parts)

    return ft.View(
        route="/kanji_detail",
        controls=[ft.Container(
            content = ft.Column(
            controls=[go_back_button, kanji_header, kanji_readings, wrong_kanji_button, kanji_parts_container],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )]
    )