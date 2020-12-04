from Direction import Direction
from random import randint
import logging


class ProgramInstructions:
    def __init__(self):
        self.instructions = {}

    @staticmethod
    def duplicate_head_stack_value(pointer):
        try:
            head = pointer.stack.pop()
            pointer.stack.append(head)
            pointer.stack.append(head)
        except IndexError:
            logging.warning(F"The stack was empty when executing"
                            F" the command \'{pointer.value}\'"
                            F"with coordinates ({pointer.x}, {pointer.y})")
            pointer.stop()

    @staticmethod
    def delete_head_stack(pointer):
        try:
            pointer.stack.pop()
        except IndexError:
            logging.warning(F"The stack was empty when executing"
                            F" the command \'{pointer.value}\' "
                            F"with coordinates ({pointer.x}, {pointer.y})")
            pointer.stop()

    @staticmethod
    def swap_two_values_on_top_stack(pointer):
        try:
            first = pointer.stack.pop()
            second = pointer.stack.pop()
            pointer.stack.append(first)
            pointer.stack.append(second)
        except IndexError:
            logging.warning(F"The stack was empty when executing"
                            F" the command \'{pointer.value}\' "
                            F"with coordinates ({pointer.x}, {pointer.y})")
            pointer.stop()

    @staticmethod
    def change_string_mode(pointer):
        pointer.is_string = not pointer.is_string

    @staticmethod
    def execute_command_p(pointer):
        try:
            x = int(pointer.stack.pop())
            y = int(pointer.stack.pop())
            symbol = chr(pointer.stack.pop())
            pointer.map[x][y] = symbol
        except IndexError:
            pointer.stop()

    def load_constants(self):
        for number in "0123456789":
            self.instructions[number] = \
                lambda p, n=number: p.stack.append(int(n))

    @staticmethod
    def execute_command_g(pointer):
        try:
            x = int(pointer.stack.pop())
            y = int(pointer.stack.pop())
            try:
                symbol = pointer.map[x][y]
                code = ord(symbol)
                pointer.stack.append(code)
            except IndexError:
                pointer.stack.append(0)
        except IndexError:
            pointer.stop()

    @staticmethod
    def make_random_direction(pointer):
        random_number = randint(1, 4)
        pointer.direction = Direction(random_number)

    def execute_division(self, pointer):
        try:
            self.swap_two_values_on_top_stack(pointer)
            pointer.stack \
                .append(int(pointer.stack.pop()) / int(pointer.stack.pop()))
        except ZeroDivisionError:
            logging.warning(F"There was a division by zero when executing "
                            F"the command with "
                            F"coordinates ({pointer.x}, {pointer.y})")
            pointer.stop()

    def execute_mod(self, pointer):
        try:
            self.swap_two_values_on_top_stack(pointer)
            pointer.stack \
                .append(int(pointer.stack.pop()) % int(pointer.stack.pop()))
        except IndexError:
            logging.warning(F"The stack was empty when executing"
                            F" the command \'{pointer.value}\' "
                            F"with coordinates ({pointer.x}, {pointer.y})")
            pointer.stop()

    @staticmethod
    def execute_input_int(pointer):
        pointer.stack.append(int(input()))

    @staticmethod
    def execute_input_char(pointer):
        pointer.stack.append(ord(input()))

    def load_instructions(self):
        # change direction
        self.instructions['^'] = lambda p: p.change_direction(Direction.Up)
        self.instructions['>'] = lambda p: p.change_direction(Direction.Right)
        self.instructions['v'] = lambda p: p.change_direction(Direction.Down)
        self.instructions['<'] = lambda p: p.change_direction(Direction.Left)
        self.instructions["?"] = lambda p: self.make_random_direction(p)
        self.instructions["#"] = lambda p: p.make_step()
        self.instructions["@"] = lambda p: p.stop()

        # stack operations
        self.instructions[":"] = lambda p: \
            self.duplicate_head_stack_value(p)
        self.instructions["\\"] = lambda p: \
            self.swap_two_values_on_top_stack(p)
        self.instructions["$"] = lambda p: self.delete_head_stack(p)
        self.instructions['p'] = lambda p: self.execute_command_p(p)
        self.instructions['g'] = lambda p: self.execute_command_g(p)

        # conditional operation
        self.instructions["_"] = lambda p: \
            p.change_direction(Direction.Right) \
            if int(p.stack.pop()) == 0 \
            else p.change_direction(Direction.Left)
        self.instructions['|'] = lambda p: p.change_direction(Direction.Down) \
            if int(p.stack.pop()) == 0 \
            else p.change_direction(Direction.Up)

        # Numbers
        self.load_constants()
        self.instructions['"'] = lambda p: self.change_string_mode(p)

        # math operations
        self.instructions['*'] = lambda p: p.stack \
            .append(int(p.stack.pop()) * int(p.stack.pop()))
        self.instructions['/'] = lambda p: self.execute_division(p)
        self.instructions['+'] = lambda p: p.stack.append(
            int(p.stack.pop()) + int(p.stack.pop()))
        self.instructions['-'] = lambda p: p.stack.append(
            -int(p.stack.pop()) + int(p.stack.pop()))
        self.instructions['%'] = lambda p: self.execute_mod(p)

        # logic operations
        self.instructions["!"] = lambda p: p.stack \
            .append(1 if int(p.stack.pop()) == 0 else 0)
        self.instructions['`'] = lambda p: p.stack \
            .append(1 if int(p.stack.pop()) < int(p.stack.pop()) else 0)

        # input output operations
        self.instructions["&"] = lambda p: self.execute_input_int(p)
        self.instructions["~"] = lambda p: self.execute_input_char(p)
        self.instructions["."] = lambda p: print(p.stack.pop(), end="")
        self.instructions[","] = lambda p: print(chr(p.stack.pop()), end="")
