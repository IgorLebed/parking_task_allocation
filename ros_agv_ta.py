#!/usr/bin/env python3
from __future__ import division

from random import randint
import json
import math
import numpy as np
import hungary_alg as va

import rospy
from ros_common import RosCommon
from std_msgs.msg import Int64, Float64
from threading import Thread
import time
from munkres import DISALLOWED
PKG = 'parking_controller' #'talker'

class TaskAllocation(RosCommon):

	def setUp(self):

		super(TaskAllocation, self).setUp()
		
		self.parkin_place = Float64()	

		self.parking_place_pub = rospy.Publisher('/parking_place', Float64, queue_size=1) #TODO Make new name, new topic

		# send parkin_place in seperate thread to better prevent failsafe
		self.parking_place_thread = Thread(target=self.send_parking_place, args=())
		self.parking_place_thread.daemon =True
		self.parking_place_thread.start()

	def tearDown(self):

		super(TaskAllocation, self).tearDown()

	def send_parking_place(self):

		rate = rospy.Rate(10)  # Hz
		while not rospy.is_shutdown():
			self.parking_place_pub.publish(self.parkin_place)
			try: 
				rate.sleep()
			except rospy.ROSInterruptException:
				pass

	def read_from_json(self):
		"""Read json file (no,x y, ori)"""

		#for 'while' 
		reading_json = True
		num_select = 1
		#json open
		try:
			f = open(self.path_to_json)
			data = json.load(f)
			json_place = []
			parking_coordinates = []
			for i in data:
				json_place.append(i)

				#rospy.loginfo("This is "+ i + " parking place:") #
				for j in data[json_place[-1]]:
					j
					#rospy.loginfo("Parking coordinates: ", j)
			while reading_json:
				parking_coordinates.append(data['%s' % num_select])
				num_select += 1
				count_place = int(len(json_place))
				if (num_select > count_place):
					reading_json = False
			f.close()
			return parking_coordinates, json_place
		except:
			rospy.logerr("Json not found in method!")
			exit(0)

	def path_length(self, x1, y1, x2, y2):
		"""Path length from start to park place """

		X = x2 - x1
		Y = y2 - y1
		dA = math.sqrt(X ** 2 + Y ** 2)
		#rospy.loginfo("This is lenght: %s" % dA)
		return dA

	def calculat_lenght(self, start_coor_x, start_coor_y):
		"""This function make for calculate lenght from start to for each parking place from use json file"""

		parkin_length = []
		length_calculation = True
		count_parkin_coor = 0
		T = []
		while length_calculation:
			end_coor_x = self.read_from_json()[0][count_parkin_coor][0]
			end_coor_y = self.read_from_json()[0][count_parkin_coor][1]
			#path_length(start_coor_x, start_coor_y, end_coor_x, end_coor_y)
			if(count_parkin_coor in self.unavailable_places):
				#rospy.loginfo("This is unavailable place", unavailable_places)
				#rospy.loginfo("Testing!!!!")

				#parkin_length.append(float(self.path_length(0, 0, 9999, 9999)))
				parkin_length.append(DISALLOWED)
			else:
				parkin_length.append(float(self.path_length(start_coor_x, start_coor_y, end_coor_x, end_coor_y)))

			count_parkin_coor += 1
			if (count_parkin_coor == (int(len(self.read_from_json()[1])))):
				length_calculation = False
		for i in range(int(len(self.read_from_json()[1]))):# mistake
			try:	
				T_elem = self.V_speed / parkin_length[i]
				x = round(T_elem, 5)
				#rospy.logerr(T_elem)
				T.append(x)
			except:
				T_elem = DISALLOWED
				#rospy.logerr(T_elem)
				T.append(T_elem)
		return T #parkin_length

	# def d_time(self):
	# 	""" TODO """

	# 	dist = self.calculat_lenght(self.start_x, self.start_y)
	# 	T = []
		
	# 	for i in range(int(len(self.read_from_json()[1]))):# mistake		
	# 		T_elem = self.V_speed / dist[i]
	# 		rospy.logerr(T_elem)
	# 		T.append(T_elem)
	# 	return T

	def matrix_gen(self, c_size, r_size):
		"""This function need to generate zero matrix 'n' on 'n' or 'n' on 'm'"""

		x = []
		y = []
		for j in range(0, c_size):
			y.append(0)
		for i in range(0, r_size):
			x.append(y)
		zero_matrix = np.matrix(x)
		return zero_matrix

	def matrix_convert(self, x):
		"""This function make from list view to normal view (for Hungary class)"""

		#matrix_task = np.matrix(x)
		matrix_task = []
		matrix_task.append(x)
		return matrix_task

	def hungary_class(self, task_matrix, class_mode, wait):
		"""This function ......"""#TODO need description

		result_by_hungary = va.TaskAssignment(task_matrix, class_mode, wait)
		#rospy.loginfo('cost matrix = ', '\n', task_matrix)
		#rospy.loginfo ('Assign a task to all placement methods :')
		#rospy.loginfo ('Assigning a task using the Hungarian method :')
		#rospy.loginfo('min cost = ', result_by_hungary.min_cost)
		#rospy.loginfo('best solution = ', result_by_hungary.best_solution)
		if class_mode == 'Hungary_min':
			return result_by_hungary.best_min_solution
		if class_mode == 'Hungary_max':
			return result_by_hungary.best_max_solution
		else:
			rospy.logerr("Unknown Hungary mode")

	def hungary_main(self, class_mode, wait):
		"""This function .........."""#TODO need description

		task_matrix = self.matrix_convert(self.calculat_lenght(self.start_x, self.start_y))


		rospy.logerr(task_matrix)
		hungary_result = self.hungary_class(task_matrix, class_mode, wait)
		return hungary_result

	# def test_add(self, total_parking_place_):
	# 	self.total_parking_place = total_parking_place_

	def reset_place(self, concerned_list, place_number):
		""" Add all place in initial list """

		for place in range(0, place_number):
			concerned_list.append(place)

	def make_a_place_available(self, place_number):
		"""Add a place in available list"""

		self.unavailable_places.remove(place_number)
		self.available_places.append(place_number)
		self.available_places.sort()
		self.unavailable_places.sort()
		rospy.loginfo(f'Place n°{place_number} is now available.')

	def make_a_place_unavailable(self, place_number):
		"""Remove a place in available list"""

		self.unavailable_places.append(place_number)
		self.available_places.remove(place_number) 
		self.available_places.sort()
		self.unavailable_places.sort()
		rospy.loginfo(f'Place n°{place_number} is now unavailable.')

	def know_available_places(self):
		"""Display available places"""

		if len(self.available_places) > 1:
			rospy.loginfo(f'Availables places are: {self.available_places}.')
		elif len(self.available_places) == 1:
			rospy.loginfo(f'Only place n°{self.available_places} is available.')
		else:
			rospy.loginfo('All places are unavailables.')

	# def choose_available_place():
	# 	"""Choose an available place and return it if it's available"""

	# 	choice = randint(1, total_parking_place)
	# 	while choice in unavailable_places:
	# 		choice = randint(1, total_parking_place)

	# 	return choice

	def choose_available_place(self, class_mode, wait):
		"""Choose an available place and return it if it's available"""

		best_res = self.hungary_main(class_mode, wait)
		rospy.logerr("BEST_RES")
		rospy.logerr(best_res)
		rospy.loginfo(self.total_parking_place)

		for i in range(self.total_parking_place):
			if self.calculat_lenght(self.start_x, self.start_y)[i] == best_res[0]:
				choice = i 
				while choice in self.unavailable_places:
					choice = randint(1, self.total_parking_place)
		try:
			rospy.loginfo("avalable place found!")
			return choice
		except:
			rospy.loginfo("avalable place not found!")

		
	def add_a_car(self, car_mark, car_model, car_color, class_mode, wait):
		"""Register a car with it's caracteristics in parked car list"""

		the_car = [car_color, car_mark, car_model]
		choosen_number = self.choose_available_place(class_mode, wait)
		self.parked_car_list.append(the_car)

		# link parked car to place where driver parked
		self.relation_car_parking_place[choosen_number] = the_car

		rospy.loginfo(f'{car_color} {car_mark} {car_model} added to parking at place n°{choosen_number}')

		self.parkin_place.data = choosen_number

		self.make_a_place_unavailable(choosen_number)

	def stop_input(self):

		while (self.global_stop_x == True):
			print(self.car_input_menu.data)

	def car_model_input(self, class_mode, wait):
		# Ask car carasteristics to user
		car_ma = input(rospy.loginfo('Enter the car mark: '))
		car_mo = input(rospy.loginfo('Enter the car model: '))
		car_c = input(rospy.loginfo('Enter the car color: '))

		# Avoid that user inputs not contain car caracteristics
		while len(car_ma) <= 0 or len(car_mo) <= 0 or len(car_c) <= 0:

			rospy.loginfo('\nMake sure to fill in all the fields.')
			car_ma = input(rospy.loginfo('Enter the car mark: '))
			car_mo = input(rospy.loginfo('Enter the car model: '))
			car_c = input(rospy.loginfo('Enter the car color: ') )

		# If all is good admit car to parking and count it
		self.add_a_car(car_ma, car_mo, car_c, class_mode, wait)
		self.parked_car_number += 1
		correct_choice = False
		return correct_choice


	def test_ta_(self):

		self.log_topic_vars()

		try:
			self.total_parking_place = int(len(self.read_from_json()[1]))
		except:
			rospy.loginfo("Json not found")

		self.reset_place(self.available_places, self.total_parking_place)

		rospy.loginfo('******************************')
		rospy.loginfo('Welcome to Autonomous Parking Station.\n')
		
		# Initialize a boolean which indicate if application continue or stop
		continue_game = True
		while continue_game:
			# program interact with parking guard and display choices
			#rospy.loginfo("Unavailable place: ", int(len(unavailable_places)))
			correct_choice = False
			user_choice = ''

			#self.car_input_menu = RosCommon().car_input_menu.data
			#rospy.loginfo(self.car_input_menu_callback) 
			rospy.loginfo('What do you want to do?\n\
				Choose wright number:\n\
				1- Leave the car in the parking lot\n\
				2- Pick up car from parking\n\
				3- Availables places list\n\
					')
			user_choice = 0		
			while not correct_choice:
				time.sleep(3)	
				
				user_choice = self.car_input_menu.data
			
				# Let's be sure that user choose a integer, and his choice is in [1:3]
				try:
					user_choice = int(user_choice)
					correct_choice = True
					
					if user_choice < 1 or user_choice > 3:
						correct_choice = False
						rospy.loginfo('Make sure that you choose a number between 1 and 3')
					else:
						correct_choice = True
				except ValueError:
					rospy.loginfo('Sorry, you must choose a number')
					correct_choice = False
			
			if user_choice == 1: # option 1: leave the car
				# Ask time to parking 

				correct_choice = False
				time_parking = 0
				while not correct_choice:
					time.sleep(3)	
				
					time_parking = input(rospy.loginfo('Enter the time parking'))
			
					# Let's be sure that user choose a integer, and his choice is in [1:3]
					try:
						time_parking = int(time_parking)
						correct_choice = True
						
						if user_choice < 1 or user_choice > 24:
							correct_choice = False
							rospy.loginfo('Make sure that you choose a number between 1 and 24')
						else:
							correct_choice = True
					except ValueError:
						rospy.loginfo('Sorry, you must choose a number')
						correct_choice = False
						
				rospy.logerr(time_parking)
				if time_parking >= 1 and time_parking <= 24: 

					if time_parking >= 1 and time_parking < 6:
						value = "quick"
						rospy.logerr(value)
						self.car_model_input('Hungary_min', 'quick')
					if time_parking >= 6 and time_parking < 12:
						value = "soon"
						rospy.logerr(value)
						self.car_model_input('Hungary_min', 'soon')
					if time_parking >= 12 and time_parking < 18:
						value = "not soon"
						rospy.logerr(value)
						self.car_model_input('Hungary_max', 'not soon')
					if time_parking >= 18 and time_parking <= 24:
						value = "long wait"
						rospy.logerr(value)
						self.car_model_input('Hungary_max', 'long wait')

					

			elif user_choice == 2: # option 2: remove a car
				rospy.loginfo('List of parked cars:')
				# Display parked cars list
				for place, car in self.relation_car_parking_place.items():
					rospy.loginfo(f'place n°{place}: {car}')

				'''here, we can add a try...except statement to 
				be sure that user enter correct answer
				'''
				place_wanted = int(input('Choose place you want to remove: '))

				place_of_removed_car = 0
				if place_wanted in self.unavailable_places:
					for place, car in self.relation_car_parking_place.items():
						if place == place_wanted:
							self.parked_car_list.remove(car)
							place_of_removed_car = place
							esthetic_phrase = ' '.join(car) # Transform list in string
							rospy.loginfo(f'{esthetic_phrase} go out.')
					del(self.relation_car_parking_place[place_of_removed_car])
					self.make_a_place_available(place_wanted)

				else: # tell user that place number he choose is already available
					rospy.loginfo(f'Sorry, {place_wanted} is already available.')

			else: # option 3: display available places
				self.know_available_places()
				
			# Ask if parking guard want to continue the program
			exit_question = 'y' #input('Do you want to continue the program? (Y/n)')

			if exit_question.lower() == 'n':
				continue_game = False
		rospy.loginfo('The end!')


		if self.parked_car_number == 0:
			rospy.loginfo(f'You didn\'t parked a car.')
		elif self.parked_car_number == 1:
			rospy.loginfo(f'You\'ve parked only {self.parked_car_number} car.')
		else:
			rospy.loginfo(f'You\'ve parked {self.parked_car_number} cars')	


if __name__ == '__main__':
	import rostest
	rospy.init_node('ta_node', anonymous=True)

	rostest.rosrun(PKG, 'main_ta', TaskAllocation)