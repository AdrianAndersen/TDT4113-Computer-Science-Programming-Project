""" TDT4113: Project 5 - Keypad """

import time

from GPIOSimulator_v5 import N_LEDS, GPIOSimulator, charlieplexing_pins


class LEDBoard:
    """ An interface to the simulated Charlieplexed LED board """

    def __init__(self):
        """ Initialize a GPIO simulator and perform setup """
        self.gpio = GPIOSimulator()

        high = self.gpio.HIGH
        low = self.gpio.LOW
        out = self.gpio.OUT
        inn = self.gpio.IN

        # Dictionary that shows which state pins need to be in for a specific LED
        self.led_mapping = {
            0: [high, low, low],
            1: [low, high, low],
            2: [low, high, low],
            3: [low, low, high],
            4: [high, low, low],
            5: [low, low, high],
        }
        # Dictionary for mapping which pins should be out and in for a specific LED
        self.charlie_mapping = {
            0: [out, out, inn],
            1: [out, out, inn],
            2: [inn, out, out],
            3: [inn, out, out],
            4: [out, inn, out],
            5: [out, inn, out],
        }

    def light_led(self, led, duration):
        """ Light a specific LED on the charlieplexed LED board """
        # Get the settings for lighting the specific LED
        self.__led_settings(led)
        # Print the LED states to the console
        self.gpio.show_leds_states()
        time.sleep(duration)
        self.gpio.cleanup()
        self.gpio.show_leds_states()

    def flash_all_leds(self, duration):
        """ Flash all LEDs on and off for k seconds"""
        for i in range(N_LEDS):
            self.__led_settings(i)
        # Print the LED states to the console
        self.gpio.show_leds_states()
        # Do nothing for the specified k seconds
        time.sleep(duration)
        # Reset pins
        self.gpio.cleanup()
        # Print the LED states to the console
        self.gpio.show_leds_states()

    def twinkle_all_leds(self, duration):
        """ Turn LEDs on and off in sequence for k seconds """
        # For each LED, twinkle that LED
        for i in range(N_LEDS):
            self.__led_settings(i)
            self.gpio.show_leds_states()
            # Let the LED "twinkle" for duration / N_LEDS time
            time.sleep(duration / N_LEDS)
            self.gpio.cleanup()

    def power_up_blink(self):
        """ Light pattern associated with powering up the system """
        # Blinks 4 middle LEDs and first+last LEDs in turn
        for i in range(N_LEDS - 1):
            if i % 2 == 0:
                self.__led_settings(1)
                self.__led_settings(2)
                self.__led_settings(3)
                self.__led_settings(4)
                self.gpio.show_leds_states()
            else:
                self.__led_settings(0)
                self.__led_settings(5)
                self.gpio.show_leds_states()
            time.sleep(0.5)
            self.gpio.cleanup()

    def power_down_blink(self):
        """ Light pattern associated with powering down the system """
        # First twinkle LEDs in correct order (0-5)
        self.twinkle_all_leds(1)
        # Then twinkle LEDs in reversed order (5-0)
        for i in range(5):
            self.__led_settings(4 - i)
            self.gpio.show_leds_states()
            # Let the LED "twinkle" for duration / N_LEDS time
            time.sleep(0.2)
            self.gpio.cleanup()

    def __led_settings(self, led):
        """ Sets up the charlieplexed pins according to some settings """
        # Get the states for a particular LED
        led_state_setting = self.led_mapping.get(led)
        # Get specified settings for which modes pins should be in
        charlie_mode_setting = self.charlie_mapping.get(led)

        # Set up charlieplexed pins with correct mode
        for i in range(len(charlieplexing_pins)):
            self.gpio.setup(i, charlie_mode_setting[i])

        # Set let state on output pins only
        for i in range(len(charlieplexing_pins)):
            if charlie_mode_setting[i] == self.gpio.OUT:
                self.gpio.output(i, led_state_setting[i])
