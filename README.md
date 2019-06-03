# kubrick

a framework for medical stenography.
supports least bit stenography.
supports text, image, and binary file encoding/decoding.

# installation

`pip install -r requirements.txt`

# how to use

at the top of your main python file, import the `lsbrick` class from `kubrick.py`:

`from kubrick import lsbrick`

also, import the `cv2` module:

`import cv2`

the `lsbrick` constructor is structured:

`lsbrick([image read in using the cv2 module], [# representing the encoding length bit size])`

# example usage

text encoding/decoding

```python
#encoding
steg_obj = lsbrick(cv2.imread("bryan_michael.png"), 16)
img_encoded = steg_obj.encode_text("hi how are you?")
cv2.imwrite("new_img.png", img_encoded)

#decoding
im = cv2.imread("new_img.png")
steg_obj2 = lsbrick(im, 16)
print(steg_obj2.decode_text())
```

binary file encoding/decoding

```python
#encoding
steg = lsbrick(cv2.imread("bryan_michael.png"), 16)
data = open("my_data.bin", "rb").read()
new_img = steg.encode_binary(data)
cv2.imwrite("new_image.png", new_img)

#decoding
steg = lsbrick(cv2.imread("new_image.png"), 16)
binary = steg.decode_binary()
with open("recovered.bin", "wb") as f:
    f.write(data)
```

image file encoding/decoding

```python
#encoding
steg = lsbrick(cv2.imread("chico.png"), 16)
new_im = steg.encode_image(cv2.imread("bryan_michael.png"))
cv2.imwrite("new_image.png", new_im)

#decoding
steg = lsbrick(cv2.imread("new_image.png"), 16)
orig_im = steg.decode_image()
cv2.imwrite("recovered.png", orig_im)
```

# to test

write some test shit (see "how to use" and "example usage" section) in `test.py`
and run:

`python test.py`

# notes

- only works with PNG files rn bc JPEG/JPG files fuck with compression of bits
