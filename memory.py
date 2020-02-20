class Memory:
    def __init__(self):
        self.value = 0x00

    def set(self, value):
        self.value = value

    def get(self):
        return self.value

