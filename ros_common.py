#!/usr/bin/env python3
from __future__ import division

import unittest
import rospy
from std_msgs.msg import Int64
from pathlib import Path


class RosCommon(unittest.TestCase):

    def __init__(self, *args):

        super(RosCommon, self).__init__(*args)
        self.car_input_menu = Int64()

        self.total_parking_place = 12           # we suppose that we've 12 places in parking
        self.available_places = []              # register all availables places
        self.unavailable_places = []            # register all unavailables places
        self.parked_car_list = []               # register all parked cars at the moment
        self.relation_car_parking_place = {}
        self.parked_car_number = 0              # count all parked cars

        self.start_x = 0
        self.start_y = 0

        self.global_stop_x = True
        self.V_speed = 0.5                      # m\s

        home = str(Path.home())
        self.path_to_json = home + '/parking/src/parking_system/parking_controller/task_allocation/json/parking_slots.json'

    def setUp(self):

        self.sub_topics_ready = {
            key: False
            for key in [
                'car_menu'
            ]
        }
        #------------------------------------Tipic_List-----------------------------------------------------------------
        self.car_input_menu_sub = rospy.Subscriber('/car_input_menu', Int64, self.car_input_menu_callback)
        #self.car_input_menu_sub = 3

    def tearDown(self):

        self.log_topic_vars()

    def car_input_menu_callback(self, data):

        self.car_input_menu = data
        #rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data)

        if not self.sub_topics_ready['car_menu']:
            self.sub_topics_ready['car_menu'] = True

    def log_topic_vars(self):
        """log the state of topic variables"""

        rospy.loginfo('========================')
        rospy.loginfo('===== topic values =====')
        rospy.loginfo('========================')
        rospy.loginfo('car_input_menu:{}\n'.format(self.car_input_menu))
        rospy.loginfo('========================')