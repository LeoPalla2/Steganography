#!/usr/bin/env python3

import png, array,argparse
import sys

def encode(data, pixels, pix_length):
    '''
    (string, list of int, int) -> void
    hide text in array of pixels by modifying their value
    '''

    index = 0
    pix_char_size = 3 if pix_length == 3 else 2
    for char in data:
        pixels_to_change = pixels[index * pix_length : (index + pix_char_size) * pix_length]
        bytechar = f'{ord(char):08b}'
        for i, bit in enumerate(bytechar):
            pixels_to_change[i] = change_value(bit, pixels_to_change[i])
        pixels[index * pix_length : (index + pix_char_size) * pix_length] = pixels_to_change
        index = index + pix_char_size


def change_value(bit, pix_value):
    ''' (char, int) -> int
    Change the value of a pixel depending on the value of a given bit
    '''

    if bit == '0':
        if pix_value % 2 != 0:
            return pix_value-1
        else:
            return pix_value
    elif bit == '1':
        if pix_value % 2 == 0:
            return pix_value + 1
        else:
            return pix_value

def decode(pixels, pixel_length):
    '''
    (list of int, int) -> string
    Decypher message hidden in an image
    '''

    decoded_message = ""
    char_size = 2 if pixel_length == 4 else 3
    while (chr(3) not in decoded_message):
        encoded_char = pixels[len(decoded_message) * (char_size * pixel_length) : (len(decoded_message) + 1) * (char_size * pixel_length)]
        decoded_message = decoded_message + decode_char(encoded_char, pixel_length)
    return decoded_message[:-1].replace("\\n",'\n')

def decode_char(pix_list, pixel_length):
    '''
    (list of int, int) -> char
    Decypher a single character hidden in subpart of an image
    '''

    decoded_char = ""
    for pix in pix_list:
        if pix % 2 == 0:
            decoded_char = decoded_char + '0'
        else:
            decoded_char = decoded_char + '1'
    if pixel_length == 4:
        return chr(int(decoded_char, 2))
    else:
        return chr(int(decoded_char[:-1], 2))


def encode_message(image, text):
    '''
    (string, string) -> void
    Hides text in image
    '''
    try:
        reader = png.Reader(filename = image)
        w, h, pixels, metadata = reader.read_flat()
    except FileNotFoundError:
        print("Image not found!")
        sys.exit()
    except png.FormatError:
        print("Image is not a PNG file or has invalid signature!")
        sys.exit()

    if metadata['alpha']:
        if len(text) >= int((w * h) / 2):
            print("The specified text is too long to be encoded!")
            sys.exit()
        pixel_size = 4
        
    else:
        if len(text) >= int((w * h) / 3):
            print("The specified text is too long to be encoded!")
            sys.exit()
        pixel_size = 3
        metadata.pop('physical',None)
        
    text = text + chr(3)
    encode(text, pixels, pixel_size)
    output = open(image, 'wb')
    writer = png.Writer(w, h, **metadata)
    writer.write_array(output, pixels)
    output.close()
        
def decode_message(image):
    '''
    (string) -> void
    prints text found in an image
    '''

    try:
        reader = png.Reader(filename = image)
        w, h, pixels, metadata = reader.read_flat()
    except FileNotFoundError:
        print("Image not found!")
        sys.exit()
    except png.FormatError:
        print("Image is not a PNG file or has invalid signature!")
        sys.exit()

    if metadata['alpha']:
        pixel_length = 4
    else:
        pixel_length = 3
    print(decode(pixels,pixel_length))

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
parser.add_argument("image", help = "Path to the image you want to read from / write into")
parser.add_argument("-w", help = "Specify that the program should write a message. If the argument is not provided, the program will be in reading mode", action = "store_true")
group.add_argument("-f", help = "Optional argument : reads from file")
group.add_argument("-t", help = "Optional argument : reads from text")

args = parser.parse_args()

if args.w:
    if args.f:
        f = open(args.f, 'r')
        text = f.read()
    elif args.t:
        text = args.t
    else:
        text = input("Enter text you want to encode in image: \n")
    encode_message(args.image, text)
else: 
    decode_message(args.image)

