# _*_ coding: utf-8 _*_

import os
import re
import glob
from unidecode import unidecode
import itertools

# Function to generate IDFS ##############################################

def genIdfs(ecbc_XPS_Thick_Wall,ecbc_Roof_SolarAbsorptance,ecbc_Wall_Construction,ecbc_SHGC_WithShades):
      
      ecbc_Orientation = '0'
      ecbc_SHGC = ecbc_SHGC_WithShades
      ecbc_Win_H = '1'
      ecbc_Win_L = '1'

      ecbc_Building_L = float(ecbc_Win_L) + 2
      ecbc_Building_L = str(ecbc_Building_L)

      ohang = '1'
      ecbc_Overhang_D = '0.5'
      ecbc_Overhang_H = '0'
      ecbc_Overhang_A = '90'
      ecbc_Overhang_LE = '0'
      ecbc_Overhang_RE = '0'

      ecbc_Fin_L_E = '0'
      ecbc_Fin_L_AT = '0'
      ecbc_Fin_L_BB = '0'
      ecbc_Fin_L_A = '90'
      ecbc_Fin_L_D = '0'
      ecbc_Fin_R_E = '0'
      ecbc_Fin_R_AT = '0'
      ecbc_Fin_R_BB = '0'
      ecbc_Fin_R_A = '90'
      ecbc_Fin_R_D = '0'

      temp = ecbc_SHGC

      # Generate IDF file with shade ###################################

      os.system("mkdir"+ ' ./static/Data/'+ecbc_SHGC+'input')
      with open('./static/template.idf', 'rt') as f1:
            with open('./static/Data/'+ecbc_SHGC+'input/'+ecbc_SHGC+'.idf', 'wt') as f2:
                  for a in f1:
                     a = a.decode('utf-8')
                     a = a.replace('ecbc_SHGC',ecbc_SHGC)
                     a = a.replace('ecbc_Win_H',ecbc_Win_H)
                     a = a.replace('ecbc_Win_L',ecbc_Win_L)
                     a = a.replace('ecbc_Orientation',ecbc_Orientation)

                     a = a.replace('ecbc_Building_L',ecbc_Building_L)
                     a = a.replace('ecbc_XPS_Thick_Wall',ecbc_XPS_Thick_Wall)
                     a = a.replace('ecbc_Wall_Construction',ecbc_Wall_Construction)
                     a = a.replace('ecbc_Roof_SolarAbsorptance',ecbc_Roof_SolarAbsorptance)

                     a = a.replace('ecbc_Overhang_D',ecbc_Overhang_D)
                     a = a.replace('ecbc_Overhang_H',ecbc_Overhang_H)
                     a = a.replace('ecbc_Overhang_A',ecbc_Overhang_A)
                     a = a.replace('ecbc_Overhang_LE',ecbc_Overhang_LE)
                     a = a.replace('ecbc_Overhang_RE',ecbc_Overhang_RE)

                     a = a.replace('ecbc_Fin_L_E',ecbc_Fin_L_E)
                     a = a.replace('ecbc_Fin_L_D',ecbc_Fin_L_D)
                     a = a.replace('ecbc_Fin_L_AT',ecbc_Fin_L_AT)
                     a = a.replace('ecbc_Fin_L_BB',ecbc_Fin_L_BB)
                     a = a.replace('ecbc_Fin_L_A',ecbc_Fin_L_A)
                     a = a.replace('ecbc_Fin_L_D',ecbc_Fin_L_D)
                     a = a.replace('ecbc_Fin_R_E',ecbc_Fin_R_E)
                     a = a.replace('ecbc_Fin_R_D',ecbc_Fin_R_D)
                     a = a.replace('ecbc_Fin_R_AT',ecbc_Fin_R_AT)
                     a = a.replace('ecbc_Fin_R_BB',ecbc_Fin_R_BB)
                     a = a.replace('ecbc_Fin_R_A',ecbc_Fin_R_A)
                     a = a.replace('ecbc_Fin_R_D',ecbc_Fin_R_D)
                     a = a.encode('utf-8')
                     f2.write(a)
      f1.close()
      f2.close()

      # Generate IDF files without shade with change with SHGC ###################################

      while (float(ecbc_SHGC) > 0.05):
         
         os.system("mkdir"+ ' ./static/Data/'+ecbc_SHGC)
         with open('./static/template_2.idf', 'rt') as f1:
               with open('./static/Data/'+ecbc_SHGC+'/'+ecbc_SHGC+'.idf', 'wt') as f2:

                  for a in f1:
                     a = a.decode('utf-8')
                     a = a.replace('ecbc_SHGC',ecbc_SHGC)
                     a = a.replace('ecbc_Win_H',ecbc_Win_H)
                     a = a.replace('ecbc_Win_L',ecbc_Win_L)
                     a = a.replace('ecbc_Orientation',ecbc_Orientation)
                     a = a.replace('ecbc_Building_L',ecbc_Building_L)
                     a = a.replace('ecbc_XPS_Thick_Wall',ecbc_XPS_Thick_Wall)
                     a = a.replace('ecbc_Wall_Construction',ecbc_Wall_Construction)
                     a = a.replace('ecbc_Roof_SolarAbsorptance',ecbc_Roof_SolarAbsorptance)
                     a = a.encode('utf-8')
                     f2.write(a)
         ecbc_SHGC = float(ecbc_SHGC) - 0.05
         ecbc_SHGC = str(ecbc_SHGC)
         f1.close()
         f2.close()
      return (temp)


