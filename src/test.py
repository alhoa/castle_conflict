#!/usr/bin/python3
import unittest

from exceptions import *
from saveparser import SaveParser
from algorithms import *

class TestAlgs(unittest.TestCase):

	def test_x_constant(self):
		self.assertEqual(bressenham(3,1,3,5), [(3,1), (3,2), (3,3), (3,4), (3,5)])

	def test_y_constant(self):
		self.assertEqual(bressenham(1,3,5,3), [(1,3), (2,3), (3,3), (4,3), (5,3)])

	#Tests for dx,dy >0 
	def test_dx_larger_both_pos(self):
		self.assertEqual(bressenham(1,1,5,4), [(1,1), (2,2), (3,2), (4,3), (5,4)])

	def test_dy_larger_both_pos(self):
		self.assertEqual(bressenham(1,1,4,5), [(1,1), (2,2), (2,3), (3,4), (4,5)])

	
	#Tests for dx,dy <0 
	def test_dx_larger_both_neg(self):
		#The return order will always have increasing x
		self.assertEqual(bressenham(5,4,1,1), [(1,1), (2,2), (3,2), (4,3), (5,4)])

	def test_dy_larger_both_neg(self):
		#The return order will always have increasing x
		self.assertEqual(bressenham(4,5,1,1), [(1,1), (2,2), (2,3), (3,4), (4,5)])


	#Tests for dx >0,dy <0 
	def test_dx_larger_and_pos(self):
		#The return order will always have increasing x
		self.assertEqual(bressenham(1,4,5,1), [(1,4), (2,3), (3,3), (4,2), (5,1)])

	def test_dy_larger_and_neg(self):
		#The return order will always have increasing y
		self.assertEqual(bressenham(1,5,4,1), [(4,1), (3,2), (3,3), (2,4), (1,5)])


	#Tests for dx < 0, dy >0 
	def test_dx_larger_and_neg(self):
		#The return order will always have increasing x
		self.assertEqual(bressenham(5,1,1,4), [(1,4), (2,3), (3,3), (4,2), (5,1)])

	def test_dy_larger_and_pos(self):
		#The return order will always have increasing y
		self.assertEqual(bressenham(4,1,1,5), [(4,1), (3,2), (3,3), (2,4), (1,5)])


	#Test that rounding works on edge case
	def test_05_edge_case(self):
		self.assertEqual(bressenham(1,2,5,4), [(1,2), (2,2), (3,3), (4,3), (5,4)])


	def test_correct_save(self):
		path = "saves/unit_tests/beach_save.txt"
		parser = SaveParser()
		save = open(path)
		check = None

		try:
			game = parser.generate_map(save)
		except CorruptedSaveError as msg:
			self.fail("Correct save caued an error")
		finally:
			save.close()

		#Compare map name
		self.assertEqual(game.get_mapname(), "beach")

		#Compare player list
		char_names = []

		chars = game.get_characters()
		for char in chars:
			char_names.append(char.get_name())

		#Names should be in order of initiative
		self.assertEqual(char_names, ["Skeleton", "Mikko", "Makke", "Shade" ,"Spider"])

	#Save parser tests
	def test_missing_header(self):
		path = "saves/unit_tests/missing_header.txt"
		parser = SaveParser()
		save = open(path)
		check = None


		try:
			game = parser.generate_map(save)
		except CorruptedSaveError as msg:
			check = msg
		finally:
			save.close()

		self.assertNotEqual(None, check, "Missing header didn't cause an exception")


	def test_missing_char_info(self):
		path = "saves/unit_tests/missing_char_info.txt"
		parser = SaveParser()
		save = open(path)
		check = None

		try:
			game = parser.generate_map(save)
		except CorruptedSaveError as msg:
			check = msg
		finally:
			save.close()

		self.assertNotEqual(None, check, "Missing char info didn't cause an exception")

	def test_missing_map(self):
		path = "saves/unit_tests/missing_map.txt"
		parser = SaveParser()
		save = open(path)
		check = None

		try:
			game = parser.generate_map(save)
		except CorruptedSaveError as msg:
			check = msg
		finally:
			save.close()

		self.assertNotEqual(None, check, "Missing map info didn't cause an exception")


if __name__ == '__main__':
	unittest.main()