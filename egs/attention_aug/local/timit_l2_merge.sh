#!/bin/bash
if [ $# -ne 3 ]; then
   echo "need timit and l2 train dataset !"
   exit 1;
fi
echo "start merge ..."
timit_train_dir=$1
l2_dir=$2
new_dir=$3
mkdir $new_dir
for x in phn_text transcript_phn_text wav.scp wav_sph.scp wrd_text ; do
	cat ${timit_train_dir}/$x   ${l2_dir}/$x  > ${new_dir}/$x
done
echo "Merge succeeded"

