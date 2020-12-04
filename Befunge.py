from collections import deque
import random
from sys import *
from Direction import Direction
from Instructions import ProgramInstructions
import argparse
import logging


def open_program(name):
    try:
        with open(name, "r") as file:
            data = file.read()
            return data.split("\n")
    except FileNotFoundError:
        logging.warning(F"No such file: \'{name}\'")
        return None


class Pointer:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.value = None
        self.is_string = False
        self.executing = True
        self.stack = []
        self.commands = ProgramInstructions()
        self.commands.load_instructions()
        self.direction = Direction.Right
        self.map_width = 80
        self.map_height = 25
        self.map = [" "] * self.map_height
        for i in range(self.map_height):
            self.map[i] = [" "] * self.map_width

    def change_direction(self, direction):
        self.direction = direction

    def stop(self):
        self.executing = False

    def make_step(self):
        if self.direction == Direction.Right:
            self.x = (self.x + 1) if (self.x + 1) < self.map_width else 0
        elif self.direction == Direction.Left:
            self.x = (self.x - 1) if (self.x - 1) >= 0 else self.map_width - 1
        elif self.direction == Direction.Up:
            self.y = (self.y - 1) if (self.y - 1) >= 0 else self.map_height - 1
        elif self.direction == Direction.Down:
            self.y = (self.y + 1) if (self.y + 1) < self.map_height else 0

    def execute_program(self):
        while self.executing:
            self.value = self.map[self.y][self.x]
            if self.is_string and self.value != '"':
                self.stack.append(ord(self.value))
                self.make_step()
            else:
                if self.value in self.commands.instructions.keys():
                    self.commands.instructions[self.value](self)
                else:
                    self.make_step()
                    continue
                if self.value != "@":
                    self.make_step()

    def get_program(self, program):
        for i in range(len(program)):
            for j in range(len(program[i])):
                self.map[i][j] = program[i][j]


def print_information():
    print(F"Для запуска вашей программы введите в командную строку \n"
          F"python Befunge.py -r 'Название вашей программы'.bf")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--information',
                        help='Выводит информацию по использованию',
                        action='store_true')
    parser.add_argument('-r', '--run',
                        help='Запускает программу',
                        nargs=1)
    args = parser.parse_args()
    if args.information:
        print_information()
    program = open_program(args.run[0])
    if program:
        pointer = Pointer()
        pointer.get_program(program)
        pointer.execute_program()


if __name__ == "__main__":
    main()
