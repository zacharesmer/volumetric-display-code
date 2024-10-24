# Hardware
I have a much more detailed writeup [here](https://resmer.co.za/ch/posts/volumetric-display/) with pictures and information about the hardware.

# Building
This project follows the getting started with pico example very closely. That is available from raspberry pi here: https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf

To build and upload the files to the pico, I used VS Code and the raspberry pi pico extension, again following the outline in the getting started guide. 

# Displaying an image
Once you have made an object in blender and exported images of it from 40 angles, run `python3 render.py <dirname>` and it will print out a C array, ready for you to paste into objects.h. Do that, update the name at the end of `be_an_object.c` if you need to, and let 'er rip. Or if you want to use my cube, just leave it how it is.

You could also use a different number of images if you want, just adjust `ROTATIONAL_SLICES` in `be_an_object.c`. I chose 40 because that made the distance between angular "pixels" somewhat comparable to the space between the LEDs on the board.

# Contributing
This is pretty bare bones because I'd be a little surprised if anyone ever builds this object and uses this code. If you do I'd love to see it, and if you find something that doesn't work, please let me know! I made some minor changes after I'd taken apart my debug board so I didn't test it again, so it's possible something is a little wrong. It definitely compiles, though.