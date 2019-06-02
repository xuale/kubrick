import cv2
from steg import LSB_steg

#encoding
steg_obj = LSB_steg(cv2.imread("bryan_michael.png"))
img_encoded = steg_obj.encode_text("hi how are you?")
cv2.imwrite("new_img.png", img_encoded)

#decoding
im = cv2.imread("new_img.png")
steg_obj2 = LSB_steg(im)
print(steg_obj2.decode_text())