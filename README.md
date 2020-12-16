# Steganography
Python tool for encoding / decoding data in images
<br></br>
Handles PNG images with and without Alpha channel.
<br></br>

# Usage

The script should be executable on its own on linux, but you have to use python if you're on windows.  
Arguments are:  
<ul>
<li> image : path to the image you want to read from / write into</li>
<li> -w : The program will write in the image if this argument is provided, otherwise it will read from it</li>
<li> -t text : text you want to write in the image. Only usable in write mode</li>
<li> -f file : path to the file that will have its content written in the image. Only usable in write mode </li>
<li> if none of the arguments above is specified, the text will be read from standard input </li>
</ul>

# Program Description

## Write Mode

The program will hide a message into the image by slightly changing the value of the pixels.  
Each character is transformed in its binary equivalent, and then the value of pixels in the image will be changed. If the bit is a 0, the value will be changed to an even number, and to an odd number if it's 1.  
A special character (End Of Text) is added at the end of the text before getting written inside the image. It will help when decoding to tell the program where to stop.  
<br></br>
Note : The message will be hidden in the input image, no new image will be created.

## Read Mode

The program will read from the image by reading each pixel value and finding the corresponding bit value explained in the write mode section. Each series of 8 bits will then be converted to a character and added to the message. When the program encounters the End Of Text character, it stops and return the message.
