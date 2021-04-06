#!/usr/bin/python
#encoding=utf-8

__author__ = 'Ruchao Fan'

import random
import math
import torch
import numpy as np
#import librosa
#import torchaudio

common_incorrect_voc = {
    't': ['r', 'l', 'n', 'ah', 'z', 'uw', 'dh', 's', 'th', 'f', 'sh', 'p', 'ch', 'ae', 'd', 'eh', 'k', 'sil', 'er', 'v'], 
    'ah': ['l', 'z', 'uw', 'uh', 'ao', 'ay', 'ih', 'ae', 'aa', 'd', 'eh', 'ow', 'iy', 'sil', 'ey', 'aw', 'er', 't', 'b'],
    'v': ['k', 'r', 'w', 'sil', 'l', 's', 'p', 'f', 'er', 'b'], 
    'iy': ['jh', 'sil', 'er', 'ah', 'ey', 'uw', 'ay', 'ih', 'aw', 'y', 'eh', 'ow'], 
    'l': ['r', 'w', 'sil', 'n', 'iy', 'ah', 'z', 'f', 'ih', 'er', 't', 'eh'], 
    'r': ['w', 'sil', 'l', 'n', 'uh', 'iy', 'ah', 'ao', 'z', 'ey', 'aa', 'ih', 'er', 'd'], 
    'sil': ['r', 'l', 'n', 'ah', 'z', 'uw', 'dh', 'w', 's', 'uh', 'ao', 'f', 'sh', 'ih', 'm', 'y', 'jh', 'p', 'ae', 'aa', 'ng', 'd', 'eh', 'k', 'iy', 'hh', 'g', 'er', 'v', 't', 'b'], 
    'dh': ['r', 'hh', 'sil', 'l', 's', 'n', 'th', 'p', 'z', 'y', 'er', 'd', 't', 'eh'], 
    'ae': ['sil', 'ao', 'ah', 'ey', 'ay', 'aa', 'ih', 'aw', 't', 'eh'], 
    'ow': ['iy', 'r', 'sil', 'w', 'uh', 'ao', 'ah', 'uw', 'aa', 'ih', 'oy', 'aw', 'er'], 
    'p': ['k', 'sil', 'f', 'er', 'v', 't', 'b'], 
    'er': ['iy', 'r', 'sil', 'l', 'w', 'uh', 'ao', 'ah', 'uw', 'aa', 'eh', 'ow'], 
    'd': ['r', 'l', 'n', 'ah', 'z', 'dh', 's', 'zh', 'th', 'f', 'jh', 'p', 'ng', 'eh', 'k', 'iy', 'sil', 'g', 'er', 'v', 't', 'b'], 
    'ch': ['jh', 'sil', 'zh', 's', 'dh', 'sh', 't'], 
    'ih': ['iy', 'r', 'sil', 'n', 'uh', 'ah', 'ey', 'ae', 'ay', 'aa', 'uw', 'er', 'eh'], 
    's': ['k', 'hh', 'sil', 'zh', 'th', 'z', 'sh', 't'], 
    'z': ['r', 'jh', 'sil', 's', 'zh', 'g', 'th', 'f', 'dh', 'sh', 'er', 't'], 
    'aa': ['sil', 'ao', 'ah', 'ae', 'uw', 'aw', 'er', 'eh', 'ow'], 
    'g': ['k', 'jh', 'hh', 'sil', 'er', 'd', 'b'], 
    'ng': ['sil', 'n', 'l', 'uh', 'm'], 
    'n': ['hh', 'sil', 'l', 'p', 'z', 'f', 'ng', 'm', 'y', 'v', 'd'], 
    'hh': ['k', 'jh', 'sil', 'g', 'er', 'ch', 'sh', 'y', 't'], 
    'jh': ['k', 'sil', 'zh', 's', 'g', 'ch', 'sh', 'y', 'er', 'd', 't'], 
    'uh': ['ao', 'ah', 'uw', 'ih', 'er', 'ow'], 
    'eh': ['iy', 'r', 'sil', 'ah', 'ey', 'ae', 'ay', 'aa', 'uw', 'ih', 'er', 'ow'], 
    'uw': ['iy', 'w', 'sil', 'l', 'uh', 'ah', 'ao', 'aa', 'ih', 'oy', 'ow'], 
    'ey': ['iy', 'sil', 'ah', 'ae', 'ay', 'aa', 'ih', 'eh'], 
    'b': ['r', 'sil', 'ah', 'p', 'f', 'v', 't'], 
    'k': ['hh', 'w', 'sil', 's', 'g', 'ch', 'dh', 'er', 't'], 
    'aw': ['uh', 'ao', 'ah', 'ay', 'aa', 'ow'], 
    'ay': ['iy', 'r', 'sil', 'ah', 'ey', 'ae', 'aa', 'ih', 'oy', 'eh'], 
    'sh': ['sil', 'zh', 's', 'ch', 't'], 
    'zh': ['jh', 's', 'z', 'ch', 'sh'], 
    'y': ['jh', 'iy', 'sil', 'ih', 'er'], 
    'f': ['sil', 'p', 'er', 'v', 'b'], 
    'th': ['sil', 's', 'p', 'z', 'ch', 'f', 'er', 'd', 't'], 
    'ao': ['sil', 'l', 'uh', 'ah', 'uw', 'ae', 'aa', 'aw', 'er', 'eh', 'ow'], 
    'm': ['ng', 'sil', 'n'], 
    'w': ['hh', 'sil', 'l', 'g', 'r', 'ao', 'y', 'v'], 
    'oy': ['ao', 'ow', 'ay']
}

