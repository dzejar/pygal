# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2014 Kozea
#
# This library is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pygal. If not, see <http://www.gnu.org/licenses/>.
"""
Pyramid chart

"""

from __future__ import division
from pygal.adapters import positive
from pygal.graph.stackedbar import StackedBar


class VerticalPyramid(StackedBar):
    """Pyramid graph"""

    _adapters = [positive]

    def _format(self, value):
        value = value and abs(value)
        return super(VerticalPyramid, self)._format(value)

    def _get_separated_values(self, secondary=False):
        series = self.secondary_series if secondary else self.series
        positive_vals = map(sum, zip(
            *[serie.safe_values
              for index, serie in enumerate(series)
              if index % 2]))
        negative_vals = map(sum, zip(
            *[serie.safe_values
              for index, serie in enumerate(series)
              if not index % 2]))
        return list(positive_vals), list(negative_vals)

    def _compute_box(self, positive_vals, negative_vals):
        self._box.ymax = max(max(positive_vals or [self.zero]),
                             max(negative_vals or [self.zero]))
        self._box.ymin = - self._box.ymax

    def _pre_compute_secondary(self, positive_vals, negative_vals):
        self._secondary_max = max(max(positive_vals), max(negative_vals))
        self._secondary_min = - self._secondary_max

    def _bar(self, serie, parent, x, y, zero, secondary=False):
        if serie.index % 2:
            y = -y
        return super(VerticalPyramid, self)._bar(
            serie, parent, x, y, zero, secondary)
