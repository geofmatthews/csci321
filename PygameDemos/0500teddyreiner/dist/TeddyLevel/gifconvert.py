import Image
folder = 'C:\\cygwin\\home\\matthews\\Teaching\\csci321\\GeofDemos\\Game001ShootTeddy\\data\\'

giffile = folder + "explode2.gif"

im = Image.open(giffile)
width,height = im.size

# Is there a better way to find the number of frames?
nframes = 0
while 1:
    nframes = nframes + 1
    try:
        im.seek(nframes)
    except:
        break

frame = 0
newwidth, newheight = nframes*width, height

newimage = Image.new("RGB",(newwidth,newheight))
for frame in range(nframes):
    im.seek(frame)
    newimage.paste(im, (frame*width, 0))

stripfile = folder + "explodestrip.png"
newimage.save(stripfile, format="png")

    
