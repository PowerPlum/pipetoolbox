#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 17:20:38 2017

@author: christopherbridge
"""

import numpy as np

from .materials import Materials

class Pipe(object):
    """
    Pipe object 
    Store the outer diameter, wall thickness and material properties 
    determine all other properties
    
    Note, units are SI. Options for Imperial units may follow
    
    """
    def __init__(self, outer_diameter=-1, wall_thickness=-1, material='default'):
        """
        Initialise the pipe with outer diameter, wall thickness and a 
        default material 
        """
        self._diameter_outer = outer_diameter
        self._wall_thickness = wall_thickness
        self._material_name = material
        #        
        self._materials = Materials()
        #
        self._coatings_material = 'none'
        self._coatings_thickness = 0.0
        self._coatings_density = 0.0
        #
        self._internal_fluid_name = 'water'
        self._internal_fluid_density = 1000.0
        #
        self._external_fluid_name = 'sea water'
        self._external_fluid_density = 1025.0
        #
        self._gravity = 9.81
        #
        self._length = 1.0
        
    def od(self, od):
        """Assign the outer diameter"""
        self._diameter_outer = od
        
    def t(self, t):
        """Assign the wall thickness"""
        self._wall_thickness = t
        
    def coatings(self, name, thickness_mm, density_kgm3):
        """Set key properties for the coatings on the pipe"""
        self._coatings_material = name
        self._coatings_thickness = thickness_mm
        self._coatings_density = density_kgm3
        
    def internal_fluid(self, name, density_kgm3):
        """Set the intenral fluids"""
        self._internal_fluid_name = name
        self._internal_fluid_density = density_kgm3

    def external_fluid(self, name, density_kgm3):
        """Set the intenral fluids"""
        self._external_fluid_name = name
        self._external_fluid_density = density_kgm3
        
    def material(self, material_name):
        """Set the material from the database"""
        self._materials.get_material(material_name)
        
    def length(self, length=None):
        """Set or return the length"""
        if length != None:
            self._length = length
        else:
            return self._length
        
    # -------------------------------------------------------------------------
    # Determine the properties
    # -------------------------------------------------------------------------
    def geometric_properties(self):
        """Calculate the goemetric properties of the pipe from wall thickness
        and outer diameter
        """

    def radius_inner(self):
        return 0.5 * (self._diameter_outer - 2.0 * self._wall_thickness)
    
    def radius_outer(self):
        return 0.5 * self._diameter_outer
    
    def radius_external(self):
        return 0.5 * (self._diameter_outer + 2.0 * self._coatings_thickness)
        
    # -----------------    
    def diameter_inner(self):
        return self._diameter_outer - 2.0 * self._wall_thickness
    
    def diameter_outer(self):
        return self._diameter_outer
    
    def diameter_external(self):
        return self._diameter_outer + 2.0 * self._coatings_thickness
    
    # -----------------    
    def area_internal(self):
        return 0.25 * np.pi * self.diameter_inner()**2.0
    
    def area_steel(self):
        return self.area_outer() - self.area_internal()
    
    def area_outer(self):
        return 0.25 * np.pi * self.diameter_outer()**2.0
    
    def area_coatings(self):
        return self.area_external() - self.area_outer()

    def area_external(self):
        return 0.25 * np.pi * self.diameter_external()**2.0
        
    # -----------------    
    def second_moment(self):
        return 0.015625 * np.pi * (self.diameter_outer()**4.0 - self.diameter_inner()**4.0)
    
    def radius_of_gyration(self):
        return np.sqrt(self.second_moment() / self.area_steel())       

    # -----------------  
    def mass_fluids(self):
        return self.area_internal() * self._internal_fluid_density
    
    def mass_steel(self):
        """Calculate the mass per unit length of the pipe"""
        return self.area_steel() * self._materials.density()
    
    def mass_coatings(self):
        return self.area_coatings() * self._coatings_density
    
    def mass_total(self):
        return self.mass_fluids() + self.mass_steel() + self.mass_coatings()
    
    def mass_buoyant(self):
        return self.mass_total() - self.area_external * self._external_fluid_density
    
    # -----------------  
    def tension_limit(self, safety_factor=1.0):
        return safety_factor * self.area_steel() * self._materials.yield_stress()
    
    def bending_limit(self, safety_factor=1.0):
        return safety_factor * self.second_moment() * self._materials.yield_stress() / self.radius_outer()
    
    def pressure_internal_limit(self, safety_factor=1.0):
        return safety_factor * 2.0 * self._wall_thickness * self._materials.yield_stress() / self._diameter_outer
    
    # -----------------  
    def euler_load(self, end_conditions='fixed'):
        """Return the Eular buckling load for a given length"""
        if end_conditions == 'fix-fix':
            factor = 4.0
        elif end_conditions == 'pin-fix':
            factor = 2.045
        elif end_conditions == 'pin-pin':
            factor = 1.0
        elif end_conditions == 'free-fix':
            factor = 0.25
        else:
            factor = 1.0
        #
        return factor * np.pi**2.0 * self._materials.youngs() * self.second_moment() / self._length**2.0        
        
    # -------------------------------------------------------------------------
    # Display for information
    # -------------------------------------------------------------------------
    def display(self, SI=False):
        """Print a copy of the pipe details to the screen for information"""
        print("Pipe Details")
        
        if SI:
            print("Outer Diameter {:6.4g} m and wall thickness {:6.4g} m".format(self._diameter_outer, self._wall_thickness))
        else:
            print("Outer Diameter {:6.4g} mm and wall thickness {:6.4g} mm".format(1e3 * self._diameter_outer, 1e3 * self._wall_thickness))

        print("Material {}".format(self._materials.name()))
        #
        # Geometry
        print(" ")
        #
        #
        if SI:
            print("Tension limit {:6g} N".format(self.tension_limit()))
            print("Bending limit {:6g} N".format(self.bending_limit()))
            print("Burst limit {:6g} Pa".format(self.pressure_internal_limit()))
        else:
            print("Tension limit {:6g} kN".format(1e-3 * self.tension_limit()))
            print("Bending limit {:6g} kN".format(1e-3 * self.bending_limit()))
            print("Burst limit {:6g} MPa".format(1e-6 * self.pressure_internal_limit()))
        
        