# ISLES'22: Ischemic Stroke Lesion Segmentation Challenge

![alt text](https://github.com/ezequieldlrosa/isles22/blob/main/isles-logo.png)

## Aims
Infarct segmentation in ischemic stroke is crucial at i) acute stages to guide treatment decision making (whether to reperfuse or not, and type of treatment) and at ii) sub-acute and chronic stages to evaluate the patients' disease outcome, for their clinical follow-up and to define optimal therapeutical and rehabilitation strategies to maximize critical windows for recovery.
This challenge task aims to benchmark infarct segmentation in acute and sub-acute stroke using multimodal MRI data, namely DWI, ADC and FLAIR images. ISLES'22 differs from the previous challenge editions in ischemic stroke by i) targeting the delineation of not only large infarct lesions, but also of multiple embolic and/or cortical infarcts (typically seen after mechanical recanalization), ii) by evaluating both pre- and post- interventional MRI images and iii) by including ~3x more data than ISLES'15 (a previous challenge edition with similar aims).
From a clinical perspective, ISLES'22 focuses on the clinical growing interest of acute embolic infarct patterns, both pre-intervention (i.e. at a very early disease state) and post-intervention (typical, post-interventional sub-acute infarct patterns not restricted to a single vessel territory). This clinical problem also challenges the participants from a technical perspective: teams will deal with a wider ischemic stroke disease spectra, involving variable lesion size and burden, more complex infarct patterns and variable anatomically located lesions in data from multiple centers.


## Challenge task
The goal of this challenge is to evaluate automated methods of stroke lesion segmentation in MR images. Participants are tasked with automatically generating lesion segmentation masks from DWI, ADC and FLAIR MR modalities. The task consist on a single phase of algorithms evaluation. Participants will submit their segmentation model ("algorithm") via a Docker container which will then be used to generate predictions on a hidden dataset.

## Data
You can access ISLES'22 data after registration to the [challenge](https://isles22.grand-challenge.org/).
Data is organized following the Brain Imaging Data Structure (BIDS; https://bids.neuroimaging.io/) and contains 4 image files (ADC, DWI, FLAIR and ground-truth), 1 snapshot and (when available) accompanying .json files for the images.

A single case-sample is structured as follows:
```
+-- rawdata
|   +-- sub-strokecase0009
|       +-- ses-0001
|           +-- sub-strokecase0009_ses-0001_adc.nii.gz 
|           +-- sub-strokecase0009_ses-0001_adc.json 
|           +-- sub-strokecase0009_ses-0001_dwi.nii.gz
|           +-- sub-strokecase0009_ses-0001_dw.json 
|           +-- sub-strokecase0009_ses-0001_flair.nii.gz
|           +-- sub-strokecase0009_ses-0001_flair.json
+-- derivatives
|   +-- sub-strokecase0009
|       +-- ses-0001
|           +-- sub-strokecase0009_ses-0001_msk.nii.gz
|           +-- sub-strokecase0009_ses-0001_snp.png
```

## Performance evaluation
Metrics used in this challenge are found in utils/eval_utils and are also used to rank the teams in the challenge:
* Dice Score 
* Absolute volume difference
* Absolute lesion count difference
* Lesion-wise F1-Score

For information about the ranking computation, please check the challenge [document](https://zenodo.org/record/6362388#.YpW-mJNBxQJ).

## Getting started
A Jupyter notebook is provided to get started with ISLES'22. The notebook will guide you through the data loading process and performance evaluation of a simple segmentation approach.

## Citation
Please cite the followings works when using ISLES'22 dataset:

de la Rosa, E., Reyes, M., Liew, S. L., Hutton, A., Wiest, R., Kaesmacher, J., ... & Wiestler, B. (2024). A Robust Ensemble Algorithm for Ischemic Stroke Lesion Segmentation: Generalizability and Clinical Utility Beyond the ISLES Challenge. arXiv preprint arXiv:2403.19425.

Hernandez Petzsche, M. R., de la Rosa, E., Hanning, U., Wiest, R., Valenzuela, W., Reyes, M., ... & Kirschke, J. S. (2022). ISLES 2022: A multi-center magnetic resonance imaging stroke lesion segmentation dataset. Scientific data, 9(1), 762.




## License
The ISLES'22 dataset is provided under the CC BY-SA 4.0 License.
The ISLES'22 repository is under the MIT License.

## Contact
Please email [Ezequiel de la Rosa](ezequiel.delarosa@icometrix.com) for questions not fitting in a Github issue.
