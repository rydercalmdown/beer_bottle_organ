import RPi.GPIO as GPIO
from threading import Thread
import time


class SolenoidController:

    def __init__(self):
        self.define_shift_register_pins()
        self.setup_gpio()
        self.set_note_map()
        self.set_default_pin_state()

    def __del__(self):
        self.cleanup()

    def define_shift_register_pins(self):
        self.data_pin = 17
        self.clock_pin = 27
        self.latch_pin = 22

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.data_pin, GPIO.OUT)
        GPIO.setup(self.clock_pin, GPIO.OUT)
        GPIO.setup(self.latch_pin, GPIO.OUT)

    def set_note_map(self):
        self.note_map = {
            'C4': 0,
            'D4': 1,
            'E4': 2,
            'F4': 3,
            'G4': 4,
            'A4': 5,
            'B4': 6,
            'C5': 7,
        }
        self.note_range = len(self.note_map.keys())

    def set_default_pin_state(self):
        self.solenoid_state = [0] * self.note_range

    def _shift_out(self, byte):
        for i in range(8):
            GPIO.output(self.data_pin, (byte >> i) & 1)
            GPIO.output(self.clock_pin, GPIO.HIGH)
            GPIO.output(self.clock_pin, GPIO.LOW)
        GPIO.output(self.latch_pin, GPIO.HIGH)
        GPIO.output(self.latch_pin, GPIO.LOW)

    def _update_solenoids(self):
        byte = 0
        for i, state in enumerate(self.solenoid_state):
            if state:
                byte |= (1 << i)
        self._shift_out(byte)

    def activate_solenoid(self, note):
        if note in self.note_map:
            index = self.note_map[note]
            self.solenoid_state[index] = 1
            Thread(target=self._update_solenoids).start()

    def deactivate_solenoid(self, note):
        if note in self.note_map:
            index = self.note_map[note]
            self.solenoid_state[index] = 0
            Thread(target=self._update_solenoids).start()

    def cleanup(self):
        GPIO.cleanup()