vowels = ['iy', 'aa', 'ae', 'eh', 'ah', 'ao', 'ih', 'ey', 'aw', 'ay', 'er', 'uw', 'uh', 'oy', 'ow']
consonants = ['w', 'dh', 'y', 'hh', 'ch', 'jh', 'th', 'zh', 'd', 'ng', 'b', 'g', 'f', 'k', 'm', 'l', 'n', 's', 'r', 't', 'v', 'z', 'p', 'sh']
"""
index2word = {0: 'blank', 1: 'UNK', 2: 'sil', 3: 'ah', 4: 's', 5: 'uw', 6: 'm', 7: 'f', 8: 'ao', 9: 'r', 10: 'ih', 11: 'z', 12: 'ae', 13: 'p', 14: 'uh', 15: 'l', 16: 'ch', 17: 'ey', 18: 'sh', 19: 'n', 20: 'w', 21: 'eh', 22: 'er', 23: 'aa', 24: 'hh', 25: 'k', 26: 'iy', 27: 'ng', 28: 'd', 29: 'dh', 30: 'aw', 31: 'ay', 32: 'v', 33: 'ow', 34: 'b', 35: 'th', 36: 'g', 37: 'y', 38: 'jh', 39: 't', 40: 'oy', 41: 'zh', 42:'err'}
"""
"""
word2index = {'blank': 0, 'UNK': 1, 'sil': 2, 'ah': 3, 's': 4, 'uw': 5, 'm': 6, 'f': 7, 'ao': 8, 'r': 9, 'ih': 10, 'z': 11, 'ae': 12, 'p': 13, 'uh': 14, 'l': 15, 'ch': 16, 'ey': 17, 'sh': 18, 'n': 19, 'w': 20, 'eh': 21, 'er': 22, 'aa': 23, 'hh': 24, 'k': 25, 'iy': 26, 'ng': 27, 'd': 28, 'dh': 29, 'aw': 30, 'ay': 31, 'v': 32, 'ow': 33, 'b': 34, 'th': 35, 'g': 36, 'y': 37, 'jh': 38, 't': 39, 'oy': 40, 'zh': 41, 'err':42}
"""
index2word = {0: 'blank',
 1: 'UNK',
 2: 'sil',
 3: 'sh',
 4: 'iy',
 5: 'hh',
 6: 'ae',
 7: 'd',
 8: 'y',
 9: 'er',
 10: 'aa',
 11: 'r',
 12: 'k',
 13: 's',
 14: 'uw',
 15: 't',
 16: 'ih',
 17: 'n',
 18: 'g',
 19: 'w',
 20: 'ao',
 21: 'dh',
 22: 'l',
 23: 'ow',
 24: 'm',
 25: 'eh',
 26: 'oy',
 27: 'ay',
 28: 'b',
 29: 'v',
 30: 'f',
 31: 'z',
 32: 'th',
 33: 'ah',
 34: 'p',
 35: 'ey',
 36: 'ng',
 37: 'ch',
 38: 'uh',
 39: 'zh',
 40: 'jh',
 41: 'aw',
 42: 'err'}

