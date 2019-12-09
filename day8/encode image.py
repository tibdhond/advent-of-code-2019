from PIL import Image
image_file = Image.open("capture.png")    # open colour image
image_file = image_file.convert('1')    # convert image to black and white
width, height = image_file.size
data = [0 if x == 0 else 1 for x in list(image_file.getdata())]
with open("input2.txt", "w+") as f:
    f.write("%dx%d\n" % (width, height))
    f.write(str(data[0]))
    for x in data[1:]:
        f.write(str(x))

