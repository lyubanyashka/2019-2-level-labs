import unittest
from unittest.mock import patch

from lab_2 import main
def test_find_distance_ideal_again(self):
        """
        Ideal scenario # 2
        """
        # arrange
        original_word = 'length'
        target_word = 'kitchen'
        add_weight = 1
        remove_weight = 1
        substitute_weight = 2
        expected_result = 9
        # act
        actual_distance = main.find_distance(original_word, target_word, add_weight, remove_weight, substitute_weight)
        # assert
        self.assertEqual(expected_result, actual_distance)
        self.save_to_csv()
