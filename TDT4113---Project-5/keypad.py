""" TDT4113: Project 5 - Keypad """

import time

import GPIOSimulator_v5 as Sim

GPIO = Sim.GPIOSimulator()


class Keypad:
    """ An interface to the simulated keypad """

    keypad_values = {
        0: {
            0: "1",
            1: "2",
            2: "3",
        },
        1: {
            0: "4",
            1: "5",
            2: "6",
        },
        2: {
            0: "7",
            1: "8",
            2: "9",
        },
        3: {
            0: "*",
            1: "0",
            2: "#",
        },
    }

    def __init__(self, poll_interval=0.01):
        self.setup()
        self.poll_interval = poll_interval

    @staticmethod
    def setup():
        """ Initialize row pins as output and column pins as input """

        for row_pin in Sim.keypad_row_pins:
            GPIO.setup(row_pin, GPIO.OUT)

        for col_pin in Sim.keypad_col_pins:
            GPIO.setup(col_pin, GPIO.IN, state=GPIO.LOW)

    @staticmethod
    def do_polling():
        """ Determine which key is being pressed on the keypad """

        inp = None
        for row_pin in Sim.keypad_row_pins:
            # Loop through every row pin and set its value to HIGH
            GPIO.output(row_pin, GPIO.HIGH)
            for col_pin in Sim.keypad_col_pins:
                # Loop through every column pin and check its input state
                if GPIO.input(col_pin) == GPIO.HIGH:
                    # If column pin is HIGH, set inp_state and break out of for loop
                    inp = (
                        row_pin - Sim.keypad_row_pins[0],
                        col_pin - Sim.keypad_col_pins[0],
                    )
                    break  # Leave inner loop

            GPIO.output(row_pin, GPIO.LOW)
            # Set the row pin back to LOW

            if inp is not None:
                break  # Leave outer loop

        return inp

    def get_next_signal(self, poll_interval=None):
        """
        Interface between KPC and keypad,
        that repeatedly does polling until key press detected
        """

        if poll_interval is None:
            poll_interval = self.poll_interval

        poll = self.do_polling()
        while poll is None:
            # Do: retrieve a poll every 'self.poll_interval' seconds
            # While: the poll is None
            poll = self.do_polling()
            time.sleep(poll_interval)
        # start = time.time_ns()

        while self.do_polling() == poll:
            time.sleep(poll_interval)
        # end = time.time_ns()

        # Could do a check of signal length etc here

        return Keypad.keypad_values[poll[0]][poll[1]]
