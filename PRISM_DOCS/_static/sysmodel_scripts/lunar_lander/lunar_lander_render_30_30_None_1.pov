#include "colors.inc"
#include "transforms.inc"
#include "D:\2018_P~1\PRISM\prism\examples\LUNAR_~1\lunar_lander_render_30_30_None_1.inc"

background {Quartz}
light_source { <10, 30, 0>  color White transmit 0 filter 0  shadowless}

#declare  mainObject = 
  union { 
    object { System  }
  }

#declare finalObject = object { mainObject  rotate <30,0,0>  rotate <0,30,0> }

finalObject

#declare camLoc = LocationForAngleD(finalObject, 10, 1.06);
camera {location camLoc angle 10 look_at ObjCenter(finalObject)}

light_source { LocationForLight1(finalObject, camLoc, 1)  color White shadowless}
light_source { LocationForLight1(finalObject, camLoc, 2)  color White shadowless}
light_source { LocationForLight1(finalObject, camLoc, 3)  color White shadowless}


