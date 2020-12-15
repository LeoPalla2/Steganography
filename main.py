import png, array,argparse
import sys

def encode_message(data, pixels):
    index = 0
    for char in data:
        pixels_to_change = pixels[index * 4 : (index + 2) * 4]
        bytechar = f'{ord(char):08b}'
        for i, bit in enumerate(bytechar):
            pixels_to_change[i] = change_value(bit, pixels_to_change[i])
        pixels[index * 4 : (index + 2) * 4] = pixels_to_change
        index = index + 2


def change_value(bit, pix_value):
    if bit == '0':
        if pix_value % 2 != 0:
            if pix_value == 255:
                return pix_value - 1
            else:
                return pix_value + 1
        else:
            return pix_value
    elif bit == '1':
        if pix_value % 2 == 0:
            if pix_value == 0:
                return pix_value + 1
            else:
                return pix_value - 1
        else:
            return pix_value

def decode(pixels):
    decoded_message = ""
    while ("^C" not in decoded_message):
        encoded_char = pixels[len(decoded_message) * 8 : (len(decoded_message) + 1) * 8]
        decoded_message = decoded_message + decode_char(encoded_char)
    return decoded_message[:-2].replace("\\n",'\n')

def decode_char(pix_list):
    decoded_char = ""
    for pix in pix_list:
        if pix % 2 == 0:
            decoded_char = decoded_char + '0'
        else:
            decoded_char = decoded_char + '1'
    return chr(int(decoded_char, 2))

def encode_message_from_file(image, file):
    f = open(file, 'r')
    text = f.read()
    reader = png.Reader(filename = image)
    w, h, pixels, metadata = reader.read_flat()
    if metadata['alpha']:
        if len(text) >= int((w * h) / 4):
            print("The specified text is too long to be encoded!")
            sys.exit()
    else:
        if len(text) >= int((w * h) / 3):
            print("The specified text is too long to be encoded!")
            sys.exit()
    text = text + '^C'
    encode_message(text, pixels)
    output = open(image, 'wb')
    writer = png.Writer(w, h, **metadata)
    writer.write_array(output, pixels)
    output.close()

def encode_message_from_input(image):
    text = input("Enter text you want to encode in image: \n")
    reader = png.Reader(filename = image)
    w, h, pixels, metadata = reader.read_flat()
    if metadata['alpha']:
        if len(text) >= int((w * h) / 4):
            print("The specified text is too long to be encoded!")
            sys.exit()
    else:
        if len(text) >= int((w * h) / 3):
            print("The specified text is too long to be encoded!")
            sys.exit()
    text = text + '^C'
    encode_message(text, pixels)
    output = open(image, 'wb')
    writer = png.Writer(w, h, **metadata)
    writer.write_array(output, pixels)
    output.close()


def encode_message_from_text(image, text):
    reader = png.Reader(filename = image)
    w, h, pixels, metadata = reader.read_flat()
    if metadata['alpha']:
        if len(text) >= int((w * h) / 4):
            print("The specified text is too long to be encoded!")
            sys.exit()
    else:
        if len(text) >= int((w * h) / 3):
            print("The specified text is too long to be encoded!")
            sys.exit()
    text = text + '^C'
    encode_message(text, pixels)
    output = open(image, 'wb')
    writer = png.Writer(w, h, **metadata)
    writer.write_array(output, pixels)
    output.close()
        
def decode_message(image):
    reader = png.Reader(filename = image)
    w, h, pixels, metadata = reader.read_flat()
    print(decode(pixels))

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
parser.add_argument("image", help = "Path to the image you want to read from / write into")
parser.add_argument("-w", help = "Specify that the program should write a message. If the argument is not provided, the program will be in reading mode", action = "store_true")
group.add_argument("-f", help = "Optional argument : reads from file")
group.add_argument("-t", help = "Optional argument : reads from text")

args = parser.parse_args()

if args.w:
    if args.f:
        encode_message_from_file(args.image,args.f)
    elif args.t:
        encode_message_from_text(args.image,args.t)
    else:
        encode_message_from_input(args.image)
else: 
    decode_message(args.image)

