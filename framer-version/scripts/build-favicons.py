from PIL import Image, ImageDraw
SRC='/tmp/logo_src.png'; S=512
im=Image.open(SRC).convert('RGBA').resize((S,S))
# 1) detect black disc on centre row
d=im.convert('RGB').load()
first=last=-1
for x in range(S):
    r,g,b=d[x,S//2]
    if r+g+b<30:
        if first<0: first=x
        last=x
cx=round((first+last)/2); r=round((last-first)/2)-3   # inset 3px to kill gradient fringe
print(f"disc: centre {cx}, radius {r}")
# 2) keep only the disc, flatten everything else to solid black
mask=Image.new('L',(S,S),0); ImageDraw.Draw(mask).ellipse((cx-r,cx-r,cx+r,cx+r),fill=255)
onBlack=Image.new('RGB',(S,S),(0,0,0))
onBlack.paste(im.convert('RGB'),(0,0),mask)
# 3) scale 1.25x and centre-crop so the bolt fills more of the frame
big=round(S*1.25); off=round((big-S)/2)
master=onBlack.resize((big,big)).crop((off,off,off+S,off+S))
master.save('assets/favicon-v3.png')
master.resize((180,180)).save('assets/apple-touch-icon.png')
master.save('favicon.ico', sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
# 4) verify corners are pure black
m=master.load()
print("corners:", m[0,0], m[S-1,0], m[0,S-1], m[S-1,S-1], "| centre", m[S//2,S//2])
print("done")
