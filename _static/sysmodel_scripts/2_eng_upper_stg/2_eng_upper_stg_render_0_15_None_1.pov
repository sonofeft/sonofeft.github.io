#include "colors.inc"
#include "transforms.inc"
#include "D:\2018_P~1\PRISM\prism\examples\2_ENG_~1\2_eng_upper_stg_render_0_15_None_1.inc"

background {Black}
light_source { <10, 30, 0>  color White transmit 0 filter 0  shadowless}

#declare  mainObject = 
  union { 
    object { System  }
  }

#declare finalObject = object { mainObject  rotate <0,15,0> }

finalObject

#declare camLoc = LocationForAngleD(finalObject, 10, 1.06);
camera {location camLoc angle 10 look_at ObjCenter(finalObject)}

light_source { LocationForLight1(finalObject, camLoc, 1)  color White shadowless}
light_source { LocationForLight1(finalObject, camLoc, 2)  color White shadowless}
light_source { LocationForLight1(finalObject, camLoc, 3)  color White shadowless}


