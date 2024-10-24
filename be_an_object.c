#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "pico/binary_info.h"
#include "pico/time.h"

#include "objects.h"

// Some non-LED pins are used for serial debugging and other important things
// this is a silly way to write this since I only ever use it with ~, but I 
// guessed wrong and figured out the bit mask this way first
const uint NOT_LEDS_MASK = 0x380f803;

const uint IR_SENSOR = 14;
const uint ROTATIONAL_SLICES = 40;
const uint SCAN_LINES = 9;
// to adjust for time taken performing the calculations to display each scan line
const uint TUNING_PARAMETER = 0;

// counter for which rotational slice we're on
volatile uint SLICE = 0;

absolute_time_t current_rotation_start;
absolute_time_t previous_rotation_start;
// this is int64 because that's what the fuction to set it returns, not because it will ever
// be large enough to require 64 bits
volatile int64_t rotation_time;

// approximate value probably
uint delay = 92;

uint test_pattern_smiley[9] = {0x0, 0x310, 0x20308, 0x4020318, 0x4040318, 0x400018, 0x380000, 0x0, 0x0};
// 2 rows can be addressed at once, so these have 2 bits set
uint row_masks[9] = {0x8000004, 0x4000008, 0x400010, 0x200020, 0x100040, 0x80080, 0x40100, 0x20200, 0x10400};

// high_mask chooses the row
// output mask chooses which pixels in that row light up
int light_up_masked(uint high_mask, uint output_mask)
{
    gpio_put_masked(~NOT_LEDS_MASK, high_mask);
    gpio_set_dir_masked(~NOT_LEDS_MASK, output_mask);
    return 0;
}

// delay is the delay for each row, so this will take (number of rows) * (delay) microseconds
int make_a_pattern(uint one_frame[9], uint delay)
{
    for (int row_index = 0; row_index < 9; row_index++)
    {
        light_up_masked(row_masks[row_index], (one_frame[row_index]) | row_masks[row_index]);
        sleep_us(delay);
    }
}

void update_delay()
{
    // how many microseconds to display each scan line

    // rotation_time us | 1 rotation | 1 frame
    // -----------------|------------|-------------- = delay us/scan line
    //    1 rotation    |  40 frames | 9 scan lines

    current_rotation_start = get_absolute_time();
    rotation_time = absolute_time_diff_us(previous_rotation_start, current_rotation_start);
    delay = rotation_time / (ROTATIONAL_SLICES * SCAN_LINES) - TUNING_PARAMETER;
    previous_rotation_start = current_rotation_start;
    // reset to the first rotational slice every rotation so the image doesn't drift
    SLICE = 0;
}

int main()
{
    // initialize this before the interrupt is called
    previous_rotation_start = get_absolute_time();

    // may not be necessary except for debugging
    stdio_init_all();

    // Initialize all the LED pins
    gpio_init_mask(~NOT_LEDS_MASK);

    for (int i = 2; i <= 29; i++)
    {
        gpio_set_drive_strength(i, GPIO_DRIVE_STRENGTH_4MA);
    }

    gpio_init(IR_SENSOR);
    // false means input
    gpio_set_dir(IR_SENSOR, false);
    gpio_set_irq_enabled_with_callback(IR_SENSOR, GPIO_IRQ_EDGE_RISE, true, &update_delay);
    
    while (1)
    {   
            make_a_pattern(a_cube[SLICE], delay);
            if (SLICE < (ROTATIONAL_SLICES - 1))
            {
                SLICE++;
            }
    }
}
