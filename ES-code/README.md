# Early-warning signals of disease transitions
Code to accompany "Early-warning signals of infectious disease transitions: a review".

## Abstract
Early warning signals (EWS) are a group of statistical time series signals which could be used to anticipate a critical transition before it is reached. EWS are model-independent methods, that have grown in popularity to support evidence of disease emergence and disease elimination. Theoretical work has demonstrated their capability of detecting disease transitions in simple epidemic models where elimination is reached through vaccination, to more complex vector transmission, age-structured and metapopulation models. However, the exact time-evolution of EWS depends on the transition;  here we review the literature to provide guidance on what trends to expect and when. Recent advances include methods which detect when an EWS becomes significant; where the earlier an upcoming disease transition is detected, the more valuable EWS will be in practice. We suggest that future work should firstly validate detection methods with synthetic and historical datasets, before addressing their performance with real-time data which is accruing. A major challenge to overcome for the use of EWS with disease transitions is to maintain the accuracy of EWS in data poor settings. We demonstrate how EWS behave on reported cases for pertussis in the USA, to highlight some limitations when detecting disease transitions with real-world data. 


## Usage

The requirements.txt file lists all Python libraries that the notebooks depend on.

### ews_theory_figs.ipynb
- ipynb notebook using Python
- Creates figures 1, 2a and 2b

### pertussiss_example.ipynb
- ipynb notebook using Python
- Creates figures 3 and 4, and supplementary figures
- Data exploration 
