__author__ = 'Miguel Molero'

import sys

FONT_NAME = "TimesNewRomanPSMT"

if sys.platform == "darwin":
	FONT_SIZE_1 = 13
	FONT_SIZE_2 = 12
	FONT_SIZE_3 = 11
else:
	FONT_SIZE_1 = 10
	FONT_SIZE_2 = 9
	FONT_SIZE_3 = 8


if (sys.version_info > (3, 0)):

	RHO = chr(961)
	MU  = chr(956)
	RHO_LABEL = chr(961) + " (kg/m<sup>3</sup>)"
	LAMBDA_LABEL = chr(955) + " (GPa)"
	MU_LABEL = chr(956) + " (GPa)"
	ETAV_LABEL = chr(951) + "<sub>"+chr(955)+"</sub>" + " (GPa)"
	ETAS_LABEL = chr(951) + "<sub>"+chr(956)+"</sub>" + " (GPa)"

	VL_LABEL = " V<sub>L</sub> " + " (m/s)"
	VT_LABEL = " V<sub>T</sub> " + " (m/s)"

	MARK = u"\u2713"
	CROSS = u"\u2718"

else:

	RHO =  u"\u03C1"
	MU = u"\u03BC"
	RHO_LABEL = u"\u03C1" + " (kg/m<sup>3</sup>)"
	LAMBDA_LABEL = u"\u03BB" + " (GPa)"
	MU_LABEL = u"\u03BC" + " (GPa)"
	ETAV_LABEL = u'\u0397' + "<sub>" + u'\u03BB' + "</sub>" + " (GPa)"
	ETAS_LABEL = u'\u0397' + "<sub>" + u'\u03BC' + "</sub>" + " (GPa)"

	VL_LABEL = " V<sub>L</sub> " + " (m/s)"
	VT_LABEL = " V<sub>T</sub> " + " (m/s)"

	MARK = u"\u2713"
	CROSS = u"\u2718"


DEGREE_ANGLE = chr(176)