word2index = {'blank': 0,
 'UNK': 1,
 'sil': 2,
 'sh': 3,
 'iy': 4,
 'hh': 5,
 'ae': 6,
 'd': 7,
 'y': 8,
 'er': 9,
 'aa': 10,
 'r': 11,
 'k': 12,
 's': 13,
 'uw': 14,
 't': 15,
 'ih': 16,
 'n': 17,
 'g': 18,
 'w': 19,
 'ao': 20,
 'dh': 21,
 'l': 22,
 'ow': 23,
 'm': 24,
 'eh': 25,
 'oy': 26,
 'ay': 27,
 'b': 28,
 'v': 29,
 'f': 30,
 'z': 31,
 'th': 32,
 'ah': 33,
 'p': 34,
 'ey': 35,
 'ng': 36,
 'ch': 37,
 'uh': 38,
 'zh': 39,
 'jh': 40,
 'aw': 41,
 'err': 42}
def load_audio(path):
    """
    Args:
        path     : string 载入音频的路径
    Returns:
        sound    : numpy.ndarray 单声道音频数据，如果是多声道进行平均
    """
    sound, _ = torchaudio.load(path)
    sound = sound.numpy()
    if len(sound.shape) > 1:
        if sound.shape[1] == 1:
            sound = sound.squeeze()
        else:
            sound = sound.mean(axis=1)
    return sound

def load_wave(path, normalize=True):
    """
    Args:
        path     : string 载入音频的路径
    Returns:
    """
    sound = load_audio(path)
    wave = torch.FloatTensor(sound)
    if normalize:
        mean = wave.mean()
        std = wave.std()
        wave.add_(-mean)
        wave.div_(std)
    return wave

def F_Mel(fre_f, audio_conf):
    '''
    Input:
        fre_f       : FloatTensor log spectrum
        audio_conf  : 主要需要用到采样率
    Output:
        mel_f       : FloatTensor  换成mel频谱
    '''
    n_mels = fre_f.size(1)
    mel_bin = librosa.mel_frequencies(n_mels=n_mels, fmin=0, fmax=audio_conf["sample_rate"]/2) * audio_conf["window_size"]
    count = 0
    fre_f = fre_f.numpy().tolist()
    mel_f = []
    for frame in fre_f:
        mel_f_frame = []
        for i in range(n_mels):
            left = int(math.floor(mel_bin[i]))
            right = left + 1
            tmp = (frame[right] - frame[left]) * (mel_bin[i] - left) + frame[left]      #线性插值
            mel_f_frame.append(tmp)
        mel_f.append(mel_f_frame)
    return torch.FloatTensor(mel_f)

def make_context(feature, left, right):
    if left==0 and right == 0:
        return feature
    feature = [feature]
    for i in range(left):
        feature.append(np.vstack((feature[-1][0], feature[-1][:-1])))
    feature.reverse()
    for i in range(right):
        feature.append(np.vstack((feature[-1][1:], feature[-1][-1])))
    return np.hstack(feature)

def skip_feat(feature, skip):
    '''
    '''
    if skip == 1 or skip == 0:
        return feature
    skip_feature=[]
    for i in range(feature.shape[0]):
        if i % skip == 0:
            skip_feature.append(feature[i])
    return np.vstack(skip_feature)

def spec_augment(mel_spectrogram, frequency_mask_num=1, time_mask_num=1, frequency_masking_para=2, time_masking_para=5):
    """
    frequency_mask_num = random.randint(1, frequency_mask_num+1)
    time_mask_num = random.randint(1, time_mask_num+1)
    frequency_masking_para = random.randint(1, frequency_masking_para+1)
    time_masking_para = random.randint(1, time_masking_para+1)
    """
    tau = mel_spectrogram.shape[0]
    v = mel_spectrogram.shape[1]
    
    warped_mel_spectrogram = np.array(mel_spectrogram)
    
    # Frequency masking 
    if( frequency_mask_num > 0 ):
        for i in range(frequency_mask_num):
            f = np.random.uniform(low=0.0, high=frequency_masking_para)
            f = int(f)
            f0 = random.randint(0, v - f)
            warped_mel_spectrogram[:, f0:f0 + f] = 0
    # Time masking 
    if time_mask_num > 0:
        for i in range(time_mask_num):
            t = np.random.uniform(low=0.0, high=time_masking_para)
            t = int(t)
            t0 = random.randint(0, tau - t)
            warped_mel_spectrogram[t0:t0 + t, :] = 0
    return warped_mel_spectrogram


