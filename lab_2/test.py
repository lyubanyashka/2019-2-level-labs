# pylint: skip-file
"""
Checks the second lab. Part about the path finding
"""

import unittest
from unittest.mock import patch

from lab_2 import main


class PrintPathTest(unittest.TestCase):
    """
    Tests path finding
    """

    def test_find_pathl_again(self):
        """
        Ideal scenario # 2
        """

        original_word = 'cat'
        target_word = 'doge'
        add_weight = 1
        remove_weight = 2
        substitute_weight = 3
        edit_matrix = tuple(main.generate_edit_matrix(len(original_word) + 1, len(target_word) + 1))
        edit_matrix = tuple(main.initialize_edit_matrix(edit_matrix, add_weight, remove_weight))
        edit_matrix = main.fill_edit_matrix(edit_matrix, add_weight, remove_weight, substitute_weight, original_word, target_word)
        print("best path cost " + str(edit_matrix[len(original_word)][len(target_word)]))
        main.print_path(edit_matrix, original_word, target_word, add_weight, remove_weight, substitute_weight)

