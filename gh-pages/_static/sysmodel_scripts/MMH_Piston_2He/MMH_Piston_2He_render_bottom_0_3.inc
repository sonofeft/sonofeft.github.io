
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
     union {         cylinder { <0, 0, 0>  <0, 18.1534074792, 0>  1.54879
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Pink transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
            translate <3.4149220304, 0.5, 0.0>  }
         cylinder { <0, 0, 0>  <0, 18.1534074792, 0>  1.54879
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Aquamarine transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
            translate <3.4149220304, 0.5, 0.0> rotate <0.0, 90.0, 0.0>  }
         cylinder { <0, 0, 0>  <0, 18.1534074792, 0>  1.54879
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Pink transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
            translate <3.4149220304, 0.5, 0.0> rotate <0.0, 180.0, 0.0>  }
         cylinder { <0, 0, 0>  <0, 18.1534074792, 0>  1.54879
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Aquamarine transmit 0 filter 0 
                }
                normal{ bumps 0.01 }
              }
            translate <3.4149220304, 0.5, 0.0> rotate <0.0, 270.0, 0.0>  }
         union {  sor { 
           45
            <0.0, -0.589835605961>
            <0.0, -0.589835605961>
            <0.0965564361282, -0.583861353096>
            <0.190179053805, -0.56612011915>
            <0.278023177166, -0.537150962539>
            <0.357419706976, -0.497834096428>
            <0.425956219853, -0.449364143899>
            <0.481550268534, -0.393213839931>
            <0.522512655981, -0.331089283098>
            <0.547598760781, -0.264878096623>
            <0.556046354333, -0.196592073901>
            <0.556046354333, 0.0>
            <0.556046354333, 0.12875>
            <0.556046354333, 0.2575>
            <0.556046354333, 0.38625>
            <0.556046354333, 0.515>
            <0.553506917221, 0.559614841613>
            <0.545921408537, 0.603653380316>
            <0.533387812505, 0.646546757468>
            <0.516068029238, 0.687740906818>
            <0.495341640153, 0.730120453409>
            <0.474615251068, 0.7725>
            <0.453888861982, 0.814879546591>
            <0.433162472897, 0.857259093182>
            <0.415842689631, 0.898453242532>
            <0.403309093599, 0.941346619684>
            <0.395723584914, 0.985385158387>
            <0.393184147803, 1.03>
            <0.394536528038, 1.06258281769>
            <0.398584365561, 1.09494149431>
            <0.405299814816, 1.12685343067>
            <0.41463667943, 1.15809910077>
            <0.439200901136, 1.21457674366>
            <0.527949071478, 1.38787133046>
            <0.612408544884, 1.56583857084>
            <0.692579321354, 1.74847846483>
            <0.768461400887, 1.93579101241>
            <0.840054783485, 2.12777621358>
            <0.907359469146, 2.32443406835>
            <0.970375457871, 2.52576457672>
            <1.02910274966, 2.73176773868>
            <1.08354134451, 2.94244355423>
            <1.13369124243, 3.15779202338>
            <1.17955244341, 3.37781314613>
            <1.17955244341, 3.37781314613>
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
            rotate <180, 0, 0> rotate <0.0, 0.0, 90.0> translate <1.39011588583, 9.57670373962, 0> rotate <0.0, 315.0, 0.0>  }
         difference { 
          cylinder { <0, 0, 0>  <0, 19.1534074792, 0>  4.975
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
          cylinder { <0, -0.1, 0>  <0, 19.2534074792, 0>  4.9625
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
         union {  sor { 
           45
            <0.0, -0.589835605961>
            <0.0, -0.589835605961>
            <0.0965564361282, -0.583861353096>
            <0.190179053805, -0.56612011915>
            <0.278023177166, -0.537150962539>
            <0.357419706976, -0.497834096428>
            <0.425956219853, -0.449364143899>
            <0.481550268534, -0.393213839931>
            <0.522512655981, -0.331089283098>
            <0.547598760781, -0.264878096623>
            <0.556046354333, -0.196592073901>
            <0.556046354333, 0.0>
            <0.556046354333, 0.12875>
            <0.556046354333, 0.2575>
            <0.556046354333, 0.38625>
            <0.556046354333, 0.515>
            <0.553506917221, 0.559614841613>
            <0.545921408537, 0.603653380316>
            <0.533387812505, 0.646546757468>
            <0.516068029238, 0.687740906818>
            <0.495341640153, 0.730120453409>
            <0.474615251068, 0.7725>
            <0.453888861982, 0.814879546591>
            <0.433162472897, 0.857259093182>
            <0.415842689631, 0.898453242532>
            <0.403309093599, 0.941346619684>
            <0.395723584914, 0.985385158387>
            <0.393184147803, 1.03>
            <0.394536528038, 1.06258281769>
            <0.398584365561, 1.09494149431>
            <0.405299814816, 1.12685343067>
            <0.41463667943, 1.15809910077>
            <0.439200901136, 1.21457674366>
            <0.527949071478, 1.38787133046>
            <0.612408544884, 1.56583857084>
            <0.692579321354, 1.74847846483>
            <0.768461400887, 1.93579101241>
            <0.840054783485, 2.12777621358>
            <0.907359469146, 2.32443406835>
            <0.970375457871, 2.52576457672>
            <1.02910274966, 2.73176773868>
            <1.08354134451, 2.94244355423>
            <1.13369124243, 3.15779202338>
            <1.17955244341, 3.37781314613>
            <1.17955244341, 3.37781314613>
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
            rotate <180, 0, 0> rotate <0.0, 0.0, 90.0> translate <1.39011588583, 9.57670373962, 0> rotate <0.0, 45.0, 0.0>  }
         union {  sor { 
           45
            <0.0, -0.589835605961>
            <0.0, -0.589835605961>
            <0.0965564361282, -0.583861353096>
            <0.190179053805, -0.56612011915>
            <0.278023177166, -0.537150962539>
            <0.357419706976, -0.497834096428>
            <0.425956219853, -0.449364143899>
            <0.481550268534, -0.393213839931>
            <0.522512655981, -0.331089283098>
            <0.547598760781, -0.264878096623>
            <0.556046354333, -0.196592073901>
            <0.556046354333, 0.0>
            <0.556046354333, 0.12875>
            <0.556046354333, 0.2575>
            <0.556046354333, 0.38625>
            <0.556046354333, 0.515>
            <0.553506917221, 0.559614841613>
            <0.545921408537, 0.603653380316>
            <0.533387812505, 0.646546757468>
            <0.516068029238, 0.687740906818>
            <0.495341640153, 0.730120453409>
            <0.474615251068, 0.7725>
            <0.453888861982, 0.814879546591>
            <0.433162472897, 0.857259093182>
            <0.415842689631, 0.898453242532>
            <0.403309093599, 0.941346619684>
            <0.395723584914, 0.985385158387>
            <0.393184147803, 1.03>
            <0.394536528038, 1.06258281769>
            <0.398584365561, 1.09494149431>
            <0.405299814816, 1.12685343067>
            <0.41463667943, 1.15809910077>
            <0.439200901136, 1.21457674366>
            <0.527949071478, 1.38787133046>
            <0.612408544884, 1.56583857084>
            <0.692579321354, 1.74847846483>
            <0.768461400887, 1.93579101241>
            <0.840054783485, 2.12777621358>
            <0.907359469146, 2.32443406835>
            <0.970375457871, 2.52576457672>
            <1.02910274966, 2.73176773868>
            <1.08354134451, 2.94244355423>
            <1.13369124243, 3.15779202338>
            <1.17955244341, 3.37781314613>
            <1.17955244341, 3.37781314613>
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
            rotate <180, 0, 0> rotate <0.0, 0.0, 90.0> translate <1.39011588583, 9.57670373962, 0> rotate <0.0, 135.0, 0.0>  }
         union {  sor { 
           45
            <0.0, -0.589835605961>
            <0.0, -0.589835605961>
            <0.0965564361282, -0.583861353096>
            <0.190179053805, -0.56612011915>
            <0.278023177166, -0.537150962539>
            <0.357419706976, -0.497834096428>
            <0.425956219853, -0.449364143899>
            <0.481550268534, -0.393213839931>
            <0.522512655981, -0.331089283098>
            <0.547598760781, -0.264878096623>
            <0.556046354333, -0.196592073901>
            <0.556046354333, 0.0>
            <0.556046354333, 0.12875>
            <0.556046354333, 0.2575>
            <0.556046354333, 0.38625>
            <0.556046354333, 0.515>
            <0.553506917221, 0.559614841613>
            <0.545921408537, 0.603653380316>
            <0.533387812505, 0.646546757468>
            <0.516068029238, 0.687740906818>
            <0.495341640153, 0.730120453409>
            <0.474615251068, 0.7725>
            <0.453888861982, 0.814879546591>
            <0.433162472897, 0.857259093182>
            <0.415842689631, 0.898453242532>
            <0.403309093599, 0.941346619684>
            <0.395723584914, 0.985385158387>
            <0.393184147803, 1.03>
            <0.394536528038, 1.06258281769>
            <0.398584365561, 1.09494149431>
            <0.405299814816, 1.12685343067>
            <0.41463667943, 1.15809910077>
            <0.439200901136, 1.21457674366>
            <0.527949071478, 1.38787133046>
            <0.612408544884, 1.56583857084>
            <0.692579321354, 1.74847846483>
            <0.768461400887, 1.93579101241>
            <0.840054783485, 2.12777621358>
            <0.907359469146, 2.32443406835>
            <0.970375457871, 2.52576457672>
            <1.02910274966, 2.73176773868>
            <1.08354134451, 2.94244355423>
            <1.13369124243, 3.15779202338>
            <1.17955244341, 3.37781314613>
            <1.17955244341, 3.37781314613>
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
            rotate <180, 0, 0> rotate <0.0, 0.0, 90.0> translate <1.39011588583, 9.57670373962, 0> rotate <0.0, 225.0, 0.0>  }
         union {  sor { 
           45
            <0.0, -0.589835605961>
            <0.0, -0.589835605961>
            <0.0965564361282, -0.583861353096>
            <0.190179053805, -0.56612011915>
            <0.278023177166, -0.537150962539>
            <0.357419706976, -0.497834096428>
            <0.425956219853, -0.449364143899>
            <0.481550268534, -0.393213839931>
            <0.522512655981, -0.331089283098>
            <0.547598760781, -0.264878096623>
            <0.556046354333, -0.196592073901>
            <0.556046354333, 0.0>
            <0.556046354333, 0.12875>
            <0.556046354333, 0.2575>
            <0.556046354333, 0.38625>
            <0.556046354333, 0.515>
            <0.553506917221, 0.559614841613>
            <0.545921408537, 0.603653380316>
            <0.533387812505, 0.646546757468>
            <0.516068029238, 0.687740906818>
            <0.495341640153, 0.730120453409>
            <0.474615251068, 0.7725>
            <0.453888861982, 0.814879546591>
            <0.433162472897, 0.857259093182>
            <0.415842689631, 0.898453242532>
            <0.403309093599, 0.941346619684>
            <0.395723584914, 0.985385158387>
            <0.393184147803, 1.03>
            <0.394536528038, 1.06258281769>
            <0.398584365561, 1.09494149431>
            <0.405299814816, 1.12685343067>
            <0.41463667943, 1.15809910077>
            <0.439200901136, 1.21457674366>
            <0.527949071478, 1.38787133046>
            <0.612408544884, 1.56583857084>
            <0.692579321354, 1.74847846483>
            <0.768461400887, 1.93579101241>
            <0.840054783485, 2.12777621358>
            <0.907359469146, 2.32443406835>
            <0.970375457871, 2.52576457672>
            <1.02910274966, 2.73176773868>
            <1.08354134451, 2.94244355423>
            <1.13369124243, 3.15779202338>
            <1.17955244341, 3.37781314613>
            <1.17955244341, 3.37781314613>
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
            rotate <180, 0, 0> rotate <0.0, 0.0, 90.0> translate <1.39011588583, 9.57670373962, 0> rotate <0.0, 315.0, 0.0>  }
         union {  sor { 
           24
            <1.57984445187, 0.0>
            <1.57984445187, 0.0>
            <1.57542688636, 0.0737887023378>
            <1.56219889465, 0.147164748321>
            <1.54023445304, 0.219717789335>
            <1.50965639558, 0.291042079346>
            <1.47063572719, 0.360738743992>
            <1.42339066727, 0.428418011252>
            <1.36818542935, 0.493701391211>
            <1.30532874353, 0.556223792726>
            <1.23517212988, 0.615635565167>
            <1.15810793265, 0.671604453802>
            <1.07456712608, 0.723817457904>
            <0.985016904267, 0.771982581173>
            <0.889958068361, 0.815830464704>
            <0.789922225937, 0.855115893344>
            <0.685468818003, 0.889619167042>
            <0.577181990387, 0.919147329494>
            <0.465667326954, 0.943535247239>
            <0.351548462937, 0.962646533148>
            <0.235463597313, 0.976374309159>
            <0.118061923741, 0.984641803978>
            <0.0, 0.987402782421>
            <0.0, 0.987402782421>
            sturm  
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Gray50 transmit 0.8 filter 0 
                }
                normal{ bumps 0.01 }
              }
            translate <0.0, 5.62067218911, 0.0>  }
          sor { 
           24
            <1.57984445187, 0.0>
            <1.57984445187, 0.0>
            <1.57542688636, 0.0737887023378>
            <1.56219889465, 0.147164748321>
            <1.54023445304, 0.219717789335>
            <1.50965639558, 0.291042079346>
            <1.47063572719, 0.360738743992>
            <1.42339066727, 0.428418011252>
            <1.36818542935, 0.493701391211>
            <1.30532874353, 0.556223792726>
            <1.23517212988, 0.615635565167>
            <1.15810793265, 0.671604453802>
            <1.07456712608, 0.723817457904>
            <0.985016904267, 0.771982581173>
            <0.889958068361, 0.815830464704>
            <0.789922225937, 0.855115893344>
            <0.685468818003, 0.889619167042>
            <0.577181990387, 0.919147329494>
            <0.465667326954, 0.943535247239>
            <0.351548462937, 0.962646533148>
            <0.235463597313, 0.976374309159>
            <0.118061923741, 0.984641803978>
            <0.0, 0.987402782421>
            <0.0, 0.987402782421>
            sturm  
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Gray50 transmit 0.8 filter 0 
                }
                normal{ bumps 0.01 }
              }
            rotate <180.0, 0.0, 0.0>  }
          cylinder { <0.0, 0.0, 0.0>  <0.0, 5.62067218911, 0.0>  1.57984
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Gray50 transmit 0.8 filter 0 
                }
                normal{ bumps 0.01 }
              }
          }
            translate <0.0, 1.48740278242, 0.0>  }
         union {  sor { 
           24
            <1.57984445187, 0.0>
            <1.57984445187, 0.0>
            <1.57542688636, 0.0737887023378>
            <1.56219889465, 0.147164748321>
            <1.54023445304, 0.219717789335>
            <1.50965639558, 0.291042079346>
            <1.47063572719, 0.360738743992>
            <1.42339066727, 0.428418011252>
            <1.36818542935, 0.493701391211>
            <1.30532874353, 0.556223792726>
            <1.23517212988, 0.615635565167>
            <1.15810793265, 0.671604453802>
            <1.07456712608, 0.723817457904>
            <0.985016904267, 0.771982581173>
            <0.889958068361, 0.815830464704>
            <0.789922225937, 0.855115893344>
            <0.685468818003, 0.889619167042>
            <0.577181990387, 0.919147329494>
            <0.465667326954, 0.943535247239>
            <0.351548462937, 0.962646533148>
            <0.235463597313, 0.976374309159>
            <0.118061923741, 0.984641803978>
            <0.0, 0.987402782421>
            <0.0, 0.987402782421>
            sturm  
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Gray50 transmit 0.8 filter 0 
                }
                normal{ bumps 0.01 }
              }
            translate <0.0, 5.62067218911, 0.0>  }
          sor { 
           24
            <1.57984445187, 0.0>
            <1.57984445187, 0.0>
            <1.57542688636, 0.0737887023378>
            <1.56219889465, 0.147164748321>
            <1.54023445304, 0.219717789335>
            <1.50965639558, 0.291042079346>
            <1.47063572719, 0.360738743992>
            <1.42339066727, 0.428418011252>
            <1.36818542935, 0.493701391211>
            <1.30532874353, 0.556223792726>
            <1.23517212988, 0.615635565167>
            <1.15810793265, 0.671604453802>
            <1.07456712608, 0.723817457904>
            <0.985016904267, 0.771982581173>
            <0.889958068361, 0.815830464704>
            <0.789922225937, 0.855115893344>
            <0.685468818003, 0.889619167042>
            <0.577181990387, 0.919147329494>
            <0.465667326954, 0.943535247239>
            <0.351548462937, 0.962646533148>
            <0.235463597313, 0.976374309159>
            <0.118061923741, 0.984641803978>
            <0.0, 0.987402782421>
            <0.0, 0.987402782421>
            sturm  
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Gray50 transmit 0.8 filter 0 
                }
                normal{ bumps 0.01 }
              }
            rotate <180.0, 0.0, 0.0>  }
          cylinder { <0.0, 0.0, 0.0>  <0.0, 5.62067218911, 0.0>  1.57984
              texture { 
                finish {
                  ambient 0.3  phong 0.8 phong_size 60 reflection 0
                }
                pigment {
                  color Gray50 transmit 0.8 filter 0 
                }
                normal{ bumps 0.01 }
              }
          }
            translate <0.0, 11.8761991657, 0.0>  }
     }

