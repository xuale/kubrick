import cv2
from steg import LSB_steg

input_img = cv2.imread("me.jpg")
steg_obj = LSB_steg(input_img)

steg_obj.encode_text("hi, how are you?")

print(steg_obj.decode_text())