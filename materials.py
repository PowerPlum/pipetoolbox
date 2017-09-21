#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 14:37:53 2017

@author: christopherbridge
"""

import pickle

def materials_default():
    """
    Return a dictionary containing default materials properties
        Name:   yeild_stress,      Pa
                ultimate_stress,   Pa
                possions_ratio,    -
                youngs_modulus,    Pa
                density,           kg/m^3
                thermal_expansion, -
                notes
    """
    return {
        'default' :
            {'yield_stress': 358.5e6,
             'ultimate_stress': 394.3e6,
             'possions_ratio': 0.3,
             'youngs_modulus': 205.0e9,
             'density': 7850.0,
             'thermal_expansion': 1.2e-6,
             'notes': 'Default is Steel x52'
             },
        'steel x52' :
            {'yield_stress': 358.5e6,
             'ultimate_stress': 394.3e6,
             'possions_ratio': 0.3,
             'youngs_modulus': 205.0e9,
             'density': 7850.0,
             'thermal_expansion': 1.20e-6
             },
        'stainless steel' :
            {'yield_stress': 290.0e6,
             'ultimate_stress': 495.0e6,
             'possions_ratio': 0.3,
             'youngs_modulus': 193e9,
             'density': 8030.0,
             'thermal_expansion': 1.2e-6
             },
	}
#
#
#
class Materials(object):
    """
    Material object
    """
    def __init__(self, material_name='default'):
        #
        # Set up the default variables
        self._materials_data = materials_default()
        self._name = material_name
        self._yield = 0.0
        self._ultimate = 0.0
        self._possions = 0.0
        self._youngs = 0.0
        self._density = 0.0
        self._thermal_expansion = 0.0
        #
        # Read from the materials data
        self.material(material_name)
        #
        
    def name(self):
        """Return the material name"""
        return self._name
    
    def yield_stress(self):
        """Return the yield stress"""
        return self._yield
    
    def ultimate_stress(self):
        """Return the ultimate stress"""
        return self._ultimate
    
    def possions(self):
        """Return the Possions Ratio"""
        return self._possions
    
    def youngs(self):
        """Return the Youngs Modulus"""
        return self._youngs
    
    def density(self):
        """Return the density of the material"""
        return self._density
    
    def thermalexpansion(self):
        """Return the thermal expansion of the material"""
        return self._thermal_expansion
    
    def addmat(self, name, yield_stress_Pa, ultimate_Pa, youngs_Pa, possions, density_kgm3, thermal):
        """Add a meterial to the database and set it as the current material"""
        self.database_add(name, yield_stress_Pa, ultimate_Pa, youngs_Pa, possions, density_kgm3, thermal)
        self.material(name)
            
    # -------------------------------------------------------------------------
    # Database functions
    # -------------------------------------------------------------------------
    def material(self, material_name='default'):
        """Get the meterial from the materials database"""
        material_data = self._materials_data.get(material_name)
        #
        if not material_data:
            return False
        else:   
            self._name = material_name
            self._yield = material_data.get('yield_stress')
            self._ultimate = material_data.get('ultimate_stress')
            self._possions = material_data.get('possions_ratio')
            self._youngs = material_data.get('youngs_modulus')
            self._density = material_data.get('density')
            self._thermal_expansion = material_data.get('thermal_expansion')
            return True
    
    def __repr__(self):
        return "Material {}".format(self._name) \
            + " Yield {:5.1f} MPa".format(self._yeild)
        #, Ultimate {:5.1f} MPa, Youngs Modulus {:5.1f} GPa, Possions Ratio {:5.3f}, Thermal Expansion {:5.2e}".format(self.MaterialName, 0.000001 * self.Data['yield'], 0.000001 * self.Data['ultimate'], 0.000000001 * self.Data['youngs'], self.Data['possions'], self.Data['thermalexpansion']))

    def database_add(self, name, yield_stress_Pa, ultimate_Pa, youngs_Pa, possions, density_kgm3, thermal):
        """Add another mateiral to the database"""
        self._materials_data[name] = {'yield_stress': yield_stress_Pa,
                         'ultimate_stress':  ultimate_Pa, 
                         'possions_ratio': possions, 
                         'youngs_modulus': youngs_Pa,
                         'density': density_kgm3,
                         'thermal_expansion': thermal
                         }

    def database_display(self):
        """Print out the database to the command line"""
        print("Material                       Yield   Ultimate  Youngs   Possions  Thermal")
        print("Name                           Stress  Stress    Modulus  Ratio     Expansion")
        print("                               (MPa)   (MPa)     (GPa)    (-)       (-)")
        
        for material_name in sorted(self._material_data):
            material = self._materials_data[material_name]
            print ("{:30} {:5.1f}   {:6.1f}    {:5.1f}    {:5.3f}     {:5.2e}".format(material_name, 
                   1e-6 * material['yield'], 
                   1e-6 * material['ultimate'], 
                   1e-9 * material['youngs'], 
                   material['possions'], 
                   material['thermalexpansion']))

    def database_save(self, filename='Materials.txt'):
        """Save the database using pickle"""
        with open(filename, 'wb') as save_file:
            save_file.write(pickle.dumps(self.__dict__))
    
    def database_load(self, filename='Materials.txt'):
        """Load the database using pickle from an existing file"""
        with open(filename, 'rb') as load_file:
            dict_data = load_file.read()
            self.__dict__ = pickle.loads(dict_data)
