import base64

image = open('/Users/rahil.r/Desktop/localimage.pdf', 'rb')
image_read = image.read()
image_64_encode = base64.encodestring(image_read)
print(image_64_encode)
