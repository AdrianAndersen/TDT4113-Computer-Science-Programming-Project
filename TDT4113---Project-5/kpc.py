""" TDT4113: Project 5 - Keypad """

from time import sleep

from keypad import Keypad
from led_board import LEDBoard
from logger.Logger import Logger


class KPC:
    """ Keypad controller coordinates activity between classes and password verification """

    __logger = Logger()

    def __init__(self, override_signal=None, password_file_path="password.txt"):
        self.current_led = 0
        self.duration_buffer = ""
        self.keypad = Keypad()
        self.led_board = LEDBoard()
        self.password_file_path = password_file_path
        self.override_signal = override_signal
        self.input_buffer = []
        self.previous_input_buffer = []
        self.actions = {
            None: lambda s=None: None,
            "A1": self.boot,
            "A2": self.append_password_char,
            "A3": self.verify_login,
            "A4": self.boot,
            "A5": lambda s=None: None,
            "A6": self.next_entry,
            "A7": self.next_entry,
            "A8": self.validate_passcode_change,
            "A9": self.choose_led,
            "A10": self.append_duration_digit,
            "A11": self.apply_led_lighting,
            "A12": self.show_power_down,
        }

    def boot(self, signal=None):
        """ Display power-up and reset input buffer """
        self.led_board.power_up_blink()
        self.reset_input_buffer()

    def next_entry(self, signal=None):
        """ Go to the next input stage """
        self.show_success()
        self.reset_input_buffer()
        self.__logger.debug("Entering next input stage")

    def reset_input_buffer(self, signal=None):
        """ Clear password buffer """
        self.previous_input_buffer = self.input_buffer
        self.input_buffer = []
        self.__logger.debug("Cleared input entry")

    def get_next_signal(self):
        """ Return override signal if not blank, otherwise query keypad for next pressed key """
        if self.override_signal is not None:
            sig = self.override_signal
            self.override_signal = None
            return sig
        return self.keypad.get_next_signal()

    def append_password_char(self, signal):
        """ Append a character to the password under construction """
        self.input_buffer.append(signal)
        self.__logger.debug(f"Appended character: {signal}")

    def choose_led(self, signal):
        """ Set the LED ID which is selected for activation """
        self.current_led = int(signal)

    def append_duration_digit(self, signal):
        """ Append a decimal digit to the duration (in seconds) the LED will be high for """
        self.duration_buffer += signal

    def apply_led_lighting(self, signal=None):
        """ Apply lighting to the inputted LED for the inputted duration """
        if self.duration_buffer != "":
            self.light_one_led(self.current_led, int(self.duration_buffer))
        self.duration_buffer = ""

    def verify_login(self, signal=None):
        """ Check that entered password matches the one in the password file """
        with open(self.password_file_path, "r") as pass_file:
            password = pass_file.readline()
            read_password = "".join(self.input_buffer)
            self.__logger.debug(
                f"Password received: {read_password}. Password expected: {password}"
            )
            if password == read_password:
                self.override_signal = "Y"
                self.show_success()
                self.reset_input_buffer()
                self.__logger.info("Succesfully logged in")
            else:
                self.override_signal = "N"
                self.show_failure()
                self.reset_input_buffer()
                self.__logger.info("Failed to log in")

    def validate_passcode_change(self, signal=None):
        """ Check that new password is valid """

        new_pass = "".join(self.previous_input_buffer)
        new_pass_confirm = "".join(self.input_buffer)
        if new_pass.isnumeric() and len(new_pass) >= 4:
            if new_pass_confirm == new_pass:
                with open(self.password_file_path, "w") as pass_file:
                    pass_file.write(new_pass)
                    self.show_success()
                    self.__logger.info("Succesfully changed password")
                    self.__logger.debug(f"New password: {new_pass}")
            else:
                self.__logger.debug("Passwords didn't match")
                self.__logger.debug(
                    f"First entry: {new_pass}. Second entry: {new_pass_confirm}"
                )
                self.__logger.info("Failed to change password")
        else:
            self.show_failure()
            self.__logger.debug(f"Malformed password candidate: {new_pass}")
            self.__logger.info("Failed to change password")
        self.reset_input_buffer()

    def light_one_led(self, led_id, led_duration):
        """ Request that LED #led_id is turned on for led_duration seconds"""
        self.led_board.light_led(led_id, duration=led_duration)

    def flash_leds(self):
        """ Call LED board and request flash all lights """
        self.led_board.flash_all_leds(1)

    def twinkle_leds(self):
        """ Call LED board and request twinkle all lights """
        self.led_board.twinkle_all_leds(1)

    def exit_action(self):
        """ Call LED board and request power down light sequence """
        self.led_board.power_down_blink()

    def show_success(self):
        """ Call LED board and request success sequence """
        self.led_board.twinkle_all_leds(0.5)

    def show_failure(self):
        """ Call LED board and request failure sequence """
        self.led_board.flash_all_leds(0.2)

    def show_power_down(self, signal=None):
        """ Call LED board and request power-down sequence """
        self.led_board.flash_all_leds(0.1)
        sleep(0.2)
        self.led_board.flash_all_leds(0.3)

    def do_action(self, action, signal):
        """ Perform submitted action """
        self.actions[action](signal)
