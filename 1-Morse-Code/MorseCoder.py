import time
from datetime import datetime

from GPIOSimulator_v1 import *
from logger.Logger import Logger
from Utils import Utils


class MorseCoder:
    __MORSE_CODE = {
        ".-": "a",
        "-...": "b",
        "-.-.": "c",
        "-..": "d",
        ".": "e",
        "..-.": "f",
        "--.": "g",
        "....": "h",
        "..": "i",
        ".---": "j",
        "-.-": "k",
        ".-..": "l",
        "--": "m",
        "-.": "n",
        "---": "o",
        ".--.": "p",
        "--.-": "q",
        ".-.": "r",
        "...": "s",
        "-": "t",
        "..-": "u",
        "...-": "v",
        ".--": "w",
        "-..-": "x",
        "-.--": "y",
        "--..": "z",
        ".----": "1",
        "..---": "2",
        "...--": "3",
        "....-": "4",
        ".....": "5",
        "-....": "6",
        "--...": "7",
        "---..": "8",
        "----.": "9",
        "-----": "0",
    }
    __logger = Logger()
    __current_symbol = ""
    __current_word = ""
    __output = ""

    __SIGNAL_DURATION_BASE = 0.1
    __SIGNAL_DURATION_DOT = __SIGNAL_DURATION_BASE
    __SIGNAL_DURATION_DASH = __SIGNAL_DURATION_BASE * 3
    __SIGNAL_DURATION_SYMBOL_COMPLETE = __SIGNAL_DURATION_BASE * 10
    __SIGNAL_DURATION_WORD_COMPLETE = __SIGNAL_DURATION_BASE * 20
    __SIGNAL_DURATION_RESET = __SIGNAL_DURATION_BASE * 50

    __GPIO = GPIOSimulator()

    def __init__(self):
        self.__GPIO.setup(PIN_BTN, self.__GPIO.IN, self.__GPIO.PUD_DOWN)

    def __reset(self):
        """ reset the variable for a new run """
        self.__logger.debug("Reseting output...")
        self.__current_symbol = ""
        self.__current_word = ""
        self.__output = ""

    def __read_one_signal(self):
        """ read a signal from Raspberry Pi """
        return str(self.__GPIO.input(PIN_BTN))

    def __print_state(self, current_signal, signal_duration):
        Utils().clear_terminal()
        print("Symbol: ", self.__current_symbol)
        print("Word: ", self.__current_word)
        print("Output: ", self.__output)
        print("Current signal: ", current_signal)
        print("Signal duration: ", round(signal_duration, 2))

        if current_signal == "0":
            if len(self.__current_symbol) > 0:
                print(
                    "Time until symbol COMPLETE: ",
                    round(self.__SIGNAL_DURATION_SYMBOL_COMPLETE - signal_duration, 2),
                )

            if len(self.__current_word) > 0:
                print(
                    "Time until word COMPLETE: ",
                    round(self.__SIGNAL_DURATION_WORD_COMPLETE - signal_duration, 2),
                )

            if len(self.__output) > 0:
                print(
                    "Time until RESET: ",
                    round(self.__SIGNAL_DURATION_RESET - signal_duration, 2),
                )

    def __decoding_loop(self):
        """ the main decoding loop """

        start_time = time.time()
        signal_duration = 0
        prev_signal = "0"
        while True:
            current_signal = self.__read_one_signal()
            self.__logger.debug(f"current signal: {current_signal}")
            self.__logger.debug(f"prev_signal: {prev_signal}\n")

            if current_signal == "0" and prev_signal == "1":
                # Button release

                now = time.time()
                signal_duration = now - start_time
                self.__logger.debug(f"Signal ended. duration: {signal_duration}")

                if signal_duration >= self.__SIGNAL_DURATION_DASH:
                    self.__process_signal("-")
                elif signal_duration >= self.__SIGNAL_DURATION_DOT:
                    self.__process_signal(".")

            elif current_signal == "0" and prev_signal == "0":
                # Pause / no signal

                now = time.time()
                signal_duration = now - start_time
                if signal_duration > self.__SIGNAL_DURATION_RESET:
                    # Reset all output
                    self.__reset()
                elif (
                    signal_duration > self.__SIGNAL_DURATION_WORD_COMPLETE
                    and len(self.__current_word) > 0
                ):
                    # Long (word) pause
                    self.__process_signal("WORD_COMPLETE")
                elif (
                    signal_duration > self.__SIGNAL_DURATION_SYMBOL_COMPLETE
                    and len(self.__current_symbol) > 0
                ):
                    # Medium (letter) pause
                    self.__process_signal("SYMBOL_COMPLETE")

            if current_signal != prev_signal:
                self.__logger.debug("Detected signal change...")
                start_time = time.time()

            self.__print_state(current_signal, signal_duration)
            time.sleep(0.05)
            prev_signal = current_signal

    def __process_signal(self, signal):
        """ handle the signals using corresponding functions """
        if signal == "." or signal == "-":
            self.__update_current_symbol(signal)
        elif signal == "SYMBOL_COMPLETE":
            self.__handle_symbol_end()
        elif signal == "WORD_COMPLETE":
            self.__handle_word_end()
        else:
            self.__reset()

    def __update_current_symbol(self, signal):
        """ append the signal to current symbol code """
        self.__current_symbol += signal
        self.__logger.debug(f"current_symbol: {self.__current_symbol}")

    def __update_current_word(self, symbol):
        """ Add the most recently completed symbol onto current word """
        self.__current_word += symbol
        self.__logger.debug(f"Current word: {self.__current_word}")

    def __handle_symbol_end(self):
        """ process when a symbol ending appears """
        self.__logger.debug(
            f"Checking whether {self.__current_symbol} is in {list(self.__MORSE_CODE.keys())}"
        )
        if self.__current_symbol in list(self.__MORSE_CODE.keys()):
            new_symbol = self.__MORSE_CODE[self.__current_symbol]
            self.__update_current_word(new_symbol)
            self.__logger.debug(f"Symbol completed: {new_symbol}")
        else:
            self.__logger.warning(f"Illegal symbol: {self.__current_symbol}")
            self.__update_current_word("?")

        self.__current_symbol = ""

    def __handle_word_end(self):
        """ process when a word ending appears """
        self.__logger.info(f"Word completed: {self.__current_word}")
        self.__output += self.__current_word
        self.__output += " "
        self.__current_word = ""

    def start_decode_mode(self):
        print("You are now in decode mode. Please enter morse by pressing *spacebar*\n")
        self.__decoding_loop()

    # Methods for encoding:

    def __get_key(self, char):
        legal_chars = list(self.__MORSE_CODE.values())
        if char not in legal_chars:
            self.__logger.warning(f"Illegal character: '{char}'")
            return char

        # Find the corresponding morse code for a char
        for key, value in self.__MORSE_CODE.items():
            if char == value:
                return key

        return char

    def __encode(self, input_str):
        result = ""
        for char in input_str:
            result = result + self.__get_key(char)
        return result

    def start_encode_mode(self):
        self.__logger.info(
            "You are now in encode mode. Please enter at text string to encode and press enter..."
        )
        while True:
            input_str = input("").lower()
            self.__logger.info(f"{input_str} => {self.__encode(input_str)}\n")
