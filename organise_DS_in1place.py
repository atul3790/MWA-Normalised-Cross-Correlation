'''
Run in python3 or inside CASA. Copies all Ncross DS pickle files in subdirectories of a basedir to a common folder. 
The name of the DS files will be changed to 'Ncross_starttime-endtime_startFreq-EndFreq_STOKES.p' . This code works best for output of 
Make_normCC_DS.py as the folder structure the code assumes is the natural structure that Make_normCC_DS uses. 

This code hepls to gather all DS pickle files corresponding to different bands in a 'picket fence' or 'harmonic' mode observation to one place.  

################# INPUT #################################
basedir = '/Users/atulm/Documents/Post_Doc_EMISSA/Parker_probe_MWA/Ra_data/1239162800/' # Basedir where pickle files directory and MS folder exist 
DS_pickledir='DS_pfiles/' # Location in basedir where pickle files are saved by Make_normCC_DS.py
pdest_dir='Mean_DS_pfiles/' # Location where to save baseline-averaged NCC DS pickle files
pngdest_dir='Mean_I_DS_pngs/' # Location where to save baseline-averaged NCC DS PNGs
DS_png_filenametag='*mean_I_DS*.png' # Give with wildcards '*' and extension
DS_pfilename_format='Ncross_mean_I_DS.p' # Give the search string to find the files of that type
Stokes='I'
#############################################################

'''
import matplotlib.pyplot as plt
import numpy as np,os,glob
from datetime import datetime as dt
import pickle
from datetime import timedelta
################# INPUT #################################
basedir = '/Users/atulm/Documents/Post_Doc_EMISSA/Parker_probe_MWA/Ra_data/1239162800/'
DS_pickledir='DS_pfiles/'
pdest_dir='Mean_DS_pfiles/'
pngdest_dir='Mean_I_DS_pngs/'
DS_png_filenametag='*mean_I_DS*.png' # Give with wildcards '*' and extension
DS_pfilename_format='Ncross_mean_I_DS.p' # Give the search string to find the files of that type
Stokes='I'
#############################################################

cwd=os.getcwd()
os.chdir(basedir)
folds=glob.glob(DS_pickledir+'*_ncrossDS/')
os.system('mkdir '+pdest_dir)
os.system('mkdir '+pngdest_dir)

for fld in folds:
	mstag=fld.replace('ncrossDS/','').split('/')[-1]
	fils=glob.glob(fld+DS_pfilename_format)
	for fil in fils:
		alldet=pickle.load(open(fil,'rb'))
		stt,Dt,T=alldet[1]
		rf,dnu,BW=alldet[0]
		fq_str=str(round(rf,3))+'-'+str(round(rf+BW,3))
		st_time=str(stt.time()).replace(':','')
		endt=stt+timedelta(seconds=T)
		end_time=str(endt.time()).replace(':','')
		tm_str=st_time+'-'+end_time
		DS_newname='Ncross_'+tm_str+'_'+fq_str+'_'+Stokes+'.p'
		os.system('cp '+fil+' '+pdest_dir+DS_newname)
	pngsal=glob.glob(fld+'DS_jpgs/'+DS_png_filenametag)
	print 'Pngs with tag ',pngsal
	for fn in pngsal:
		fn1=fn.split('/')[-1]
		print 'Copying ',fn,' under name: ',mstag+fn1		
		os.system('cp '+fn+' '+pngdest_dir+mstag+fn1)
		
os.chdir(cwd)
