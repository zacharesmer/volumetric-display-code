"""
Which GPIO pins go to which contacts on the LED matrix
If your LEDs are attached to different GPIO pins, adjust the U_X and L_X values
U for upper sub-grid, L for lower sub-grid

I would have used something more descriptive, but the conversion tuple wouldn't have fit on one screen

The way the code for the pico iterates through the pins assumes that each grid uses adjacent GPIO pins,
but you could make some minor adjustments to use arbitrary pins
(Currently that code shifts the bits directly, but it could just as easily iterate over an array of masks)
"""
U_0 = 2
U_1 = 3
U_2 = 4
U_3 = 5
U_4 = 6
U_5 = 7
U_6 = 8
U_7 = 9
U_8 = 10

L_0 = 27
L_1 = 26
L_2 = 22
L_3 = 21
L_4 = 20
L_5 = 19
L_6 = 18
L_7 = 17
L_8 = 16

upper_pins = [U_0, U_1, U_2, U_3, U_4, U_5, U_6, U_7, U_8]
lower_pins = [L_0, L_1, L_2, L_3, L_4, L_5, L_6, L_7, L_8]

""""Each sub-tuple (A, B) represents 1 pixel in the LED grid.

A is which scan line it should be part of. The scan lines don't directly map to rows, but this is  
like a row selector. For each scan line one pin on each grid will always be high. Which pins are high for 
which scan line is defined in `row_masks` in the code that runs on the microcontroller.

B is which pin is low in each scan line to get a particular pixel to light up. This is sort of like
a column selector.

The funky formatting matches with the wiring of the LEDs
"""

pixel_high_low_tuple = (
    (0, U_8), (0, U_7), (0, U_6), (0, U_5), (0, U_4), (0, U_3), (0, U_2), (0, U_1),           (1, U_0),
    (1, U_8), (1, U_7), (1, U_6), (1, U_5), (1, U_4), (1, U_3), (1, U_2),           (2, U_1), (2, U_0),
    (2, U_8), (2, U_7), (2, U_6), (2, U_5), (2, U_4), (2, U_3),           (3, U_2), (3, U_1), (3, U_0),
    (3, U_8), (3, U_7), (3, U_6), (3, U_5), (3, U_4),           (4, U_3), (4, U_2), (4, U_1), (4, U_0),
    (4, U_8), (4, U_7), (4, U_6), (4, U_5),           (5, U_4), (5, U_3), (5, U_2), (5, U_1), (5, U_0),
    (5, U_8), (5, U_7), (5, U_6),           (6, U_5), (6, U_4), (6, U_3), (6, U_2), (6, U_1), (6, U_0),
    (6, U_8), (6, U_7),           (7, U_6), (7, U_5), (7, U_4), (7, U_3), (7, U_2), (7, U_1), (7, U_0),
    (7, U_8),           (8, U_7), (8, U_6), (8, U_5), (8, U_4), (8, U_3), (8, U_2), (8, U_1), (8, U_0),

    (0, L_8), (0, L_7), (0, L_6), (0, L_5), (0, L_4), (0, L_3), (0, L_2), (0, L_1),           (1, L_0),
    (1, L_8), (1, L_7), (1, L_6), (1, L_5), (1, L_4), (1, L_3), (1, L_2),           (2, L_1), (2, L_0),
    (2, L_8), (2, L_7), (2, L_6), (2, L_5), (2, L_4), (2, L_3),           (3, L_2), (3, L_1), (3, L_0),
    (3, L_8), (3, L_7), (3, L_6), (3, L_5), (3, L_4),           (4, L_3), (4, L_2), (4, L_1), (4, L_0),
    (4, L_8), (4, L_7), (4, L_6), (4, L_5),           (5, L_4), (5, L_3), (5, L_2), (5, L_1), (5, L_0),
    (5, L_8), (5, L_7), (5, L_6),           (6, L_5), (6, L_4), (6, L_3), (6, L_2), (6, L_1), (6, L_0),
    (6, L_8), (6, L_7),           (7, L_6), (7, L_5), (7, L_4), (7, L_3), (7, L_2), (7, L_1), (7, L_0),
    (7, L_8),           (8, L_7), (8, L_6), (8, L_5), (8, L_4), (8, L_3), (8, L_2), (8, L_1), (8, L_0),
)
