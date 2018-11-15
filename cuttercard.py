from PIL import Image

mainimg = Image.open("UNO.png")

card = Image.new("RGB",(240,360))

imgx = 1 + 240*13
imgy = 1
for xcard in range(0,240):
	for ycard in range(0,360):
		pixcolor = mainimg.getpixel((imgx+xcard,imgy+ycard))
		card.putpixel((xcard,ycard),pixcolor)
card.save("13 4.png","PNG")

imgx = 1 + 240*13
imgy = 1 + 360*4
for xcard in range(0,240):
	for ycard in range(0,360):
		pixcolor = mainimg.getpixel((imgx+xcard,imgy+ycard))
		card.putpixel((xcard,ycard),pixcolor)
card.save("14 4.png","PNG")

for x in range(13):
	imgx = 1 + 240*x
	for y in range(4):
		imgy = 1 + 360*y
		for xcard in range(0,240):
			for ycard in range(0,360):
				pixcolor = mainimg.getpixel((imgx+xcard,imgy+ycard))
				card.putpixel((xcard,ycard),pixcolor)
		card.save(str(x) + " " + str(y) + ".png","PNG")

def Halfsize(Img):
	img = Image.open(Img)
	width, height = img.size
	img.resize((width//2, height//2)).save(Img)

def Imagescalar():
	for y in range(13):
		for x in range(4):
			Halfsize((str(y) + " " +str(x) +".png"))
	Halfsize("13 4.png")
	Halfsize("14 4.png")

Imagescalar()
