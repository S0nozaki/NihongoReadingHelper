import easyocr
import config

reader = easyocr.Reader(['ja','en'])
result = reader.readtext(config.IMG_PATH, detail = 0)
print(result)