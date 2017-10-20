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
        'steel' :
            {'yield_stress': 358.5e6,
             'ultimate_stress': 394.3e6,
             'possions_ratio': 0.3,
             'youngs_modulus': 205.0e9,
             'density': 7850.0,
             'thermal_expansion': 1.20e-6
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
            
def youngs_modulus_reference():
    youngs_data = {}
    youngs_data['rubber'] = 0.05e9
    youngs_data['low-density polyethylene'] = 0.5e9
    youngs_data['diatom frustules'] = 2e9
    youngs_data['ptfe'] = 0.5e9
    youngs_data['hdpe'] = 0.8e9
    youngs_data['bacteriophage capsids'] = 2e9
    youngs_data['polypropylene'] = 1.75e9
    youngs_data['polyethylene terephthalate'] = 2.2e9
    youngs_data['nylon'] = 3e9
    youngs_data['polystyrene, solid'] = 3.25e9
    youngs_data['polystyrene, foam'] = 0.005e9
    youngs_data['medium-density fiberboard'] = 4e9
    youngs_data['wood'] = 11e9
    youngs_data['human cortical bone'] = 14e9
    youngs_data['glass-reinforced polyester matrix'] = 17.2e9
    youngs_data['aromatic peptide nanotubes'] = 24e9
    youngs_data['high-strength concrete'] = 30e9
    youngs_data['carbon fiber reinforced plastic'] = 40e9
    youngs_data['hemp fiber'] = 35e9
    youngs_data['magnesium metal'] = 45e9
    youngs_data['glass'] = 70e9
    youngs_data['flax fiber'] = 58e9
    youngs_data['aluminum'] = 69e9
    youngs_data['mother-of-pearl'] = 70e9
    youngs_data['aramid'] = 100e9
    youngs_data['tooth enamel'] = 83e9
    youngs_data['stinging nettle fiber'] = 87e9
    youngs_data['bronze'] = 110e9
    youngs_data['brass'] = 110e9
    youngs_data['titanium'] = 110.3e9
    youngs_data['titanium alloys'] = 112e9
    youngs_data['copper'] = 117e9
    youngs_data['carbon fiber reinforced plastic'] = 181e9
    youngs_data['silicon single crystal'] = 160e9
    youngs_data['wrought iron'] = 200e9
    youngs_data['steel'] = 209e9
    youngs_data['polycrystalline yttrium iron garnet'] = 193e9
    youngs_data['single-crystal yttrium iron garnet'] = 200e9
    youngs_data['cobalt-chrome'] = 240e9
    youngs_data['aromatic peptide nanospheres'] = 250e9
    youngs_data['beryllium'] = 287e9
    youngs_data['molybdenum'] = 330e9
    youngs_data['tungsten'] = 405e9
    youngs_data['silicon carbide'] = 450e9
    youngs_data['tungsten carbide'] = 550e9
    youngs_data['osmium'] = 550e9
    youngs_data['single-walled carbon nanotube'] = 1000e9
    youngs_data['graphene'] = 1050e9
    youngs_data['diamond'] = 1100e9
    youngs_data['carbyne'] = 32100e9
    youngs_data['pvc'] = 2.9e9
    return youngs_data
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
        self.get_material(material_name)
        #
        self._databse_filename = 'Materials.txt'
        
    def name(self, material_name=None):
        """Return the material name"""
        if material_name != None:
            self._name = material_name
        else:
            return self._name
    
    def yield_stress(self, stress=None):
        """Return the yield stress"""
        if stress != None:
            self._yield = stress
        else:
            return self._yield
    
    def ultimate_stress(self, stress=None):
        """Return the ultimate stress"""
        if stress != None:
            self._ultimate = stress
        else:
            return self._ultimate
    
    def possions(self, possions_ratio=None):
        """Return the Possions Ratio"""
        if possions_ratio != None:
            self._possions = possions_ratio
        else:
            return self._possions
    
    def youngs(self, youngs_modulus=None):
        """Return the Youngs Modulus"""
        if youngs_modulus != None:
            self._youngs = youngs_modulus
        else:
            return self._youngs
    
    def density(self, density=None):
        """Return the density of the material"""
        if density != None:
            self._density = density
        else:
            return self._density
    
    def thermalexpansion(self, thermal_expansion=None):
        """Return the thermal expansion of the material"""
        if thermal_expansion != None:
            self._thermal_expansion = thermal_expansion
        else:
            return self._thermal_expansion
    
    def addmat(self, name, yield_stress_Pa, ultimate_Pa, youngs_Pa, possions, density_kgm3, thermal):
        """Add a meterial to the database and set it as the current material"""
        self.database_add(name, yield_stress_Pa, ultimate_Pa, youngs_Pa, possions, density_kgm3, thermal)
        self.get_material(name)
            
    # -------------------------------------------------------------------------
    # Database functions
    # -------------------------------------------------------------------------
    def get_material(self, material_name='default'):
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

    def database_save(self):
        """Save the database using pickle"""
        with open(self._databse_filename, 'wb') as save_file:
            save_file.write(pickle.dumps(self.__dict__))
    
    def database_load(self):
        """Load the database using pickle from an existing file"""
        with open(self._databse_filename, 'rb') as load_file:
            dict_data = load_file.read()
            self.__dict__ = pickle.loads(dict_data)
