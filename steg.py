#!/usr/bin/env python
# coding: UTF-8

import numpy as np

class LSB_steg():

    def __init__(self, in_img):
        self.image = in_img
        self.height, self.width, self.nbchannels = in_img.shape
        self.size = self.width * self.height
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
                        print("Image is completely filled. No spots remaining.")
                        exit(1)
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
        bin_length = self.binary_value(len(text), 16)
        self.put_bin_val(bin_length)
        # encode the actual text
        for c in text:
            self.put_bin_val(self.binary_value(ord(c), 8))
        return self.image

    # decode text
    def decode_text(self):
        text_size = ""

        # check order of bits

        for i in range(16):
            text_size += self.decode_bit()
        #print (int(text_size, 2))
        res = ""
        for i in range(int(text_size, 2)):
            temp = ""
            for i in range(8):
                temp += self.decode_bit()
            res += chr(int(temp, 2))
        return res

    # encode binary file
    def encode_binary(self, data):
        if self.size*self.nbchannels < len(data)+64:
            print ("Our carrier image is not big enough to encrypt this file!")
            exit(1)
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



"""
def LSB_steg(in_img, option):
    # create steg object
    steg_obj = LSB_steg(in_img)

    # encode
    if option == '-e':
        data = open(sys.argv[4], "rb").read()
        res = steg_obj.encode_binary(data)
        cv2.imwrite(sys.argv[3], res)
    # decode
    else:
        raw = steg_obj.decode_binary()
        with open(sys.argv[3], "wb") as f:
            f.write(raw)

def example_usage():
    print('Usage: python steg.py -e/-d [input] [output] [file]')

def main():
    # check for valid arguments:
    # -check length
    # -check options
    if len(sys.argv) != 5 or (not sys.argv[1] in ['-e', '-d']):
        print('Invalid arguments!\n')
        example_usage()
        exit(1)

    # read in the input image
    input_img = cv2.imread(sys.argv[2])

    # call main steg function
    steg = LSB_steg(input_img, sys.argv[1])

if __name__=='__main__':
    main()
"""