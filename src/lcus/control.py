"""
Control device for LCUS relay board
"""
import time
from typing import List

import serial  # import serial from the pyserial package

class LCUS:
    """
    Device control
    """

    def __init__(self, device_path):
        self.port = serial.Serial(
            port=device_path,        # Which port is yours on? Update as needed.
            baudrate=9600,
            bytesize=8,
            timeout=2,
            stopbits=serial.STOPBITS_ONE,
            parity=serial.PARITY_NONE,
        )

        self.status = self.read_status()
        self.num_relays = len(self.status)
        print(f"Num Relays: {self.num_relays}")
        print(f"Status: {self.status}")

    def send_command(self, command):
        """Send a command to the USB relay."""
        self.port.write(command)
        time.sleep(0.1)  # Small delay to ensure the command is sent

    def read_status(self) -> List[bool]:
        """
        Reads status of each relay
        """

        self.send_command(bytes([0xff,0x0d,0xa]))       #query status command - returns a one byte per relay
        time.sleep(0.01)
        bytes_in = self.port.readline()
        status = []
        for b in bytes_in:
            status.append(b != 0)
        return status

    def set_relay_state(self, relay_index:int, on:bool):
        """
        Sets a relay status
        """
        msg = [0xA0, relay_index, int(on)]
        checksum = sum(msg)
        msg.append(checksum)
        self.send_command(bytes(msg))
