import binascii

from processor import Processor


class Chip:
    def __init__(self, rom):
        self.ram = [None for i in range(4095)]  # initialize ram
        self.cpu = Processor(self.ram)
        if rom is not None:
            self.load_program(rom)

    def load_program(self, content):
        self.cpu.initial_load(content)

    def run(self):
        while True:
            if not self.CPU.tick():
                break

    def dump_ram(self):
        i = 0
        while i < len(self.ram)-1:
            if self.ram[i] is not None:
                code = self.cpu.merge_bytes(self.ram[i], self.ram[i + 1])
                print("0x{:04x}".format(code))
            i += 2
