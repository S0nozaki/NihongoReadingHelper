import flet as ft

def kanji_detail(page, kanji: str):
    return ft.View(
        route="/kanji_detail",
        controls=[ft.Text("New view, kanji observed:" + kanji)]
    )