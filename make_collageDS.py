'''
Run this code in CASA or python 2. While using Ipython call it as "ipython2" in terminal or python2.7 -m IPython

Makes a DS collage from pickle files with file structure compatible to "Make_normCC_DS.py" and filename compatible to "organise_DS_in1place.py"
output. 
!!!
	Assumes all DS have same time and freq resolution
!!!
Filename format: 'Ncross_starttime-endtime_startFreq-EndFreq_STOKES.p'
picklefile structure: [[Start Freq,resolution,Band width],[start_time,dt,Total time in sec],Dynamic Spectrum,baseline length,angular scale,Mid_freq]
if these are mean normalised DS pickle files
angular scale and baseline length values are mean values corresponding to the various baselines one averaged over.
'''
import pickle,os,glob
import numpy as np
from datetime import timedelta
from datetime import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.cm as cm
import numpy.ma as ma
#################### INPUT ######################
pfile_dir='/Users/atulm/Documents/Post_Doc_EMISSA/Parker_probe_MWA/Event_2/Mean_I_DS_pfiles/'
which_python=2 # Which python does the CASA used to generate the DS pickle files use? 2 or 3 ? Give an integer 
STOKES='I'
delta_t=0.5 # in sec
delta_nu=0.01 # in MHz
datestr='2019/04/13' # Give year string in the format 2012/11/31.
trim_zeros=True # Do you want to trim the masked values at the edge of the DS
trimmed_DS_fold='MeanDS_I_trimmed/'
common_colormap=True # The code will find the common maximum and minimum flux level for all picket fence/harmonic band DS files and set a single colormap for the DS plot.
cmap=cm.jet
bad_data_color='grey' #How to color nans and infs/ no data regions in the DS plot
nxticks=8
DS_pngloc='DS_pngs/'# Give name with '/'
collab='Norm. Cross Correlations'
#########################################################
cwd=os.getcwd()
os.chdir(pfile_dir)
fils=glob.glob('Ncross*'+STOKES+'.p')

###################################################################
# Function to find the last non-zero / masked column in the DS
##################################################################
def find_zero_start(ar):
	x,y=ar.shape
	arm=ar.mask
	armb=arm[:,:-1] + ~arm[:,1:]
	armb=np.mean(armb,axis=0)
	loc=np.max(np.where(armb==0)[0])
	if loc%2 ==1:
		loc+=1
	return loc
###################################################################
encoding='latin1' if which_python==2 else 'ASCII'
timr=[]
frqr=[]
minflx=1
maxflx=0
## Section where the masked columns at the end of the observation are removed
if trim_zeros==True:
	if not os.path.isdir(trimmed_DS_fold):
		os.mkdir(trimmed_DS_fold)
	maxloc=0
	for fl in fils:
		frq,timR,DS,bsln,ang,mid_frq=pickle.load(open(fl,'rb'),encoding=encoding)
		loc=find_zero_start(DS)
		if maxloc<loc:
			maxloc=loc
	tfils=[]	
	for fl in fils:
		frq,timR,DS,bsln,ang,mid_frq=pickle.load(open(fl,'rb'),encoding=encoding)
		if minflx>ma.min(DS):
			minflx=ma.min(DS)
		if maxflx<ma.max(DS):
			maxflx=ma.max(DS)
		timRn=[timR[0],timR[1],timR[1]*maxloc]
		nDS=DS[:,0:maxloc]
		flele=fl.split('_')
		flele[1]=str(timR[0].time()).replace(':','')+'-'+str((timR[0]+timedelta(seconds=timRn[-1])).time()).replace(':','')
		fln='_'.join(flele)
		pickle.dump([frq,timRn,nDS,bsln,ang,mid_frq],open(trimmed_DS_fold+fln,'wb'))
		timr+=[flele[1]]
		frqr+=[flele[2]]
		tfils+=[fln]		
	os.chdir(trimmed_DS_fold)		
	fils=tfils
###################################################################
if not os.path.isdir(DS_pngloc):
	os.mkdir(DS_pngloc)
if trim_zeros==False:
	for i in fils:
		if common_colormap==True:
			frq,timR,DS,bsln,ang,mid_frq=pickle.load(open(i,'rb'),encoding=encoding)
			if minflx>ma.min(DS):
				minflx=ma.min(DS)
			if maxflx<ma.max(DS):
				maxflx=ma.max(DS)			
		spt=i.split('_')
		timr+=[spt[1]]
		frqr+=[spt[2]]
