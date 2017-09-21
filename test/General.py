#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 18:00:24 2017

@author: christopherbridge
"""

import pipetoolbox as ptb


material_test = ptb.Materials()
material_test.database_save()

pipe_test = ptb.Pipe(0.0254, 0.0021082)
pipe_test.material('stainless steel')
pipe_test.display()



