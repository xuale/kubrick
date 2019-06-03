#!/usr/bin/env python
# coding: UTF-8

import numpy as np

def print_error(msg):
    print(msg)
    exit(1)

class LSB_steg():

    def __init__(self, in_img, bit_size):
        self.image = in_img
        self.encode_bit_size = bit_size
        self.height, self.width, self.nbchannels = in_img.shape
        self.cur_width = 0
        self.cur_height = 0
        self.cur_channel = 0
        self.mask_one_vals = [128,64,32,16,8,4,2,1]
        self.mask_one = self.mask_one_vals.pop()
        self.mask_zero_vals = [127, 191, 223, 239, 247, 251, 253, 254]
        self.mask_zero = self.mask_zero_vals.pop()

    # function to embed bits within the image
    def put_bin_val(self, bits):
        for bit in bits:
            pixel_val = list(self.image[self.cur_height,self.cur_width])
            pixel_val[self.cur_channel] = (int(pixel_val[self.cur_channel]) | self.mask_one) if int(bit) == 1 else (int(pixel_val[self.cur_channel]) & self.mask_zero)
            self.image[self.cur_height,self.cur_width] = tuple(pixel_val)
            self.next_slot()
    
    # move encoding/decoding position to next available slot
    def next_slot(self):
        if self.cur_channel != self.nbchannels-1:
            self.cur_channel += 1
        else:
            self.cur_channel = 0
            if self.cur_width != self.width-1:
                self.cur_width += 1
            else:
                self.cur_width = 0
                if self.cur_height != self.height-1:
                    self.cur_height += 1
                else:
                    self.cur_height = 0
                    if self.mask_one == 128:
                        print_error("Image is completely filled. No spots remaining.")
                    else:
                        self.mask_one = self.mask_one_vals.pop()
                        self.mask_zero = self.mask_zero_vals.pop()
    
    # decode a bit from the image
    def decode_bit(self):
        img_val = self.image[self.cur_height,self.cur_width][self.cur_channel]
        decoded_val = int(img_val) & self.mask_one
        self.next_slot()
        res = "1" if decoded_val > 0 else "0"
        return res
    
    # turn an integer into its binary value representation (as a string)
    def binary_value(self, val, bitsize):
        res_string = "{0:{fill}" + str(bitsize) + "b}"
        res = res_string.format(val, fill="0")
        return res

    # encode text
    def encode_text(self, text):
        # encode the length of text (so we can know how much to retrieve when we decode later)
        bin_length = self.binary_value(len(text), self.encode_bit_size)
        self.put_bin_val(bin_length)
        # encode the actual text
        for c in text:
            self.put_bin_val(self.binary_value(ord(c), 8))
        return self.image

    # decode text
    def decode_text(self):
        text_size = ""
        # check order of bits
        for i in range(self.encode_bit_size):
            text_size += self.decode_bit()
        res = ""
        for i in range(int(text_size, 2)):
            temp = ""
            for i in range(8):
                temp += self.decode_bit()
            res += chr(int(temp, 2))
        return res

    # encode binary file
    def encode_binary(self, data):
        carrier_img_size = self.width * self.height * self.nbchannels
        if carrier_img_size < len(data)+64:
            print_error("Our carrier image is not big enough to encrypt this file!")
        length_bin_val = self.binary_value(len(data), 64)
        # encode the length of the file
        self.put_bin_val(length_bin_val)
        # encode the actual data of the file
        for b in data:
            if not isinstance(b, int):
                b = ord(b)
            byte_val = self.binary_value(b, 8)
            self.put_bin_val(byte_val)
        return self.image

    # decode binary file
    def decode_binary(self):
        length_file = ""
        for i in range(64):
            length_file += self.decode_bit()
        res = b""
        for i in range(int(length_file, 2)):
            tmp = ""
            for i in range(8):
                tmp += self.decode_bit()
            res += chr(int(tmp, 2)).encode("utf-8")
        return res

    # encode image
    def encode_image(self, in_img):
        carrier_img_size = self.width * self.height * self.nbchannels
        if carrier_img_size < (in_img.shape[1]*in_img.shape[0]*in_img.shape[2]):
            print_error("Our carrier image is not big enough to encrypt this file!")
        binary_width = self.binary_value(in_img.shape[1], self.encode_bit_size)
        binary_height = self.binary_value(in_img.shape[0], self.encode_bit_size)
        # put sizes into image
        self.put_bin_val(binary_width)
        self.put_bin_val(binary_height)
        # put actual data into image
        for h in range(in_img.shape[0]):
            for w in range(in_img.shape[1]):
                for c in range(in_img.shape[2]):
                    bin_val = self.binary_value(int(in_img[h,w][c]), 8)
                    self.put_bin_val(bin_val)
        return self.image

    # decode image
    def decode_image(self):
        binary_width = ""
        for i in range(self.encode_bit_size):
            binary_width += self.decode_bit()
        width = int(binary_width, 2)
        binary_height = ""
        for i in range(self.encode_bit_size):
            binary_height += self.decode_bit()
        height = int(binary_height, 2)
        new_img = np.zeros((width, height, 3), np.uint8)
        for h in range(height):
            for w in range(width):
                for c in range(new_img.shape[2]):
                    temp = ""
                    for i in range(8):
                        temp += self.decode_bit()
                    new_val = int(temp, 2)
                    list_cur_vals = list(new_img[w, h])
                    list_cur_vals[c] = new_val
                    new_img[w, h] = tuple(list_cur_vals)
        new_img = np.fliplr(new_img)
        return new_img