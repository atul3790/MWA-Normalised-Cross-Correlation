'''
IMPORTANT: Use this code only inside CASA.
Output saves pickle file with details as follows for each short baseline and also finds mean DS.
[[Start Freq,resolution,Band wind],[start_time,dt,Total time in sec],Dynamic Spectrum,baseline length,angular scale,Mid frequency]

For short baselines to be used to get NCC use from the following list.
baseline_list=['LBA1MWA-LBA2MWA','LBA2MWA-LBA3MWA','LBA7MWA-LBA8MWA','LBA6MWA-LBA7MWA','LBB2MWA-LBB4MWA','LBA8MWA-Tile165MWA','Tile166MWA-Tile167MWA','Tile101MWA-Tile102MWA','Tile105MWA-Tile106MWA','Tile123MWA-Tile124MWA'] # Give name without spaces. Choose from this list

Details about other INPUT parameters with example

####### INPUT ###########################################################################
array_config='PhaseII' # Does your data come from PhaseII or PhaseI ?. Give 'PhaseI' or 'PhaseII' as input  
make_jpgimgs=True # Boolean input. Do you want JPGs to me made?
want_allDS_jpgs=True # Boolean input. Do you want JPGs to me made for all STOKES DSs and baselines?
want_meanDS=True # Boolean input. Do you want to make baseline-averaged DS?
want_I_map=True # Want to make STOKES I DS?
basedir='/Data1/atul/PSP_MWA_corr_work/1239162208/' #Where MS files are located
MWA_info_dir='/Data/atul/MWA_details/' #Place MWA_antenna_coords_'+array_config+'.csv' files here.
flag_bandedges=True
coarse_chan=1.28 # Bandwidth of a coarse spectral channel of MWA. Usually set to 1.28 MHz

MSNAMES=['1239162208_062-062_2min_8~12.ms/','1239162504_062-062_2min_8~12.ms/','1239162800_062-062_2min_8~12.ms/'] # Leave as [] if you need the code to grab all MSs with a specific name tag from a folder. 
MSNAME_tag='*.ms' #If there are many .ms files which can be picked up by nametag leave the above variable [] and provide the nametag here
POL_LIST = ['XX','YY'] # Use ['XX','YY']
CPOL_LIST=['XX','XY','YX','YY']	# Use ['XX','XY','YX','YY'] in this order if all polarisations exist
DS_pfiledir=basedir+'DS_pfiles/' # Where to save DSs.

'''
import numpy as np
import os,pickle,glob
from datetime import datetime as dt
import matplotlib.pyplot as plt
import numpy.ma as ma
####### INPUT ###########################################################################
array_config='PhaseII' #PhaseII or PhaseI
make_jpgimgs=True
want_allDS_jpgs=True
want_meanDS=True
want_I_map=True
basedir='/Data1/atul/PSP_MWA_corr_work/1239162208/' #Where MS files are located
MWA_info_dir='/Data/atul/MWA_details/' #Place MWA_antenna_coords_'+array_config+'.csv' files here.
#MSNAMES=['1239162208_062-062_2min_8~12.ms/','1239162504_062-062_2min_8~12.ms/','1239162800_062-062_2min_8~12.ms/']
MSNAMES=[]
flag_bandedges=True
coarse_chan=1.28 # Bandwidth of a coarse spectral channel of MWA. Usually set to 1.28 MHz

