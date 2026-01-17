# MWA-Normalised-Cross-Correlation
This workflow will help generate normalised cross correlation (NCC) dynamic spectrum (DS) using short baselines in MWA Phase I and Phase II data. The user can choose the baselines from a selected list.

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
