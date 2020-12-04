import unittest
from Befunge import Pointer
from Direction import Direction


class Test(unittest.TestCase):

    def setUp(self) -> None:
        self.pointer = Pointer()

    def get_and_execute_program_and_print_map(self, program):
        self.pointer.get_program(program)
        self.pointer.execute_program()

    def test_move_one_step_right(self):
        program = [">@"]
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.x, 1)

    def test_jump_operation(self):
        program = ['>#@<']
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.x, 2)
        self.setUp()

    def test_move_step_down(self):
        program = ['>v', ' @']
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.x, 1)
        self.assertEqual(self.pointer.y, 1)

    def test_move_step_left_out(self):
        self.pointer.change_direction(Direction.Left)
        self.pointer.make_step()
        self.assertEqual(self.pointer.x, 79)
        self.assertEqual(self.pointer.y, 0)

    def test_move_step_up_out(self):
        self.pointer.change_direction(Direction.Up)
        self.pointer.make_step()
        self.assertEqual(self.pointer.x, 0)
        self.assertEqual(self.pointer.y, 24)

    def test_move_step_right_out(self):
        for i in range(self.pointer.map_width):
            self.pointer.make_step()
        self.assertEqual(self.pointer.x, 0)
        self.assertEqual(self.pointer.y, 0)

    def test_move_step_down_out(self):
        self.pointer.change_direction(Direction.Down)
        for i in range(self.pointer.map_height):
            self.pointer.make_step()
        self.assertEqual(self.pointer.x, 0)
        self.assertEqual(self.pointer.y, 0)

    def test_duplicate_head_stack(self):
        program = ["5:@"]
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.stack, [5, 5])
        self.setUp()

    def test_duplicate_head_without_head(self):
        program = [":@"]
        self.get_and_execute_program_and_print_map(program)
        self.assertFalse(self.pointer.executing)
        self.setUp()

    def test_swap_two_on_top(self):
        program = ["56\\@"]
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.stack, [6, 5])

    def test_swap_two_on_top_without_values(self):
        program = ["\\@"]
        self.get_and_execute_program_and_print_map(program)
        self.assertFalse(self.pointer.executing)

    def test_delete_head_stack(self):
        program = ["5$@"]
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.stack, [])
        self.setUp()

    def test_execute_command_p(self):
        program = ["66*00p@"]
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.map[0][0], "$")

    def test_execute_command_p_with_over_coordinates(self):
        program = ["699*55*p@"]
        self.get_and_execute_program_and_print_map(program)
        self.assertFalse(self.pointer.executing)

    def test_execute_command_g_with_over_coordinates(self):
        program = ["99*55*g@"]
        self.get_and_execute_program_and_print_map(program)
        self.assertFalse(self.pointer.executing)

    def test_execute_command_g(self):
        program = ["F00g@"]
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.stack, [70])
        self.setUp()

    def test_check_stack_after_output(self):
        program = ["44*2*,@"]
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.stack, [])

    def test_execute_horizontal_conditional_statement(self):
        program = ["0_@"]
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.direction, Direction.Right)

    def test_no_execute_horizontal_conditional_statement(self):
        program = ["1 v", "@ _ @"]
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.direction, Direction.Left)
        self.assertEqual(self.pointer.x, 0)
        self.assertEqual(self.pointer.y, 1)

    def test_execute_vertical_conditional_statement(self):
        program = ["0|", " @"]
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.x, 1)
        self.assertEqual(self.pointer.y, 1)

    def test_no_execute_vertical_conditional_statement(self):
        program = ["1#@v", "  |<"]
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.x, 2)
        self.assertEqual(self.pointer.y, 0)
        self.setUp()

    def test_operation_with_number(self):
        program = ["123@"]
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.stack, [1, 2, 3])

    def test_change_string_mode(self):
        program = ['"AAA"@']
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.stack, [65, 65, 65])

    def test_addition(self):
        program = ["42+@"]
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.stack, [6])

    def test_division(self):
        program = ["42/@"]
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.stack, [2])

    def test_multiply(self):
        program = ["42*@"]
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.stack, [8])

    def test_subtraction(self):
        program = ["42-@"]
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.stack, [2])

    def test_mod(self):
        program = ["42%@"]
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.stack, [0])

    def test_zero_division(self):
        program = ["40/@"]
        self.get_and_execute_program_and_print_map(program)
        self.assertFalse(self.pointer.executing)

    def test_logic_operation(self):
        program = ["0!@"]
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.stack, [1])
        self.setUp()

        program = ["2!@"]
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.stack, [0])
        self.setUp()

        program = ["01`@"]
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.stack, [0])
        self.setUp()

        program = ["10`@"]
        self.get_and_execute_program_and_print_map(program)
        self.assertEqual(self.pointer.stack, [1])


if __name__ == '__main__':
    unittest.main()