MSNAME_tag='*.ms' #If there are many .ms files which can be picked up by nametag leave the above variable [] and provide the nametag here
POL_LIST = ['XX','YY'] # Use ['XX','YY']
CPOL_LIST=['XX','XY','YX','YY']	# Use ['XX','XY','YX','YY'] in this order if all polarisations exist
DS_pfiledir=basedir+'DS_pfiles/'
############################# Usable baselines ###############################
baseline_list=['LBA1MWA-LBA2MWA','LBA2MWA-LBA3MWA','LBA7MWA-LBA8MWA','LBA6MWA-LBA7MWA','LBB2MWA-LBB4MWA','LBA8MWA-Tile165MWA','Tile166MWA-Tile167MWA','Tile101MWA-Tile102MWA','Tile105MWA-Tile106MWA','Tile123MWA-Tile124MWA'] # Give name without spaces. Choose from this list
##############################################################################
#baseline_list=['LBA1MWA-LBA2MWA']
########################################################################################################################
polstr='_'.join(CPOL_LIST)+'_'
IDs,names,x,y,z=np.genfromtxt(MWA_info_dir+'MWA_antenna_coords_'+array_config+'.csv',skip_header=True,dtype=str,delimiter=',',usecols=(0,1,9,10,11),unpack=True,autostrip=True)
name2ID=dict(zip(names,IDs))
x=x.astype(float)
y=y.astype(float)
z=z.astype(float)
coords=np.array([(x[i],y[i],z[i]) for i in range(len(x))])
name2coord=dict(zip(names,coords))
id2name=dict(zip(IDs.astype(int),names))
cwd=os.getcwd()
os.chdir(basedir)
if MSNAMES==[]:
	MSNAMES=glob.glob(MSNAME_tag)
os.system('mkdir '+DS_pfiledir)
if len(CPOL_LIST)<4:
	if want_I_map==True:
		want_I_map=False
		print 'Can\'t make I map without all polarisations. So not making I map!!' 
def datetime(MSNAME):		# Returning observation integration time (in seconds),start date,start time, end date and end time (in UT)
	ms.open(MSNAME)
	a= ms.summary()
	start=(qa.time(qa.quantity(a['BeginTime'],'d'),form="ymd"))[0]
	End=(qa.time(qa.quantity(a['EndTime'],'d'),form="ymd"))[0]
	int_time = a['scan_1']['0']['IntegrationTime']
	stt=dt.strptime(start,'%Y/%m/%d/%H:%M:%S')
	endt=dt.strptime(End,'%Y/%m/%d/%H:%M:%S')
	tdt=(endt-stt).total_seconds()
	ms.close()	
	return int_time,stt,endt,tdt

def get_freq(MSNAME):			# Return the start frequency and channel width of the first spectral channel in the data set
	tb.open(MSNAME+'/SPECTRAL_WINDOW')
	Mid_Freq = tb.getcol('REF_FREQUENCY')[0]/(10**6) # conversion from Hz to MHz
	BW=tb.getcol('TOTAL_BANDWIDTH')[0]*10**-6 # BW in MHz
	spec_resol = tb.getcol('CHAN_WIDTH')[0][0]/(10**6) #in MHz
	RefFreq=Mid_Freq-BW/2.
	print 'Mid Freq: ',Mid_Freq
	tb.close()
	return RefFreq,spec_resol,BW

def get_amp(MSNAME,tile1,tile2,POL_LIST):		# Extraction of amplitude of crosscorrelations
	ms.open(MSNAME)
	print "#### Tile1 %03d; Tile2 %03d" % (tile1, tile2)
	print '#### Tile1 %03d; Tile2 %03d; POL_LIST %s' % (tile1, tile2, POL_LIST)
	ms.selectinit(datadescid=0) # Reset any earlier selections
	try:
		ms.select({'antenna1':[tile1],'antenna2':[tile2]})
		ms.selectpolarization(POL_LIST)
		amp=ms.getdata(['amplitude'])['amplitude']
	except:
		amp=None
		print MSNAME,' has no information in ',id2name[tile1],' - ',id2name[tile2],' baseline.'	
	ms.close()
	return amp

def get_phases(MSNAME,tile1,tile2,POL_LIST):	# Extraction of phase of crosscorrelations data along with u,v and w for each time slice.
	ms.open(MSNAME)
	print "#### Tile1 %03d; Tile2 %03d" % (tile1, tile2)
	print '#### Tile1 %03d; Tile2 %03d; POL_LIST %s' % (tile1, tile2, POL_LIST)
	ms.selectinit(datadescid=0) # Reset any earlier selections
	try:
		ms.select({'antenna1':[tile1],'antenna2':[tile2]})
		ms.selectpolarization(POL_LIST)
		phases=ms.getdata(['phase'])['phase']
	except:
		print MSNAME,' has no information in ',id2name[tile1],' - ',id2name[tile2],' baseline.'			
		phases=None	
	#u=ms.getdata(['u'])['u']
	#v=ms.getdata(['v'])['v']
	#w=ms.getdata(['w'])['w']
	ms.close()
	return phases

