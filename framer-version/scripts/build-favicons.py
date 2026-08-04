from PIL import Image
SRC='assets/favicon-v5.png'   # circular logo (transparent corners)
im=Image.open(SRC).convert('RGBA')
im.resize((180,180)).save('assets/apple-touch-icon.png')
im.save('favicon.ico', sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
