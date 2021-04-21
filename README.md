“A Full Text-Dependent End to End Mispronunciation Detection and Diagnosis with Easy Data Augment Techniques“
https://arxiv.org/pdf/2104.08428.pdf

Implemented with TIMIT and L2-Arctic Database:

TIMIT :  -  
L2-Arctic: (https://psi.engr.tamu.edu/l2-arctic-corpus/)

Note:  
CNN-RNN-CTC is baseline.  
attention_aug is our best system.

Usage: 
1. ./run.sh  get the decode sequence (decode_seq)
2. mv decode_seq ./result/hyp
   ./mdd_result.sh
