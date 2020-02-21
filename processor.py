initial_pc = 0x200


def get_lower_three_nibbles(upper_byte, lower_byte):
    return (upper_byte & 0x0F << 8) + lower_byte


def get_upper_nibble(upper_byte):
    return (upper_byte & 0xF0)


def get_lower_nibble(upper_byte):
    return (upper_byte & 0x0F)


class Processor:
    def __init__(self, ram):
        self.V = [None for i in range(16)]  # VN registers 16 bit wide
        self.I = 0x000
        self.PC = initial_pc  # program counter
        self.SP = 0x00  # stack pointer
        self.stack = [0 for i in range(16)]
        self.ram = ram
        self.screen = [[0 for x in range(64)] for y in range(32)]  # 64x32 pixel screen use 0 or 1

    def tick(self):
        lower_byte = self.ram[self.PC]
        upper_byte = self.ram[self.PC + 1]
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
        # Zeros out the upper or lower section, but maintains place
        upper_byte_upper_nibble = get_upper_nibble(upper_byte)
        upper_byte_lower_nibble = get_lower_nibble(upper_byte)
        lower_byte_upper_nibble = get_upper_nibble(upper_byte)
        lower_byte_lower_nibble = get_lower_nibble(upper_byte)

        if upper_byte == 0x00:
            if lower_byte == 0xE0:
                self.wipe_screen()
            if lower_byte == 0xEE:
                self.stack_pop_address_to_pc()
            else:
                raise Exception("Invalid Instruction: SYS addr not implemented")
        if upper_byte_upper_nibble == 0x10:
            self.jump_to(get_lower_three_nibbles(upper_byte, lower_byte))
        if upper_byte_upper_nibble == 0x20:
            self.call(get_lower_three_nibbles(upper_byte, lower_byte))
        if upper_byte_upper_nibble == 0x30:
            self.skip_if_equal(upper_byte_lower_nibble, lower_byte)
        if upper_byte_upper_nibble == 0x40:
            self.skip_if_equal(upper_byte_lower_nibble, lower_byte)
        if upper_byte_upper_nibble == 0x50 and lower_byte_lower_nibble == 0x00:
            self.skip_if_v_equal(upper_byte_lower_nibble,  lower_byte_upper_nibble >> 4)
        if upper_byte_upper_nibble == 0x60:
            self.load_v(upper_byte_lower_nibble, lower_byte)
        if upper_byte_upper_nibble == 0x70:
            self.add_v_no_carry(upper_byte_lower_nibble, lower_byte)
        if upper_byte_upper_nibble == 0x80
            if lower_byte_lower_nibble == 0x00:
                self.load_v_to_v(upper_byte_lower_nibble, lower_byte_upper_nibble >> 4)
            if lower_byte_lower_nibble == 0x01:
                self.or_v_v(upper_byte_lower_nibble, lower_byte_upper_nibble >> 4)
            if lower_byte_lower_nibble == 0x02:
                self.and_v_v(upper_byte_lower_nibble, lower_byte_upper_nibble >> 4)
            if lower_byte_lower_nibble == 0x03:
                self.xor_v_v(upper_byte_lower_nibble, lower_byte_upper_nibble >> 4)

    def wipe_screen(self):  # CLS
        self.screen = [[0 for x in range(64)] for y in range(32)]  # 64x32 pixel screen use 0 or 1
        pass

    def stack_pop_address_to_pc(self):  # RET
        self.PC = self.stack[self.SP]
        self.SP -= 1

    def jump_to(self, address):  # JP addr
        self.PC = address

    def call(self, address):  # CALL addr
        self.SP += 1
        self.stack[self.SP] = self.PC
        self.PC = address

    def skip_if_equal(self, vx, lower_byte): #SE vx, byte
        if self.V[vx] == lower_byte:
            self.PC += 2

    def skip_if_not_equal(self, vx, lower_byte): #SE vx, byte
        if self.V[vx] != lower_byte:
            self.PC += 2

    def skip_if_v_equal(self, vx, vy): #SE Vx, Vy
        if self.V[vx] == self.V[vy]:
            self.PC += 2

    def load_v(self, vx, value): # LD Vx, byte
        self.V[vx] = value

    def add_v_no_carry(self, vx, lower_byte): #ADD Vx, byte
        self.V[vx] += lower_byte


    def load_v_to_v(self, vx, vy): # LD Vx, Vy
        self.V[vx] = self.V[vy]

    def or_v_v(self, vx, vy): #OR Vx, Vy
        self.V[vx] |= self.V[vy]

    def and_v_v(self, vx, vy): #OR Vx, Vy
        self.V[vx] &= self.V[vy]

    def xor_v_v(self, vx, vy):  # OR Vx, Vy
        self.V[vx] ^= self.V[vy]

    def add_v_v(self,vx,vy): # ADD Vx, Vy
        self.V[vx] += self.V[vy]
        if self.V[vx] > 0xFF:
            self.V[vx] &= 0xFF
            self.V[0xF] = 1  # Carry Bit

    def subtract_v_v(self, vx, vy):  # SUB Vx, Vy and SUBN Vx, Vy (Just switch parameters)
        if self.V[vx] < self.V[vy]:
            self.V[vx] -= self.V[vy]
            self.V[vx] &= 0xFF
            self.V[0xF] = 0  # borrow Bit
        else:
            self.V[vx] -= self.V[vy]
            self.V[0xF] = 1
    def shift_right(self, vx):  # SHR Vx {, Vy}
        self.V[0xF] = self.V[vx] %2;
        self.V[vx] >>= 1

    def shift_left(self, vx):  #SHL Vx {, Vy}
        self.V[0xF] = self.V[vx] & 0b1000_0000_0000_0000
        self.V[vx] <<= 1
        self.V[vx] &= 0xFFFF
    def notequal_v_v(self, vx, vy):  # SNE Vx, Vy
        if self.V[vx] != self.V[vy]:
            self.PC += 2