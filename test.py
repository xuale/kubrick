import cv2
from steg import LSB_steg

""" 
# TEXT ENCODING/DECODING TESTING
#encoding
steg_obj = LSB_steg(cv2.imread("bryan_michael.png"))
img_encoded = steg_obj.encode_text("hi how are you?")
cv2.imwrite("new_img.png", img_encoded)

#decoding
im = cv2.imread("new_img.png")
steg_obj2 = LSB_steg(im)
print(steg_obj2.decode_text())
"""

"""
# BINARY FILE ENCODING/DECODING TESTING
#encoding
steg = LSB_steg(cv2.imread("bryan_michael.png"))
data = open("my_data.bin", "rb").read()
new_img = steg.encode_binary(data)
cv2.imwrite("new_image.png", new_img)

#decoding
steg = LSB_steg(cv2.imread("new_image.png"))
binary = steg.decode_binary()
with open("recovered.bin", "wb") as f:
    f.write(data)
"""

# IMAGE FILE ENCODING/DECODING TESTING
#encoding
steg = LSB_steg(cv2.imread("chico.png"))
new_im = steg.encode_image(cv2.imread("bryan_michael.png"))
cv2.imwrite("new_image.png", new_im)

#decoding
steg = LSB_steg(cv2.imread("new_image.png"))
orig_im = steg.decode_image()
cv2.imwrite("recovered.png", orig_im)