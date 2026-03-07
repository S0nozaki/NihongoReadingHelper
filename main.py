import flet as ft
from pages.home import home_page
from pages.kanji_detail import kanji_detail

async def main(page: ft.Page):
    page.title = "Nihongo Reading Helper"
    page.theme_mode = ft.ThemeMode.DARK
    #initial route outside route_change function since after the update you can't trigger a route_change going to the same route as the origin
    page.views.append(home_page(page))
    page.update()

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()
        if page.route == "/":
            page.views.append(home_page(page))
        elif page.route.startswith("/kanji_detail/"):
            page.views.append(kanji_detail(page, page.route.split("/")[2]))
        page.update()

    page.on_route_change = route_change

ft.run(main)