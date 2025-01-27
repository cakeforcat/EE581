Store the dataset as follows locally:

	|-- original_dataset
	| 	 |
	|	 |-- Moxitaidi (UAV-0.6m)
	|	 |    |
	|    |    |-- img
	|	 |
	|	 |-- Moxitaidi (UAV-1m)
	|	 |-- ...
	|	 |-- Wenchuan
	|
	|
	|-- median_filtered (all median filtered images in here)
		 |
		 |-- Moxitaidi (UAV-0.6m)
	 	 |    |
	     |    |-- img
		 |
		 |-- Moxitaidi (UAV-1m)
		 |-- ...
		 |-- Wenchuan


The idea is to have an exact copy of the original dataset structure for each
script that outputs the modifications of the original images.