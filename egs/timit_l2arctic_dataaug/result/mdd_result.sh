# need  1. 跟读文本音素序列 ref
#       2. CTC识别序列 hyp
#       3. 专家标注序列 human_seq 

#step1 计算PER
compute-wer --text --mode=present ark:human_seq ark:hyp > per || exit 1;

#step2 计算Recall and Precision
# note : sequence only have 39 phoneme, no sil
align-text ark:ref  ark:human_seq ark,t:- | utils/scoring/wer_per_utt_details.pl > ref_human_detail
align-text ark:human_seq  ark:hyp ark,t:- | utils/scoring/wer_per_utt_details.pl > human_our_detail
align-text ark:ref  ark:hyp ark,t:- | utils/scoring/wer_per_utt_details.pl > ref_our_detail
python utils/scoring/ins_del_sub_cor_analysis.py
rm -rf ref_human_detail human_our_detail ref_our_detail