if common_colormap==False:		
	minflx,maxflx=None,None	

un_timr=np.unique(timr) # Finding unique time ranges
un_frqr=np.unique(frqr) # Finding unique frequency ranges
			
un_stt=[] # Finding unique start times
timeranges=[] # List of unique value combinations for [time tag in filename (Eg: '030456-030856'), start time, Total time in sec] 
max_total_time=0 # To get the maximum total time
for i in un_timr:
	stt,endt=i.split('-')
	stt=stt[0:2]+':'+stt[2:4]+':'+stt[4:]
	endt=endt[0:2]+':'+endt[2:4]+':'+endt[4:]
	if not '.' in stt:
		stt+='.0'
	if not '.' in endt:
		endt+='.0'
	Tot_t=(dt.strptime(datestr+' '+endt,'%Y/%m/%d %H:%M:%S.%f')-dt.strptime(datestr+' '+stt,'%Y/%m/%d %H:%M:%S.%f')).total_seconds()	
	timeranges+=[[i,stt, Tot_t]]
	if Tot_t>max_total_time:
		max_total_time=Tot_t
	un_stt+=[dt.strptime(datestr+' '+stt,'%Y/%m/%d %H:%M:%S.%f')]
T_matcher=dict(zip(un_stt,timeranges))
un_stt=np.sort(un_stt)

Frq_ranges=[]
un_stfrq=[]
for i in un_frqr:
	sfq=float(i.split('-')[0])
	efq=float(i.split('-')[1])
	un_stfrq+=[sfq]
	Frq_ranges+=[[i,sfq,np.round(efq-sfq,3)]]
	
F_matcher=dict(zip(un_stfrq,Frq_ranges))
un_stfrq=np.sort(un_stfrq)
plt.ioff()

cmap.set_bad(color=bad_data_color)

GDS=[]
Frq_rng=np.array([])
for fq in un_stfrq:
	if fq!=un_stfrq[-1]:
		N=29
	else:
		N=1	
	Frq_rng=np.append(Frq_rng,np.round(np.arange(fq,fq+F_matcher[fq][-1]+N*delta_nu,delta_nu),3)) # 3 extra rows added
Frq_rng=np.sort(np.unique(Frq_rng))
ylocs=np.arange(len(Frq_rng))
y_matcher=dict(zip(Frq_rng.astype(str),ylocs))

for tm in un_stt:
	tt=T_matcher[tm]	
	tmDS=np.zeros((len(Frq_rng),int(tt[-1]/delta_t)))*np.nan
	ytlocs=[]
	yts=[]
	xts=np.arange(0,tt[-1],tt[-1]/nxticks)
	xts=list(xts)+[tt[-1]]
	xtlocs=list(np.array(xts)/delta_t)
	for fq in un_stfrq:
		ff=F_matcher[fq]
		fl='Ncross_'+tt[0]+'_'+ff[0]+'_'+STOKES+'.p'
		print('Analysing ',fl)
		if fl in fils:
			tdata=pickle.load(open(fl,'rb'))
			ds=tdata[2]
			yts+=[tdata[-1]]
			ytlocs+=[y_matcher[str(tdata[-1])]]			
			y1=y_matcher[str(ff[1])]
			y2=y_matcher[str(ff[1]+ff[-1])]		
			print('Saving DS in ',[y1,y2])
			tmDS[y1:y2]=ds.filled(np.nan)
	plt.figure(figsize=(15,9))		
	plt.imshow(tmDS,origin='lower',aspect='auto',vmax=maxflx,vmin=minflx,cmap=cmap)
	colbr=plt.colorbar()
	colbr.ax.tick_params(labelsize=16)
	colbr.set_label(collab,size=18)
	plt.yticks(ytlocs,yts,size=14)
	plt.xticks(xtlocs,xts,size=14)
	plt.xlabel('Time (s)   +'+tt[1]+' UT',size=16)
	plt.ylabel('Frequency (MHz)',size=16)
	#plt.tight_layout()
	plt.savefig(DS_pngloc+'NcrossDS_'+tt[0]+'.png',dpi=100)
	plt.close()
os.chdir(cwd)
