from PIL import Image
SRC='assets/favicon-v4.png'   # approved gradient square, RGB, corners reach edges
im=Image.open(SRC).convert('RGB')
im.resize((180,180)).save('assets/apple-touch-icon.png')
im.save('favicon.ico', sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
