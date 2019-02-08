
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
           45
            <0.0, -1.65589227806>
            <0.0, -1.65589227806>
            <0.280956674302, -1.63850859776>
            <0.553376622226, -1.5868857512>
            <0.808982501505, -1.50259227243>
            <1.04000785684, -1.38818937616>
            <1.23943309972, -1.2471531365>
            <1.40119879504, -1.08376886823>
            <1.52038977402, -0.903000919658>
            <1.59338447907, -0.710341833432>
            <1.61796500301, -0.511645458395>
            <1.61796500301, 0.0>
            <1.61796500301, 0.102329091679>
            <1.61796500301, 0.204658183358>
            <1.61796500301, 0.306987275037>
            <1.61796500301, 0.409316366716>
            <1.61706532891, 0.452216801041>
            <1.61436788857, 0.495041799516>
            <1.60987742517, 0.537716058937>
            <1.60360183471, 0.58016454116>
            <1.46211489731, 1.41570227905>
            <1.3206279599, 2.25124001694>
            <1.17914102249, 3.08677775483>
            <1.03765408509, 3.92231549272>
            <1.03137849463, 3.96476397494>
            <1.02688803123, 4.00743823436>
            <1.0241905909, 4.05026323284>
            <1.02329091679, 4.09316366716>
            <1.02808108845, 4.19206024223>
            <1.04240675648, 4.29003091916>
            <1.06613379985, 4.38615846837>
            <1.09904007917, 4.47954291614>
            <1.1820947421, 4.64069117245>
            <1.4391940304, 5.06423293033>
            <1.68834131235, 5.51043854576>
            <1.92953658795, 5.97930801874>
            <2.1627798572, 6.47084134928>
            <2.3880711201, 6.98503853737>
            <2.60541037666, 7.521899583>
            <2.81479762686, 8.0814244862>
            <3.01623287071, 8.66361324694>
            <3.20971610821, 9.26846586523>
            <3.39524733937, 9.89598234108>
            <3.57282656417, 10.5461626745>
            <3.57282656417, 10.5461626745>
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
            rotate <180, 0, 0> translate <0.0, 10.5461626745, 0.0>  }
         union {  sor { 
           24
            <5.00000155613, 0.0>
            <5.00000155613, 0.0>
            <4.98602053769, 0.233531615139>
            <4.94415566988, 0.465757226756>
            <4.87464107803, 0.695378135033>
            <4.77786551593, 0.921110206708>
            <4.65437019178, 1.14169105647>
            <4.50484574154, 1.35588710673>
            <4.33012836657, 1.56250048629>
            <4.13119515732, 1.76037572932>
            <3.90915862897, 1.9484062372>
            <3.66526049987, 2.12554046706>
            <3.40086474729, 2.29078781242>
            <3.11744997953, 2.44322414311>
            <2.81660116692, 2.58199697332>
            <2.50000077807, 2.70633022911>
            <2.16941937077, 2.81552858846>
            <1.82670569035, 2.90898136986>
            <1.47377633073, 2.98616594746>
            <1.11260501605, 3.04665067377>
            <0.74521156281, 3.09009729367>
            <0.373650584222, 3.11626283605>
            <0.0, 3.12500097258>
            <0.0, 3.12500097258>
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
            translate <0.0, 13.5061130493, 0.0>  }
          sor { 
           24
            <5.00000155613, 0.0>
            <5.00000155613, 0.0>
            <4.98602053769, 0.233531615139>
            <4.94415566988, 0.465757226756>
            <4.87464107803, 0.695378135033>
            <4.77786551593, 0.921110206708>
            <4.65437019178, 1.14169105647>
            <4.50484574154, 1.35588710673>
            <4.33012836657, 1.56250048629>
            <4.13119515732, 1.76037572932>
            <3.90915862897, 1.9484062372>
            <3.66526049987, 2.12554046706>
            <3.40086474729, 2.29078781242>
            <3.11744997953, 2.44322414311>
            <2.81660116692, 2.58199697332>
            <2.50000077807, 2.70633022911>
            <2.16941937077, 2.81552858846>
            <1.82670569035, 2.90898136986>
            <1.47377633073, 2.98616594746>
            <1.11260501605, 3.04665067377>
            <0.74521156281, 3.09009729367>
            <0.373650584222, 3.11626283605>
            <0.0, 3.12500097258>
            <0.0, 3.12500097258>
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
          cylinder { <0.0, 0.0, 0.0>  <0.0, 13.5061130493, 0.0>  5
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
            translate <0.0, 16.9070936531, 0.0>  }
         union {  sor { 
           24
            <5.00000155682, 0.0>
            <5.00000155682, 0.0>
            <4.98602053837, 0.233531615171>
            <4.94415567055, 0.46575722682>
            <4.87464107869, 0.695378135129>
            <4.77786551658, 0.921110206834>
            <4.65437019242, 1.14169105663>
            <4.50484574216, 1.35588710692>
            <4.33012836717, 1.56250048651>
            <4.13119515788, 1.76037572957>
            <3.90915862951, 1.94840623747>
            <3.66526050038, 2.12554046735>
            <3.40086474776, 2.29078781274>
            <3.11744997995, 2.44322414344>
            <2.8166011673, 2.58199697368>
            <2.50000077841, 2.70633022948>
            <2.16941937107, 2.81552858885>
            <1.8267056906, 2.90898137026>
            <1.47377633093, 2.98616594786>
            <1.11260501621, 3.04665067418>
            <0.745211562912, 3.0900972941>
            <0.373650584273, 3.11626283648>
            <0.0, 3.12500097301>
            <0.0, 3.12500097301>
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
            translate <0.0, 14.6226350527, 0.0>  }
          sor { 
           24
            <5.00000155682, 0.0>
            <5.00000155682, 0.0>
            <4.98602053837, 0.233531615171>
            <4.94415567055, 0.46575722682>
            <4.87464107869, 0.695378135129>
            <4.77786551658, 0.921110206834>
            <4.65437019242, 1.14169105663>
            <4.50484574216, 1.35588710692>
            <4.33012836717, 1.56250048651>
            <4.13119515788, 1.76037572957>
            <3.90915862951, 1.94840623747>
            <3.66526050038, 2.12554046735>
            <3.40086474776, 2.29078781274>
            <3.11744997995, 2.44322414344>
            <2.8166011673, 2.58199697368>
            <2.50000077841, 2.70633022948>
            <2.16941937107, 2.81552858885>
            <1.8267056906, 2.90898137026>
            <1.47377633093, 2.98616594786>
            <1.11260501621, 3.04665067418>
            <0.745211562912, 3.0900972941>
            <0.373650584273, 3.11626283648>
            <0.0, 3.12500097301>
            <0.0, 3.12500097301>
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
          cylinder { <0.0, 0.0, 0.0>  <0.0, 14.6226350527, 0.0>  5
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
            translate <0.0, 36.951502659, 0.0>  }
         union {  sor { 
           24
            <5.00000140873, 0.0>
            <5.00000140873, 0.0>
            <4.98602039069, 0.233531608254>
            <4.94415552412, 0.465757213025>
            <4.87464093432, 0.695378114533>
            <4.77786537507, 0.921110179552>
            <4.65437005457, 1.14169102281>
            <4.50484560873, 1.35588706676>
            <4.33012823892, 1.56250044023>
            <4.13119503552, 1.76037567743>
            <3.90915851373, 1.94840617976>
            <3.66526039182, 2.12554040439>
            <3.40086464703, 2.29078774489>
            <3.11744988762, 2.44322407108>
            <2.81660108388, 2.5819968972>
            <2.50000070436, 2.70633014932>
            <2.16941930681, 2.81552850546>
            <1.8267056365, 2.9089812841>
            <1.47377628728, 2.98616585942>
            <1.11260498325, 3.04665058395>
            <0.745211540841, 3.09009720257>
            <0.373650573206, 3.11626274418>
            <0.0, 3.12500088045>
            <0.0, 3.12500088045>
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
            translate <0.0, 3.05151961535, 0.0>  }
          sor { 
           24
            <5.00000140873, 0.0>
            <5.00000140873, 0.0>
            <4.98602039069, 0.233531608254>
            <4.94415552412, 0.465757213025>
            <4.87464093432, 0.695378114533>
            <4.77786537507, 0.921110179552>
            <4.65437005457, 1.14169102281>
            <4.50484560873, 1.35588706676>
            <4.33012823892, 1.56250044023>
            <4.13119503552, 1.76037567743>
            <3.90915851373, 1.94840617976>
            <3.66526039182, 2.12554040439>
            <3.40086464703, 2.29078774489>
            <3.11744988762, 2.44322407108>
            <2.81660108388, 2.5819968972>
            <2.50000070436, 2.70633014932>
            <2.16941930681, 2.81552850546>
            <1.8267056365, 2.9089812841>
            <1.47377628728, 2.98616585942>
            <1.11260498325, 3.04665058395>
            <0.745211540841, 3.09009720257>
            <0.373650573206, 3.11626274418>
            <0.0, 3.12500088045>
            <0.0, 3.12500088045>
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
          cylinder { <0.0, 0.0, 0.0>  <0.0, 3.05151961535, 0.0>  5
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
            translate <0.0, 58.1124335761, 0.0>  }
         difference { 
          cylinder { <0, 0, 0>  <0, 65.0000001737, 0>  5.125
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
          cylinder { <0, -0.1, 0>  <0, 65.1000001737, 0>  5.0625
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
     }