def process_label_file(label_file, label_type, class2int):
    '''
    Input:
        label_file  : string  标签文件路径
        label_type  : string  标签类型(目前只支持字符和音素)
        class2int   : dict    标签和数字的对应关系
    Output:
        label_dict  : dict    所有句子的标签，每个句子是numpy类型
    '''
    label_dict = dict()
    f = open(label_file, 'r')
    for label in f.readlines():
        label = label.strip()
        label_list = []
        if label_type == 'char':
            utt = label.split('\t', 1)[0]
            label = label.split('\t', 1)[1]
            for i in range(len(label)):
                if label[i].lower() in class2int:
                    label_list.append(class2int[label[i].lower()])
                if label[i] == ' ':
                    label_list.append(class2int['SPACE'])
        else:
            label = label.split()
            utt = label[0]
            for i in range(1,len(label)):
                label_list.append(class2int[label[i]])
        label_dict[utt] = label_list
    f.close()
    return label_dict


def data_enhancement(phone, mutation_prob=0.1, enhancement_type=1, phone_num = 42):
    """
    Function:
        data enhancement
    parameters:
        phone: the norm phone(int)
        mutation_prob: the probability of phone mutations(0<= mutation_prob <= 1)
        enhancement_type: the type of enhancement(1/2/3/4)
                          type 1: Enhancement based on consonant and vowel
                          type 2: Enhancement based on data distribution
                          type 3: Enhancement based on literally random
                          type 4: Enhancement based on setting zero
    return:
        mutation_phone: mutation phone
    """
    mutation_phone = phone
    
    if enhancement_type == 1:
        # random mutation
        if random.random() < mutation_prob:
            # substite from vowels
            if index2word[mutation_phone] in vowels:
                mutation_phone = word2index[random.choice(vowels)]
            # substite from consonants
            elif index2word[mutation_phone] in consonants:
                # get the consonants phone
                consonants_phone = random.choice(consonants)
                # get the index of the consonants_phone
                mutation_phone = word2index[consonants_phone]
        
    elif enhancement_type == 2:
        # random mutation
        if random.random() < mutation_prob:
            # substite from common incorrect phones
            if index2word[mutation_phone] in common_incorrect_voc.keys():
                mutation_phone = index2word[mutation_phone]
                # get the common incorrect phone
                common_incorrect_phone = random.choice(common_incorrect_voc[mutation_phone])
                # transfer phone to index
                common_incorrect_phone_index = word2index[common_incorrect_phone]
                mutation_phone = common_incorrect_phone_index
            else:
                pass
        else:
            pass
    elif enhancement_type == 3:
        if random.random() < mutation_prob:
            mutation_phone = (phone + random.randint(0, phone_num)) % phone_num
        else:
            pass
    elif enhancement_type == 4:
        if random.random() < mutation_prob:
            mutation_phone = 0
        else:
            pass
    """
    if random.random() < .05:
            mutation_phone = word2index['blank']
            
    if random.random() < 0.05:
        if random.random() < .5:
            mutation_phone = [mutation_phone, (phone + random.randint(0, phone_num)) % phone_num]
        else:
            mutation_phone = [(phone + random.randint(0, phone_num)) % phone_num, mutation_phone]
    else:
        mutation_phone = [mutation_phone]
    """
    mutation_phone = [mutation_phone]
    return mutation_phone

'''
if __name__ == '__main__':
    import scipy.signal
    windows = {'hamming':scipy.signal.hamming, 'hann':scipy.signal.hann, 'blackman':scipy.signal.blackman,
            'bartlett':scipy.signal.bartlett}
    audio_conf = {"sample_rate":16000, 'window_size':0.025, 'window_stride':0.01, 'window': 'hamming'} 
    path = '/home/fan/Audio_data/TIMIT/test/dr7/fdhc0/si1559.wav'
    spect = parse_audio(path, audio_conf, windows, normalize=True)
    mel_f = F_Mel(spect, audio_conf)
    wave = load_wav(path)
    print(wave)

    import visdom
    viz = visdom.Visdom(env='fan')
    viz.heatmap(spect.transpose(0, 1), opts=dict(title="Log Spectrum", xlabel="She had your dark suit in greasy wash water all year.", ylabel="Frequency"))
    viz.heatmap(mel_f.transpose(0, 1), opts=dict(title="Log Mel Spectrum", xlabel="She had your dark suit in greasy wash water all year.", ylabel="Frequency"))
    viz.line(wave.numpy())
'''

