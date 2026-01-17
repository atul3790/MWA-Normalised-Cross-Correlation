# MWA-uncalibrated-solar-dynamic-spectrum
This workflow will help generate normalised cross correlation (NCC) dynamic spectrum (DS) using short baselines in MWA Phase I and Phase II data. The idea is that since the Sun is unresolved in these baselines, the NCC values should reflect the total solar disk-integrated flux variability. The user can choose the baselines from a selected list mentioned in ```Make_normCC_DS.py```.
baseline_list=['LBA1MWA-LBA2MWA','LBA2MWA-LBA3MWA','LBA7MWA-LBA8MWA','LBA6MWA-LBA7MWA','LBB2MWA-LBB4MWA','LBA8MWA-Tile165MWA','Tile166MWA-Tile167MWA','Tile101MWA-Tile102MWA','Tile105MWA-Tile106MWA','Tile123MWA-Tile124MWA'] # Give name without spaces. 
**Note**: MWA Tiles (or antenna elements) with the name starting with 'LB' should be omitted if one is using Phase I data. Please check your Measurement set before choosing the baselines. In anycase, code will not crash if some wrong antennas are mentioned in the list.  

There are 3 codes in this workflow.

1. ```Make_normCC_DS.py```
   
   **Input:** Provide the list of short baselines, a folder with all the MWA measurement sets (MSs) belonging to the Picket fence/harmonic/continuous observation under study. Ensure that all MSs for the observation window are stored in a single folder. Provide a location for DS files to be saved.

   **Task & Output:** NCC will be computed for each baseline and MS file. Pickle files containing information on NCC DS (NCC value vs frequency & flux, baseline information) for each baseline and the baseline-averaged NCC DS data will be saved for every MS file in separate folders at a user-specified location. JPGs of every DS file (for each baseline and the baseline-averaged case) per MS file will also be saved.

   *Note:* DS will be made for XX, YY, XY, YX, and STOKES I.

2. ```organise_DS_in1place.py```

   **Input:** Provide the location where DS pickle files are stored, which is the same as the input location in the earlier code. Mention the choice of polarisation in `stokes' keyword (XX, YY, XY, YX, or I) and a folder location where to save all mean NCC DS files for chosen polarization after processing.

   **Task:** The code will grab the baseline-averaged NCC pickle files for every MS from the respective subfolders within the main DS file location (This directory tree will already be created by Make_normCC_DS.py). This code will identify the mean NCC DS in the requested STOKES parameter and will store the files at the user-specified location under a standard nomenclature recognised by the next code.

3. ```make_collageDS.py```

   **Input:** Location where all mean DS are stored by the earlier code.

   **Task:** The code takes in all mean DSs at the location and make the plot with either a common colorbar or separate colorbars for every MS file within the observing window at various frequency bandwidths.   
