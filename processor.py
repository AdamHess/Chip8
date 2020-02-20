initial_pc = 0x200


def get_lower_three_nibbles(upper_byte, lower_byte):
    return (upper_byte & 0x0F << 8) + lower_byte

def get_first_nibble(upper_byte):
    return (upper_byte & 0xF0)

class Processor:
    def __init__(self, ram):
        self.V = [None for i in range(16)]  # VN registers
        self.I = 0x000
        self.PC = initial_pc  # program counter
        self.SP = 0x00  # stack pointer
        self.stack = [0 for i in range(16)]
        self.ram = ram
        self.screen = [[0 for x in range(64)] for y in range(32)] # 64x32 pixel screen use 0 or 1

    def tick(self):
        lower_byte = self.ram[self.PC]
        upper_byte = self.ram[self.PC+1]
        self.execute(upper_byte, lower_byte)
        self.PC += 2

    def initial_load(self, content):
        i = initial_pc
        for el in content:
            self.ram[i] = el
            i += 1

    def merge_bytes(self, lower_byte, upper_byte):
        return (upper_byte << 8) + (lower_byte)

    def execute(self, upper_byte, lower_byte):
        if upper_byte is 0x00:
            if lower_byte is 0xE0:
                self.wipe_screen()
            if lower_byte is 0xEE:
                self.stack_pop_address_to_pc()
            else:
                raise Exception("Invalid Instruction: SYS addr not implemented")
        if get_first_nibble(upper_byte) is 0x10:
            self.jump_to(get_lower_three_nibbles(upper_byte, lower_byte))
        if get_first_nibble(upper_byte) is 0x20:
            self.call(get_lower_three_nibbles(upper_byte, lower_byte))


    def wipe_screen(self):  #CLS
        self.screen = [[0 for x in range(64)] for y in range(32)]  # 64x32 pixel screen use 0 or 1
        pass

    def stack_pop_address_to_pc(self):  # RET
        self.PC = self.stack[self.SP]
        self.SP -= 1

    def jump_to(self, address):# JP addr
        self.PC = address

    def call(self, address):  # CALL addr
        self.SP += 1
        self.stack[self.SP] = self.PC
        self.PC = address
