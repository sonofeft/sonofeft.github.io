
global_settings {max_trace_level 7}

#macro ObjCenter(Object)
   #local Mn = min_extent(Object);
   #local Mx = max_extent(Object);
   
   #local result = (Mx - Mn)/2 + Mn;
   result
#end
#macro LocationForAngleD(Object, myAngleD, myMargin)
   // myAngleD is full angle of view
   // myMargin is a multiplier on the distance (normal = 1.1, ortho views need 1.5)
   // camera is moved away from Object along negative z axis by distance d
   #local Mn = min_extent(Object);
   #local Mx = max_extent(Object);
   
   #local sOvrd = tan( myAngleD*pi/180.0/2.0 );
   #local Ds = (Mx - Mn)/2;
   #local objC = (Mx - Mn)/2 + Mn;
   
   // make maxDist in y direction (i.e. assume screen aspect ratio of 4/3
   //#local maxDist = sqrt(Ds.x*Ds.x + Ds.y*Ds.y + Ds.z*Ds.z) * 4.0/3.0;
   //#local d = maxDist/sOvrd;

   //  project object bounding box onto the z axis
   #local zoffset = Mn.z;
   #local Proj = VProject_Plane(Ds, <0,0,1> );
   #local d = myMargin * ( max(Proj.x/sOvrd, Proj.y*4.0/sOvrd/3.0) ) - zoffset;
   
   #local result = (<objC.x, objC.y, objC.z-d>);
   result
#end
#macro LocationForLight1(Object, camLoc, N)
   // myMargin is a multiplier on the distance (normal = 1.1, ortho views need 1.5)
   // camera is moved away from Object along negative z axis by distance d
   #local Mn = min_extent(Object);
   #local Mx = max_extent(Object);
   
   #local Ds = (Mx - Mn)/2;
   #local maxDist = sqrt(Ds.x*Ds.x + Ds.y*Ds.y + Ds.z*Ds.z)  ;
   #local objC = (Mx - Mn)/2 + Mn;
   #local objMid = (camLoc + objC) / 2.0;
   
   #if (N=1)
       #local result = (<camLoc.x-maxDist, camLoc.y-maxDist, camLoc.z-maxDist>);
   #end
   #if (N=2)
       #local result = (<objMid.x-maxDist*20, objMid.y+maxDist*50.0, objMid.z-maxDist*20>);
   #end
   #if (N=3)
       #local result = (<objMid.x+maxDist, objMid.y-maxDist, objMid.z+maxDist*20>);
   #end
   result
#end

