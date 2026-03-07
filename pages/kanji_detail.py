import flet as ft
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

def kanji_detail(page, kanji: str):
    standard_gradient = ft.LinearGradient(
        begin=ft.Alignment.TOP_LEFT,
        end=ft.Alignment.BOTTOM_RIGHT,
        tile_mode=ft.GradientTileMode.MIRROR,
        colors=[ft.Colors.PURPLE_600, ft.Colors.DEEP_PURPLE_900],
    )

    go_back_button = ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: asyncio.create_task(page.push_route("/")), align=ft.Alignment.TOP_LEFT)

    kanji_header = ft.Container(
        content=ft.Text(value = kanji, theme_style=ft.TextThemeStyle.DISPLAY_LARGE, align=ft.Alignment.CENTER),
        gradient=standard_gradient,
        padding = 20
    )

    kanji_readings = ft.Container(
        content=ft.Row(
            controls=[
                ft.TextField("Kun yomi"),
                ft.TextField("On yomi")
            ]
        ),
    )

    kanji_parts = ft.Row(
        controls=[]
    )

    kanji_parts_container = ft.Container(
        content=kanji_parts,
        padding=20
    )

    def generate_kanji_parts():
        kanji_parts_generated = []
        for part in kanji2element[kanji]:
            kanji_parts_generated.append(ft.Container(
                    content=ft.Text(value=part),
                    gradient=standard_gradient,
                    padding=10
                )
            )
        kanji_parts.controls = kanji_parts_generated
    
    wrong_kanji_button = ft.Button("Was it a different kanji?", on_click=generate_kanji_parts)

    return ft.View(
        route="/kanji_detail",
        controls=[ft.Container(
            content = ft.Column(
            controls=[go_back_button, kanji_header, kanji_readings, wrong_kanji_button, kanji_parts_container],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )]
    )