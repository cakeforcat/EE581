<pre>
Data from the fetch script is stored as follows:

.
├── CAS_original           
│   ├── Moxitaidi (UAV-0.6m)
│   │   ├── img
│   │   └── mask
│   ├── Moxitaidi (UAV-1m)
│   ├── ...
│   └── Wenchuan
├── landslide4sense_original           
│   ├── TrainData
│   │   ├── img
│   │   └── mask
│   ├── TestData
│   └── ValidData
│
└── median_filtered		# all median filtered images in here
    ├── Moxitaidi (UAV-0.6m)
    │   └── img
    ├── Moxitaidi (UAV-1m)
    ├── ...
    └── Wenchuan

The idea is to have an exact copy of the original dataset structure for each
script that outputs the modifications of the original images.

The green quantisation analysis, hsv analysis and superpixel analysis can be executed by running the ‘hsv_gq_sp_for_mask.mlx’ located in ‘\src\classical_methods’. All output graphs will be located within ‘\data\green_quant_filtering’ , ‘\data\hsv_analysis’ and ‘\data\superpixel_analysis’ respectively. However, a ‘Stats_classical_methods.txt’ file must be created under ‘\data\’. 
The glcm_svm analysis can be executed by running the ‘Sense_GLCM_SVM’.mlx located in ‘\src\classical_methods\SVM\’. Note all output graphs will be located within ‘\data\glcm_svm. However, a ‘Stats_classical_methods.txt’ file must be created under ‘\data\’.


</pre>