#Function to simulate IDFs #############################################################

def simulateIdfs(name):
   Dict = {}
   tempo = name
   tempo1 = name
   tempo2 = name
   os.system("runenergyplus ./static/Data/"+tempo+"input/"+tempo+".idf /usr/local/EnergyPlus-7-2-0/WeatherData/epw/hongkong.epw")
   k=glob.glob("./static/Data/"+tempo+"input/Output/*.html")
   pat = '<td align="right">Total Site Energy</td>'
   pat2= "\d+.\d+"

   for t in k:
      tuple1 = ()
      tuple2 = ()
      f=open(t,"r")
      for i in f:
         #print i
         tuple1=re.findall(pat,i,re.M)
         if len(tuple1)>0:
            break

      for j in f:
      #print j
         tuple2=re.findall(pat2,j)
         break

   Dict[tempo+'input'] = tuple2[0]
   while (float(tempo) > 0.05):
      os.system("runenergyplus ./static/Data/"+tempo+"/"+tempo+".idf /usr/local/EnergyPlus-7-2-0/WeatherData/epw/hongkong.epw")
      k=glob.glob("./static/Data/"+tempo+"/Output/*.html")
      pat = '<td align="right">Total Site Energy</td>'
      pat2= "\d+.\d+"

      for t in k:
         tuple1 = ()
         tuple2 = ()
         f=open(t,"r")
         for i in f:
         #print i
            tuple1=re.findall(pat,i,re.M)
            if len(tuple1)>0:
               break

         for j in f:
         #print j
            tuple2=re.findall(pat2,j)
            break

      Dict[tempo] = tuple2[0]
      tempo = float(tempo) - 0.05
      tempo = str(tempo)

      for ash in Dict:
         print ash+":"+Dict[ash]+'\n'


   os.system("rm -rf ./static/Data/*")
   while(float(tempo1) > 0.05):
      if((Dict[tempo1] >= Dict[tempo2+'input'])and (Dict[str(float(tempo1)-0.05)] <= Dict[tempo2+'input'])):
         a = tempo1
         break
      else:
         tempo1 = float(tempo1) - 0.05
         tempo1 = str(tempo1)

   slope = (float(Dict[a])-float(Dict[str(float(a)-0.05)])) / (0.05)
   const = float(Dict[a]) - slope*(float(a))
   final_shgc = (float(Dict[str(tempo2)+'input']) - float(const))/float(slope)
   final_shgc = round(final_shgc,4)
   #print final_shgc
   return (final_shgc)



##################################################
#  Main Start from here
####################################################

# Wall XPS Thinkness in meters
#ecbc_XPS_Thick_Wall = ['0.005','0.02','0.04','0.06','0.08','0.1','0.12']
ecbc_XPS_Thick_Wall = ['0.04']
ecbc_Roof_SolarAbsorptance = ['0.4']
ecbc_Wall_Construction = ['Wall_Construction_Mass','Wall_Construction_NoMass']
#ecbc_Wall_Construction = ['Wall_Construction_Mass']
l=[]

ecbc_SHGC_WithShades = ['0.6']

for i in  ecbc_XPS_Thick_Wall:
	for j in ecbc_Roof_SolarAbsorptance:
		for k in ecbc_Wall_Construction:
			for p in ecbc_SHGC_WithShades:
				genIdfs(i,j,k,p)
				eqSHGC = simulateIdfs(p)
				l.append(eqSHGC)
				print "Wall thickness",i, "Equivalent SHGC", eqSHGC

print l






