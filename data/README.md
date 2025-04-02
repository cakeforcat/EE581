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

</pre>