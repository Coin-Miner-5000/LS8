"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0  # Program Counter

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8 - decimal value is 130
            0b00000000,  # at reg[0]
            0b00001000,  # store the value 8
            0b01000111,  # PRN R0 - decimal value is 71
            0b00000000,  # print reg[0]
            0b00000001,  # HLT - decimal value is 1
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        # MAR = Memory Address Register, contains the address that is being read or written to
        # MDR =  Memory Data Register, contains the data that was read or the data to write
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def HLT(self):
        sys.exit(0)

    def LDI(self, reg_add, value):
        self.reg[reg_add] = value

    def PRN(self, reg_add):
        return self.reg[reg_add]

    def run(self):
        """Run the CPU."""
        # load the program
        self.load()

        while True:
            # Instruction Register, contains a copy of the currently executing instruction
            IR = self.ram[self.pc]
            if IR == 130:
                address = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                # store the data
                self.LDI(address, value)
                # increment the PC by 3 to skip the arguments
                self.pc += 3
            elif IR == 71:
                data = self.ram[self.pc + 1]
                # print the data
                print(self.PRN(data))
                # increment the PC by 2 to skip the argument
                self.pc += 2
            elif IR == 1:
                self.HLT()
            else:
                print(f"I did not understand that command: {IR}")
                sys.exit(1)
