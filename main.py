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
        extracted_text = ft.TextField(label='Extracted text', read_only=True, value="Extracting text from selected area")
        page.add(extracted_text)
        img_text = get_image_text(img_path)
        if len(img_text) < 2:
            extracted_text.value = img_text[0]
        else:
            page.remove(extracted_text)
            for word_group in img_text:
                group_text = ft.TextField(label='Extracted text', read_only=True, value=word_group)
                page.add(group_text)
        page.update()
        
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
    button = ft.Button("Select area to extract text", on_click=get_area)
    page.add(button)

ft.app(gui)