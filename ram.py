import binascii
from memory import Memory


class RAM:
    def __init__(self, size=4095):
        self.memory = [Memory() for i in range(size)]

    def set(self, index, value):
        self.memory[index].set(value)

    def get(self, index):
        self.memory[index].get()

    def bulk_load(self, start_location, entries):
        location_pointer = start_location
        for el in entries:
            if self.memory[location_pointer] is None:
                raise Exception("Exceeded Dimensions of Memory")
            self.memory[location_pointer].set(el)
            location_pointer += 1

    def dump_memory(self):
        for el in self.memory:
            print(binascii.hexlify(el.get()), end='')