#declare  System = 
     union {         union {  sor { 
           24
            <2.70478484402, 0.0>
            <2.70478484402, 0.0>
            <2.69722171702, 0.114585501431>
            <2.67457463207, 0.228530194258>
            <2.63697024088, 0.341196853539>
            <2.58461884245, 0.451955401612>
            <2.51781320703, 0.560186431749>
            <2.43692693884, 0.665284672127>
            <2.34241238669, 0.766662370754>
            <2.23479811431, 0.863752582417>
            <2.11468594436, 0.956012339268>
            <1.98274759281, 1.04292568732>
            <1.83972091244, 1.12400657189>
            <1.68640576647, 1.19880155576>
            <1.52365955538, 1.26689235505>
            <1.35239242201, 1.3278981784>
            <1.17356216163, 1.38147785648>
            <0.988168865605, 1.42733175002>
            <0.797249328443, 1.46520342542>
            <0.601871249642, 1.49488108894>
            <0.403127262672, 1.51619877102>
            <0.202128824525, 1.52903725454>
            <0.0, 1.53332474151>
            <0.0, 1.53332474151>
            sturm  
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Gray50 transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
            translate <0.0, 31.7473206105, 0.0>  }
          sor { 
           24
            <2.70478484402, 0.0>
            <2.70478484402, 0.0>
            <2.69722171702, 0.114585501431>
            <2.67457463207, 0.228530194258>
            <2.63697024088, 0.341196853539>
            <2.58461884245, 0.451955401612>
            <2.51781320703, 0.560186431749>
            <2.43692693884, 0.665284672127>
            <2.34241238669, 0.766662370754>
            <2.23479811431, 0.863752582417>
            <2.11468594436, 0.956012339268>
            <1.98274759281, 1.04292568732>
            <1.83972091244, 1.12400657189>
            <1.68640576647, 1.19880155576>
            <1.52365955538, 1.26689235505>
            <1.35239242201, 1.3278981784>
            <1.17356216163, 1.38147785648>
            <0.988168865605, 1.42733175002>
            <0.797249328443, 1.46520342542>
            <0.601871249642, 1.49488108894>
            <0.403127262672, 1.51619877102>
            <0.202128824525, 1.52903725454>
            <0.0, 1.53332474151>
            <0.0, 1.53332474151>
            sturm  
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Gray50 transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
            rotate <180.0, 0.0, 0.0>  }
          cylinder { <0.0, 0.0, 0.0>  <0.0, 31.7473206105, 0.0>  2.70478
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Gray50 transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
          }
            translate <13.6917922747, 1.53332474151, 0.0> rotate <0.0, 45.0, 0.0>  }
         union {  sor { 
           24
            <6.57938597955, 0.0>
            <6.57938597955, 0.0>
            <6.56098868193, 0.278729098636>
            <6.50589967421, 0.555899431088>
            <6.41442703648, 0.829960948429>
            <6.28708232083, 1.09938098748>
            <6.12457769056, 1.3626528421>
            <5.92782193749, 1.61830418929>
            <5.69791539959, 1.864905323>
            <5.4361438075, 2.10107714967>
            <5.14397109412, 2.32549890065>
            <4.8230312078, 2.53691551846>
            <4.47511897456, 2.73414467562>
            <4.10218006074, 2.91608338669>
            <3.70630009202, 3.08171417658>
            <3.28969298978, 3.23011077074>
            <2.85468858991, 3.36044327522>
            <2.40371961347, 3.47198281778>
            <1.93930806192, 3.56410562405>
            <1.46405111303, 3.63629650594>
            <0.98060659644, 3.68815174275>
            <0.491678129993, 3.71938133896>
            <0.0, 3.729810646>
            <0.0, 3.729810646>
            sturm  
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Pink transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
            translate <0.0, 27.089333906, 0.0>  }
          sor { 
           24
            <6.57938597955, 0.0>
            <6.57938597955, 0.0>
            <6.56098868193, 0.278729098636>
            <6.50589967421, 0.555899431088>
            <6.41442703648, 0.829960948429>
            <6.28708232083, 1.09938098748>
            <6.12457769056, 1.3626528421>
            <5.92782193749, 1.61830418929>
            <5.69791539959, 1.864905323>
            <5.4361438075, 2.10107714967>
            <5.14397109412, 2.32549890065>
            <4.8230312078, 2.53691551846>
            <4.47511897456, 2.73414467562>
            <4.10218006074, 2.91608338669>
            <3.70630009202, 3.08171417658>
            <3.28969298978, 3.23011077074>
            <2.85468858991, 3.36044327522>
            <2.40371961347, 3.47198281778>
            <1.93930806192, 3.56410562405>
            <1.46405111303, 3.63629650594>
            <0.98060659644, 3.68815174275>
            <0.491678129993, 3.71938133896>
            <0.0, 3.729810646>
            <0.0, 3.729810646>
            sturm  
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Pink transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
            rotate <180.0, 0.0, 0.0>  }
          cylinder { <0.0, 0.0, 0.0>  <0.0, 27.089333906, 0.0>  6.57939
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Pink transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
          }
            translate <9.62537856045, 3.729810646, 0.0>  }
         union {  sor { 
           24
            <6.78295492362, 0.0>
            <6.78295492362, 0.0>
            <6.76398840594, 0.287353093103>
            <6.70719492137, 0.573099191149>
            <6.61289208211, 0.855640286047>
            <6.48160726788, 1.13339629339>
            <6.31407467663, 1.4048138889>
            <6.11123121857, 1.66837519531>
            <5.87421127658, 1.92260627087>
            <5.60434036233, 2.16608535228>
            <5.30312770345, 2.39745080575>
            <4.9722578033, 2.61540874182>
            <4.61358102057, 2.8187402513>
            <4.22910322134, 3.00630822191>
            <3.82097456142, 3.17706369747>
            <3.39147746181, 3.33005174409>
            <2.94301384453, 3.46441679057>
            <2.47809170003, 3.57940741306>
            <1.99931106153, 3.67438053735>
            <1.50934946459, 3.74880503521>
            <1.01094697319, 3.80226469465>
            <0.506890856234, 3.83446054759>
            <0.0, 3.84521254173>
            <0.0, 3.84521254173>
            sturm  
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Aquamarine transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
            translate <0.0, 26.8589942142, 0.0>  }
          sor { 
           24
            <6.78295492362, 0.0>
            <6.78295492362, 0.0>
            <6.76398840594, 0.287353093103>
            <6.70719492137, 0.573099191149>
            <6.61289208211, 0.855640286047>
            <6.48160726788, 1.13339629339>
            <6.31407467663, 1.4048138889>
            <6.11123121857, 1.66837519531>
            <5.87421127658, 1.92260627087>
            <5.60434036233, 2.16608535228>
            <5.30312770345, 2.39745080575>
            <4.9722578033, 2.61540874182>
            <4.61358102057, 2.8187402513>
            <4.22910322134, 3.00630822191>
            <3.82097456142, 3.17706369747>
            <3.39147746181, 3.33005174409>
            <2.94301384453, 3.46441679057>
            <2.47809170003, 3.57940741306>
            <1.99931106153, 3.67438053735>
            <1.50934946459, 3.74880503521>
            <1.01094697319, 3.80226469465>
            <0.506890856234, 3.83446054759>
            <0.0, 3.84521254173>
            <0.0, 3.84521254173>
            sturm  
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Aquamarine transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
            rotate <180.0, 0.0, 0.0>  }
          cylinder { <0.0, 0.0, 0.0>  <0.0, 26.8589942142, 0.0>  6.78295
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Aquamarine transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
          }
            translate <9.62537856045, 3.84521254173, 0.0> rotate <0.0, 90.0, 0.0>  }
         union {  difference { 
          cylinder { <0, 0, 0>  <0, 36.0, 0>  16.5
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color White transmit 0.9 filter 0 
                }
                normal{ bumps 0.01 }
              }
          }
          cylinder { <0, -0.1, 0>  <0, 36.1, 0>  16.42
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color White transmit 0.9 filter 0 
                }
                normal{ bumps 0.01 }
              }
          }
          }
          difference { 
          cylinder { <0, 0, 0>  <0, 0.1, 0>  16.5
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color White transmit 0.9 filter 0 
                }
                normal{ bumps 0.01 }
              }
          }
          cylinder { <0, -0.1, 0>  <0, 0.2, 0>  16
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color White transmit 0.9 filter 0 
                }
                normal{ bumps 0.01 }
              }
          }
          }
          difference { 
          cylinder { <0, 0, 0>  <0, 0.1, 0>  16.5
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color White transmit 0.9 filter 0 
                }
                normal{ bumps 0.01 }
              }
          }
          cylinder { <0, -0.1, 0>  <0, 0.2, 0>  16
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color White transmit 0.9 filter 0 
                }
                normal{ bumps 0.01 }
              }
          }
            translate <0.0, 35.9, 0.0>  }
            translate <0, -0.75, 0>  }
         union {  sor { 
           24
            <2.70478484402, 0.0>
            <2.70478484402, 0.0>
            <2.69722171702, 0.114585501431>
            <2.67457463207, 0.228530194258>
            <2.63697024088, 0.341196853539>
            <2.58461884245, 0.451955401612>
            <2.51781320703, 0.560186431749>
            <2.43692693884, 0.665284672127>
            <2.34241238669, 0.766662370754>
            <2.23479811431, 0.863752582417>
            <2.11468594436, 0.956012339268>
            <1.98274759281, 1.04292568732>
            <1.83972091244, 1.12400657189>
            <1.68640576647, 1.19880155576>
            <1.52365955538, 1.26689235505>
            <1.35239242201, 1.3278981784>
            <1.17356216163, 1.38147785648>
            <0.988168865605, 1.42733175002>
            <0.797249328443, 1.46520342542>
            <0.601871249642, 1.49488108894>
            <0.403127262672, 1.51619877102>
            <0.202128824525, 1.52903725454>
            <0.0, 1.53332474151>
            <0.0, 1.53332474151>
            sturm  
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Gray50 transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
            translate <0.0, 31.7473206105, 0.0>  }
          sor { 
           24
            <2.70478484402, 0.0>
            <2.70478484402, 0.0>
            <2.69722171702, 0.114585501431>
            <2.67457463207, 0.228530194258>
            <2.63697024088, 0.341196853539>
            <2.58461884245, 0.451955401612>
            <2.51781320703, 0.560186431749>
            <2.43692693884, 0.665284672127>
            <2.34241238669, 0.766662370754>
            <2.23479811431, 0.863752582417>
            <2.11468594436, 0.956012339268>
            <1.98274759281, 1.04292568732>
            <1.83972091244, 1.12400657189>
            <1.68640576647, 1.19880155576>
            <1.52365955538, 1.26689235505>
            <1.35239242201, 1.3278981784>
            <1.17356216163, 1.38147785648>
            <0.988168865605, 1.42733175002>
            <0.797249328443, 1.46520342542>
            <0.601871249642, 1.49488108894>
            <0.403127262672, 1.51619877102>
            <0.202128824525, 1.52903725454>
            <0.0, 1.53332474151>
            <0.0, 1.53332474151>
            sturm  
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Gray50 transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
            rotate <180.0, 0.0, 0.0>  }
          cylinder { <0.0, 0.0, 0.0>  <0.0, 31.7473206105, 0.0>  2.70478
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Gray50 transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
          }
            translate <13.6917922747, 1.53332474151, 0.0> rotate <0.0, 225.0, 0.0>  }
         union {  sor { 
           24
            <6.57938597955, 0.0>
            <6.57938597955, 0.0>
            <6.56098868193, 0.278729098636>
            <6.50589967421, 0.555899431088>
            <6.41442703648, 0.829960948429>
            <6.28708232083, 1.09938098748>
            <6.12457769056, 1.3626528421>
            <5.92782193749, 1.61830418929>
            <5.69791539959, 1.864905323>
            <5.4361438075, 2.10107714967>
            <5.14397109412, 2.32549890065>
            <4.8230312078, 2.53691551846>
            <4.47511897456, 2.73414467562>
            <4.10218006074, 2.91608338669>
            <3.70630009202, 3.08171417658>
            <3.28969298978, 3.23011077074>
            <2.85468858991, 3.36044327522>
            <2.40371961347, 3.47198281778>
            <1.93930806192, 3.56410562405>
            <1.46405111303, 3.63629650594>
            <0.98060659644, 3.68815174275>
            <0.491678129993, 3.71938133896>
            <0.0, 3.729810646>
            <0.0, 3.729810646>
            sturm  
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Pink transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
            translate <0.0, 27.089333906, 0.0>  }
          sor { 
           24
            <6.57938597955, 0.0>
            <6.57938597955, 0.0>
            <6.56098868193, 0.278729098636>
            <6.50589967421, 0.555899431088>
            <6.41442703648, 0.829960948429>
            <6.28708232083, 1.09938098748>
            <6.12457769056, 1.3626528421>
            <5.92782193749, 1.61830418929>
            <5.69791539959, 1.864905323>
            <5.4361438075, 2.10107714967>
            <5.14397109412, 2.32549890065>
            <4.8230312078, 2.53691551846>
            <4.47511897456, 2.73414467562>
            <4.10218006074, 2.91608338669>
            <3.70630009202, 3.08171417658>
            <3.28969298978, 3.23011077074>
            <2.85468858991, 3.36044327522>
            <2.40371961347, 3.47198281778>
            <1.93930806192, 3.56410562405>
            <1.46405111303, 3.63629650594>
            <0.98060659644, 3.68815174275>
            <0.491678129993, 3.71938133896>
            <0.0, 3.729810646>
            <0.0, 3.729810646>
            sturm  
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Pink transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
            rotate <180.0, 0.0, 0.0>  }
          cylinder { <0.0, 0.0, 0.0>  <0.0, 27.089333906, 0.0>  6.57939
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Pink transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
          }
            translate <9.62537856045, 3.729810646, 0.0> rotate <0.0, 180.0, 0.0>  }
         union {  sor { 
           24
            <6.78295492362, 0.0>
            <6.78295492362, 0.0>
            <6.76398840594, 0.287353093103>
            <6.70719492137, 0.573099191149>
            <6.61289208211, 0.855640286047>
            <6.48160726788, 1.13339629339>
            <6.31407467663, 1.4048138889>
            <6.11123121857, 1.66837519531>
            <5.87421127658, 1.92260627087>
            <5.60434036233, 2.16608535228>
            <5.30312770345, 2.39745080575>
            <4.9722578033, 2.61540874182>
            <4.61358102057, 2.8187402513>
            <4.22910322134, 3.00630822191>
            <3.82097456142, 3.17706369747>
            <3.39147746181, 3.33005174409>
            <2.94301384453, 3.46441679057>
            <2.47809170003, 3.57940741306>
            <1.99931106153, 3.67438053735>
            <1.50934946459, 3.74880503521>
            <1.01094697319, 3.80226469465>
            <0.506890856234, 3.83446054759>
            <0.0, 3.84521254173>
            <0.0, 3.84521254173>
            sturm  
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Aquamarine transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
            translate <0.0, 26.8589942142, 0.0>  }
          sor { 
           24
            <6.78295492362, 0.0>
            <6.78295492362, 0.0>
            <6.76398840594, 0.287353093103>
            <6.70719492137, 0.573099191149>
            <6.61289208211, 0.855640286047>
            <6.48160726788, 1.13339629339>
            <6.31407467663, 1.4048138889>
            <6.11123121857, 1.66837519531>
            <5.87421127658, 1.92260627087>
            <5.60434036233, 2.16608535228>
            <5.30312770345, 2.39745080575>
            <4.9722578033, 2.61540874182>
            <4.61358102057, 2.8187402513>
            <4.22910322134, 3.00630822191>
            <3.82097456142, 3.17706369747>
            <3.39147746181, 3.33005174409>
            <2.94301384453, 3.46441679057>
            <2.47809170003, 3.57940741306>
            <1.99931106153, 3.67438053735>
            <1.50934946459, 3.74880503521>
            <1.01094697319, 3.80226469465>
            <0.506890856234, 3.83446054759>
            <0.0, 3.84521254173>
            <0.0, 3.84521254173>
            sturm  
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Aquamarine transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
            rotate <180.0, 0.0, 0.0>  }
          cylinder { <0.0, 0.0, 0.0>  <0.0, 26.8589942142, 0.0>  6.78295
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Aquamarine transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
          }
            translate <9.62537856045, 3.84521254173, 0.0> rotate <0.0, 270.0, 0.0>  }
         union {  sor { 
           45
            <0.0, -0.715318693918>
            <0.0, -0.715318693918>
            <0.121368741174, -0.707809225064>
            <0.239049754564, -0.685508989914>
            <0.349467362126, -0.649095569828>
            <0.449266580729, -0.59967536815>
            <0.535415061616, -0.538749992699>
            <0.605295226789, -0.46817063018>
            <0.65678380279, -0.390081798806>
            <0.688316335292, -0.306856188206>
            <0.698934724251, -0.221022566442>
            <0.698934724251, 0.0>
            <0.698934724251, 0.25>
            <0.698934724251, 0.5>
            <0.698934724251, 0.75>
            <0.698934724251, 1.0>
            <0.697802763591, 1.03161445977>
            <0.694412678913, 1.06306700699>
            <0.688781832438, 1.09419655837>
            <0.680939062383, 1.12484368481>
            <0.625714495475, 1.31242184241>
            <0.570489928567, 1.5>
            <0.515265361659, 1.68757815759>
            <0.460040794751, 1.87515631519>
            <0.452198024696, 1.90580344163>
            <0.446567178222, 1.93693299301>
            <0.443177093544, 1.96838554023>
            <0.442045132883, 2.0>
            <0.443515475164, 2.03602434442>
            <0.447916720622, 2.07180903858>
            <0.455219590178, 2.10711602647>
            <0.465375501834, 2.14171043>
            <0.519501585534, 2.24995798397>
            <0.7661593835, 2.63830496679>
            <1.00487175481, 3.07220665825>
            <1.23563869946, 3.55166305836>
            <1.45846021745, 4.07667416711>
            <1.67333630879, 4.64723998452>
            <1.88026697347, 5.26336051057>
            <2.07925221149, 5.92503574526>
            <2.27029202286, 6.63226568861>
            <2.45338640756, 7.3850503406>
            <2.62853536561, 8.18338970124>
            <2.79573889701, 9.02728377053>
            <2.79573889701, 9.02728377053>
            open  
            sturm  
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0.1
                }
                pigment {
                  color Coral transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
          }
            rotate <180, 0, 0> translate <13.704261103, 8.27728377053, 0.0> rotate <0.0, -45.0, 0.0>  }
         union {  sor { 
           45
            <0.0, -0.715318693918>
            <0.0, -0.715318693918>
            <0.121368741174, -0.707809225064>
            <0.239049754564, -0.685508989914>
            <0.349467362126, -0.649095569828>
            <0.449266580729, -0.59967536815>
            <0.535415061616, -0.538749992699>
            <0.605295226789, -0.46817063018>
            <0.65678380279, -0.390081798806>
            <0.688316335292, -0.306856188206>
            <0.698934724251, -0.221022566442>
            <0.698934724251, 0.0>
            <0.698934724251, 0.25>
            <0.698934724251, 0.5>
            <0.698934724251, 0.75>
            <0.698934724251, 1.0>
            <0.697802763591, 1.03161445977>
            <0.694412678913, 1.06306700699>
            <0.688781832438, 1.09419655837>
            <0.680939062383, 1.12484368481>
            <0.625714495475, 1.31242184241>
            <0.570489928567, 1.5>
            <0.515265361659, 1.68757815759>
            <0.460040794751, 1.87515631519>
            <0.452198024696, 1.90580344163>
            <0.446567178222, 1.93693299301>
            <0.443177093544, 1.96838554023>
            <0.442045132883, 2.0>
            <0.443515475164, 2.03602434442>
            <0.447916720622, 2.07180903858>
            <0.455219590178, 2.10711602647>
            <0.465375501834, 2.14171043>
            <0.519501585534, 2.24995798397>
            <0.7661593835, 2.63830496679>
            <1.00487175481, 3.07220665825>
            <1.23563869946, 3.55166305836>
            <1.45846021745, 4.07667416711>
            <1.67333630879, 4.64723998452>
            <1.88026697347, 5.26336051057>
            <2.07925221149, 5.92503574526>
            <2.27029202286, 6.63226568861>
            <2.45338640756, 7.3850503406>
            <2.62853536561, 8.18338970124>
            <2.79573889701, 9.02728377053>
            <2.79573889701, 9.02728377053>
            open  
            sturm  
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0.1
                }
                pigment {
                  color Coral transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
          }
            rotate <180, 0, 0> translate <13.704261103, 8.27728377053, 0.0> rotate <0.0, 135.0, 0.0>  }
     }
