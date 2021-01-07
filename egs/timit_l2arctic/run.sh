#!/bin/bash

#Author: Kaiqi Fu, JinHong Lin
. path.sh

stage=-1



l2arctic_dir="/home/ljh/data/L2-Arctic/data" 
timit_dir='/bigdata/DB_PUBLIC/udisk/timit'
phoneme_map='60-39'
feat_dir='data'                            #dir to save feature
feat_type='fbank'                          #fbank, mfcc, spectrogram
config_file='conf/ctc_config.yaml'

if [ ! -z $1 ]; then
    stage=$1
fi

if [ $stage -le 0 ]; then
    echo "Step 0: Data Preparation ..."

    local/timit_data_prep.sh $timit_dir $phoneme_map || exit 1;
    python3 local/l2arctic_prep.py --l2_path=$l2arctic_dir --save_path=${feat_dir}/l2_train  
    python3 local/l2arctic_prep.py --l2_path=$l2arctic_dir --save_path=${feat_dir}/l2_dev  
    python3 local/l2arctic_prep.py --l2_path=$l2arctic_dir --save_path=${feat_dir}/l2_test
    mv ${feat_dir}/l2_dev ${feat_dir}/dev  
    mv ${feat_dir}/l2_test ${feat_dir}/test
    local/timit_l2_merge.sh ${feat_dir}/train_timit ${feat_dir}/l2_train ${feat_dir}/train
    rm -rf l2_train train_timit

    python3 steps/get_model_units.py $feat_dir/train_timit/phn_text
    exit 1;
fi
if [ $stage -le 1 ]; then
    echo "Step 1: Feature Extraction..."
    steps/make_feat.sh $feat_type $feat_dir || exit 1;
fi
if [ $stage -le 2 ]; then
    echo "Step 2: Acoustic Model(CTC) Training..."
    CUDA_VISIBLE_DEVICE='0' python3 steps/train_ctc.py --conf $config_file || exit 1;
fi


if [ $stage -eq 3 ]; then
    echo "Step 3: LM Model Training..."
    steps/train_lm.sh $feat_dir || exit 1;
fi

if [ $stage -le 4 ]; then
    echo "Step 4: Decoding..."
    CUDA_VISIBLE_DEVICE='0' python3 steps/test_ctc_nosil.py --conf $config_file || exit 1;
fi

