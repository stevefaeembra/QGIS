# -*- coding: utf-8 -*-

"""
***************************************************************************
    PreconfiguredAlgorithm.py
    ---------------------
    Date                 : April 2016
    Copyright            : (C) 2016 by Victor Olaya
    Email                : volayaf at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Victor Olaya'
__date__ = 'April 2016'
__copyright__ = '(C) 2016, Victor Olaya'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'


import os
from qgis.core import (QgsProcessingAlgorithm)
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.alglist import algList
import json


class PreconfiguredAlgorithm(GeoAlgorithm):

    def __init__(self, descriptionFile):
        self.descriptionFile = descriptionFile
        with open(self.descriptionFile) as f:
            self.description = json.load(f)
        GeoAlgorithm.__init__(self)
        self._group = ''
        self._name = ''

    def group(self):
        return self._group

    def displayName(self):
        return self._name

    def name(self):
        return os.path.splitext(os.path.basename(self.descriptionFile))[0].lower()

    def flags(self):
        return QgsProcessingAlgorithm.FlagHideFromModeler

    def getCopy(self):
        newone = PreconfiguredAlgorithm(self.descriptionFile)
        newone.outputs = []
        newone.provider = self.provider
        newone._name = self._name
        newone._group = self._group
        return newone

    def defineCharacteristics(self):
        self.name = self.description["name"]
        self._group = self.description["group"]

    def execute(self, feedback):
        self.alg = algList.getAlgorithm(self.description["algname"]).getCopy()
        for name, value in list(self.description["parameters"].items()):
            self.alg.setParameterValue(name, value)
        for name, value in list(self.description["outputs"].items()):
            self.alg.setOutputValue(name, value)
        self.alg.execute(feedback)
        self.outputs = self.alg.outputs
