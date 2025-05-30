import easyocr
import config
import flet as ft
from pynput.mouse import Listener
from PIL import ImageGrab

def get_image_text(img_path):
    reader = easyocr.Reader(['ja','en'], gpu=False)
    result = reader.readtext(img_path, detail=0)
    return result

def gui(page: ft.Page):
    page.title = "Nihongo Reading Helper"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    def get_selected_area_text(img_path):
        tb = ft.TextField(label='Area', read_only=True, value="Extracting text from selected area")
        page.add(tb)
        tb.value = get_image_text(img_path)
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
                    print("Initial coordinates: ", (x,y))
                else:
                    area_final[0] = x
                    area_final[1] = y
                    print("Final coordinates: ", (x,y))
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
    button = ft.Button("Select area to screenshot", on_click=get_area)
    page.add(button)

ft.app(gui)