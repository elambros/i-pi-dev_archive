"""Creates objects that deal with the different ensembles."""

# This file is part of i-PI.
# i-PI Copyright (C) 2014-2015 i-PI developers
# See the "licenses" directory for full license information.


import numpy as np

import ipi.engine.thermostats
import ipi.engine.barostats
from ipi.utils.inputvalue import *
from ipi.inputs.barostats import *
from ipi.inputs.thermostats import *
from ipi.inputs.initializer import *
from ipi.utils.units import *


__all__ = ['InputDynamics']


class InputDynamics(InputDictionary):
   """Dynamics input class.

   Handles generating the appropriate ensemble class from the xml input file,
   and generating the xml checkpoint tags and data from an instance of the
   object.

   Attributes:
      mode: An optional string giving the mode (ensemble) to be simulated.
         Defaults to 'unknown'.

   Fields:
      thermostat: The thermostat to be used for constant temperature dynamics.
      barostat: The barostat to be used for constant pressure or stress
         dynamics.
      timestep: An optional float giving the size of the timestep in atomic
         units. Defaults to 1.0.      
      fixcom: An optional boolean which decides whether the centre of mass
         motion will be constrained or not. Defaults to False.
   """

   attribs={"mode"  : (InputAttribute, {"dtype"   : str,
                                    "default" : 'nve',
                                    "help"    : "The ensemble that will be sampled during the simulation. ",
                                    "options" : ['nve', 'nvt', 'npt', 'nst']}) }
   fields={
           "thermostat" : (InputThermo, {"default"   : input_default(factory=ipi.engine.thermostats.Thermostat),
                                         "help"      : "The thermostat for the atoms, keeps the atom velocity distribution at the correct temperature."} ),
           "barostat" : (InputBaro, {"default"       : input_default(factory=ipi.engine.barostats.Barostat),
                                     "help"          : InputBaro.default_help}),
           "timestep": (InputValue, {"dtype"         : float,
                                     "default"       : 1.0,
                                     "help"          : "The time step.",
                                     "dimension"     : "time"}),
           "edyn":  (InputValue, {"dtype"     : float,
                                         "default"   : 0.0,
                                         "help"      : "The contribution to the conserved quantity from the integrator.",
                                         "dimension" : "energy"})
         }
         
   dynamic = {  }

   default_help = "Holds all the information for the MD integrator, such as timestep, the thermostats and barostats that control it."
   default_label = "DYNAMICS"

   def store(self, dyn):
      """Takes an ensemble instance and stores a minimal representation of it.

      Args:
         ens: An ensemble object.
      """
      
      if dyn == {}: return

      self.mode.store(dyn.enstype)
      self.timestep.store(dyn.dt)
      self.thermostat.store(dyn.thermostat)
      self.edyn.store(dyn.edyn)
      self.barostat.store(dyn.barostat)
      
   def fetch(self):
      """Creates an ensemble object.

      Returns:
         An ensemble object of the appropriate mode and with the appropriate
         objects given the attributes of the InputEnsemble object.
      """
  
      rv = super(InputDynamics,self).fetch()
      rv["mode"] = self.mode.fetch()        
      return rv