##################################################################################################################################################

bslns=[]
for i in baseline_list:
	nm1,nm2=i.split('-')
	try:
		tbl=name2coord[nm1]-name2coord[nm2]
		bslns+=[np.sqrt(np.sum(tbl**2))]
	except:
		print
		continue	
bslns=np.array(bslns)
print 'Baselines: ',baseline_list
plt.ioff()
for MSNAME in MSNAMES:
	print 'Analysing ',MSNAME
	DS_subfold=DS_pfiledir+MSNAME.split('.ms')[0]+'_ncrossDS/'
	if not os.path.isdir(DS_subfold):
		os.system('mkdir '+DS_subfold)
	int_time,start_time,end_time,tdt = datetime(MSNAME)
	RefFreq,spec_resol,BW = get_freq(MSNAME)
	count=0
	for bs in baseline_list:
		ang_scale=str(round(300./RefFreq/bslns[count]*180*60/np.pi,2))+' arcmin'	# in arcmin
		tile1,tile2=bs.split('-')
		tile1=int(name2ID[tile1])
		tile2=int(name2ID[tile2])
		a_cor1=get_amp(MSNAME,tile1,tile1,POL_LIST)
		a_cor2=get_amp(MSNAME,tile2,tile2,POL_LIST)
		c_corr=get_amp(MSNAME,tile1,tile2,CPOL_LIST)
		if a_cor1 == None or a_cor2==None or c_corr==None:
			count+=1
			continue	
		n_cross=[None]*len(CPOL_LIST)

		if len(POL_LIST)==1:
			n_cross[0]=c_corr[0]/np.sqrt(a_cor1[0]*a_cor2[0])
		elif CPOL_LIST==['XX','YY']:
			for i in range(2):
				n_cross[i]=c_corr[i]/np.sqrt(a_cor1[i]*a_cor2[i])
		elif len(CPOL_LIST)==4:		
			j=0
			k=0
			for i in range(4):		
				n_cross[i] = c_corr[i]/np.sqrt(a_cor1[j]*a_cor2[k])
				if (i%2==0):
					k+=1
				else:
					j+=1
					k = 0						
		ncross = np.array(n_cross)

		## Flag bad channels ########################
		if flag_bandedges==True:
			Ncoarse=int(BW/coarse_chan)
			minchan=int(coarse_chan/spec_resol)
			M=int(minchan/4)-1
			a=(M+1)*2
			Bcen_crop=int(.12/spec_resol)
			Tot_chans=int(BW/spec_resol)
			st_chan=M+1
			ncross=ma.array(ncross)
			ncross.mask=np.ones(ncross.shape)
			while st_chan<Tot_chans:
				ncross.mask[:,st_chan:a-int(Bcen_crop/2),:]=False
				ncross.mask[:,a+int(Bcen_crop/2)+1:minchan-M,:]=False
				st_chan+=minchan
				a+=minchan
				
		else:
			ncross=ma.array(ncross)	
			ncross.mask=np.zeros(ncross.shape)
		#############################################

		if not np.isfinite(ncross).any():
			print 'Norm. Crosscorrelations aren\'t finite for ',bs
			count+=1
			continue
		pickle.dump([[RefFreq,spec_resol,BW],[start_time,int_time,tdt],ncross,bslns[count],ang_scale,round(RefFreq+BW/2.,3)],open(DS_subfold+'NcrossDS_'+polstr+bs+'.p','wb'))
		if want_I_map==True:
			I_map=0.5*(ncross[0]+ncross[3])
			
			pickle.dump([[RefFreq,spec_resol,BW],[start_time,int_time,tdt],I_map,bslns[count],ang_scale,round(RefFreq+BW/2.,3)],open(DS_subfold+'Ncross_I_mapDS_'+bs+'.p','wb'))
		if make_jpgimgs==True and want_allDS_jpgs==True:
			DS_jpg_dir=DS_subfold+'DS_jpgs/'
			if not os.path.isdir(DS_jpg_dir):
				os.mkdir(DS_jpg_dir)
			nDS=ncross.shape[0]
			for ix in range(nDS):
				plt.imshow(ncross[i],aspect='auto',origin='lower',extent=[0,tdt,0,BW],cmap='jet')				
				plt.xlabel('Time (seconds).   +'+str(start_time)+' UT')
				plt.ylabel(r'$\nu$' +' (MHz)  +'+str(round(RefFreq,2))+' MHz')
				h=plt.colorbar()
				h.set_label('Normalised crosscorrelations')
				plt.title(bs+' ('+CPOL_LIST[ix]+')',size=20)
				plt.savefig(DS_jpg_dir+'Ncross_DS_'+bs+'_'+CPOL_LIST[ix]+'.png')
				plt.close()
			if want_I_map==True:
				plt.imshow(I_map,aspect='auto',origin='lower',extent=[0,tdt,0,BW],cmap='jet')				
				plt.xlabel('Time (seconds).   +'+str(start_time)+' UT')
				plt.ylabel(r'$\nu$' +' (MHz)  +'+str(round(RefFreq,2))+' MHz')
				h=plt.colorbar()
				h.set_label('Normalised crosscorrelations')
				plt.title(bs+' STOKES I',size=20)
				plt.savefig(DS_jpg_dir+'Ncross_I_DS_'+bs+'.png')
				plt.close()				
		count+=1
	if want_meanDS==True:
		allDS=glob.glob(DS_subfold+'NcrossDS*.p')
		if len(allDS)==0:
			continue
		AlDS=np.zeros((len(allDS),ncross.shape[0],ncross.shape[1],ncross.shape[2]))
		for nm in range(len(allDS)):
			tald=pickle.load(open(allDS[nm],'rb'))
			AlDS[nm]=tald[2]
		AlDS=ma.masked_invalid(AlDS)
		mnDS=ma.mean(AlDS,axis=0)
		ang_scale=str(round(300./(RefFreq+BW/2.)/np.mean(bslns)*180*60/np.pi,2))+' arcmin'
		pickle.dump([[RefFreq,spec_resol,BW],[start_time,int_time,tdt],mnDS,np.mean(bslns),ang_scale,round(RefFreq+BW/2.,3)],open(DS_subfold+'Ncross_meanDS_'+polstr+'.p','wb'))		
		if want_I_map==True:
			mnIDS=0.5*(mnDS[0]+mnDS[3])
			pickle.dump([[RefFreq,spec_resol,BW],[start_time,int_time,tdt],mnIDS,np.mean(bslns),ang_scale,round(RefFreq+BW/2.,3)],open(DS_subfold+'Ncross_mean_I_DS.p','wb'))
		if make_jpgimgs==True:
			nDS=mnDS.shape[0]
			for ix in range(nDS):
				plt.imshow(mnDS[ix],aspect='auto',origin='lower',extent=[0,tdt,0,BW],cmap='jet')				
				plt.xlabel('Time (seconds).   +'+str(start_time)+' UT')
				plt.ylabel(r'$\nu$' +' (MHz)  +'+str(round(RefFreq,2))+' MHz')
				h=plt.colorbar()
				h.set_label('Normalised crosscorrelations')
				plt.title('Mean DS ('+CPOL_LIST[ix]+')',size=20)
				plt.savefig(DS_jpg_dir+'Ncross_meanDS_'+CPOL_LIST[ix]+'.png')
				plt.close()
			if want_I_map==True:
				plt.imshow(mnIDS,aspect='auto',origin='lower',extent=[0,tdt,0,BW],cmap='jet')				
				plt.xlabel('Time (seconds).   +'+str(start_time)+' UT')
				plt.ylabel(r'$\nu$' +' (MHz)  +'+str(round(RefFreq,2))+' MHz')
				h=plt.colorbar()
				h.set_label('Normalised crosscorrelations')
				plt.title('Mean STOKES I DS',size=20)
				plt.show()
				plt.savefig(DS_jpg_dir+'Ncross_mean_I_DS'+'.png')
				plt.close()
							
os.chdir(cwd)
