# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 14:08:19 2022

@author: hp
"""


class Specie:
    def __init__(self, species_id, member_count, allowed_offspring_count):
        self.species_id = species_id
        self.member_count = member_count
        self.allowed_offspring_count = allowed_offspring_count
        self.average_fitness = 0
        self.average_adjusted_fitness = 0
        self.total_fitness = 0
        self.generations_since_improved = 0