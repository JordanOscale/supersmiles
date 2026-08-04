from PIL import Image
SRC='assets/favicon-v4.png'
im=Image.open(SRC).convert('RGBA')
im.resize((180,180)).save('assets/apple-touch-icon.png')
im.save('favicon.ico', sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
# confirm corners are the gradient, NOT #000000
px=im.load(); w,h=im.size
print('favicon-v4 corners:', px[0,0], px[w-1,0], px[0,h-1], px[w-1,h-1], '| centre', px[w//2,h//2])
print('done')
