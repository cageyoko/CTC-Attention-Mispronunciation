#!/bin/bash

if [ $# -ne 2 ]; then
   echo "Need directory of TIMIT dataset !"
   exit 1;
fi

conf_dir=`pwd`/conf
prepare_dir=`pwd`/data
map_file=$conf_dir/phones.60-48-39.map
phoneme_map=$2

. path.sh
sph2pipe=$KALDI_ROOT/tools/sph2pipe_v2.5/sph2pipe
if [ ! -x $sph2pipe ]; then
   echo "Could not find (or execute) the sph2pipe program at $sph2pipe";
   exit 1;
fi

#根据数据库train，test的名称修改，有时候下载下来train可能是大写或者是其他形式
train_dir=train
test_dir=test

ls -d "$1"/*/dr*/* | sed -e "s:^.*/::" > $conf_dir/train_timit_spk.list

tmpdir=`pwd`/tmp
mkdir -p $tmpdir $prepare_dir
for x in train_timit; do
  if [ ! -d $prepare_dir/$x ]; then
      mkdir -p $prepare_dir/$x
  fi

  # 只使用 si & sx 的语音.
  find $1/{$train_dir,$test_dir}  -iname '*.WAV' \
    | grep -f $conf_dir/${x}_spk.list > $tmpdir/${x}_sph.flist

  #获得每句话的id标识
  sed -e 's:.*/\(.*\)/\(.*\).WAV$:\1_\2:i' $tmpdir/${x}_sph.flist \
    > $tmpdir/${x}_sph.uttids
  
  #生成wav.scp,即每句话的音频路径
  paste -d" " $tmpdir/${x}_sph.uttids $tmpdir/${x}_sph.flist \
    | sort -k1,1 > $prepare_dir/$x/wav.scp
   
  awk '{printf("%s '$sph2pipe' -f wav %s |\n", $1, $2);}' < $prepare_dir/$x/wav.scp > $prepare_dir/$x/wav_sph.scp

  for y in wrd phn; do
    find $1/{$train_dir,$test_dir}  -iname '*.'$y'' \
        | grep -f $conf_dir/${x}_spk.list > $tmpdir/${x}_txt.flist
    sed -e 's:.*/\(.*\)/\(.*\).'$y'$:\1_\2:i' $tmpdir/${x}_txt.flist \
        > $tmpdir/${x}_txt.uttids
    while read line; do
        [ -f $line ] || error_exit "Cannot find transcription file '$line'";
        cut -f3 -d' ' "$line" | tr '\n' ' ' | sed -e 's: *$:\n:'
    done < $tmpdir/${x}_txt.flist > $tmpdir/${x}_txt.trans
  
    #将句子标识（uttid）和文本标签放在一行并按照uttid进行排序使其与音频路径顺序一致
    paste -d" " $tmpdir/${x}_txt.uttids $tmpdir/${x}_txt.trans \
        | sort -k1,1 > $tmpdir/${x}.trans
  
    #生成文本标签
    cat $tmpdir/${x}.trans | sort > $prepare_dir/$x/${y}_text || exit 1;
    if [ $y == phn ]; then 
        cp $prepare_dir/$x/${y}_text $prepare_dir/$x/${y}_text.tmp
        python local/normalize_phone.py --map $map_file --to $phoneme_map --src $prepare_dir/$x/${y}_text.tmp --tgt $prepare_dir/$x/${y}_text
        rm -f $prepare_dir/$x/${y}_text.tmp
        cp $prepare_dir/$x/${y}_text $prepare_dir/$x/transcript_${y}_text
    fi
  done
done

rm -rf $tmpdir

echo "Data preparation succeeded"
