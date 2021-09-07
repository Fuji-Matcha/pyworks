#coding utg-8
#divided by zero warningは気にしない

import sys
import numpy as np
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#N:サンプル数, Fs:サンプリング周波数
def fft(data, N, Fs):
    
    D = np.abs(np.fft.fft(data))/N
    # D = D/N * 2 #振幅 交流成分はデータ数で割り2倍する
    # D[0] = D[0]/2 #直流成分
    D[0] = 0
    ydb = 20*np.log10(D/max(D)) #振幅のdBFsへの変換
    ydb[ydb<-160] = -160 #-160dBFs未満を-160へ切り上げ
    x = np.linspace(0, 1.0*Fs, N)

    #図の整形
    # plt.xlabel("freqency [Hz]", fontsize=14)
    # plt.ylabel("dBFs [dBFs/bin]", fontsize=14)
    #プロット
    # plt.plot(x[:int(N/2)+1], ydb[:int(N/2)+1])
    # plt.savefig("fft.png")

    #信号電力計算
    signal = max(D[:int(N/2)+1])
    signal_index = np.argmax(D[:int(N/2)+1])
    signal_power = signal**2 * 2
    Fin = x[signal_index] #入力周波数
    
    #Noise Power + Distorsion Power
    noise = D[:int(N/2)+1]
    noise[signal_index] = 0
    noise_power = np.sum(noise*noise)*2

    #各測定値
    SFDR = sorted(ydb)[-3] * (-1)
    SNDR = 10*np.log10(signal_power/noise_power)
    ENOB = (SNDR-1.76)/6.02

    return ENOB

def fft_multi_data(datapath, Fs):

    regs = []
    ENOBs = []
    c = 0
    #データ取得
    with open(datapath, mode="r") as f:

        while True:
            
            r_data = str(f.readline()).strip().split(",")

            #レジスタ値の保存
            if r_data[0] == "SPI_REG_DATA":

                #放棄
                for i in range(4):
                    f.readline()

                #レジスタデータ行を抽出
                reg = []
                for i in range(16):
                    reg.append(int(str(f.readline()).strip().split(",")[1]))
                
                regs.append(reg)

            #ADCデータのFFT評価
            if r_data[0] == "ADC_DATA":
                
                c += 1

                for i in range(4):
                    r_data = str(f.readline()).strip().split(",")

                    #サンプル数を取得
                    if r_data[0] == "Data_Number" :
                        N = int(r_data[1])
                
                data = []
                for i in range(N):
                    data.append(int(str(f.readline()).strip().split(",")[1]))
                
                ENOB = fft(data, N, Fs)
                ENOBs.append(ENOB)

            # if r_data[0] == "--------------finished--------------":
            #     break

            #データ終了フラグ
            if r_data[0] == "MEASURE_FINISHED":
                break
        
    
    # print(regs)
    # print(ENOBs)
    #最大のENOBを探す
    max_ENOB  = max(ENOBs)
    max_reg_param = regs[ENOBs.index(max(ENOBs))]

    print(max_ENOB)
    print(max_reg_param)
    print("tried parameter number: {}".format(c))

    return max_ENOB, max_reg_param

#単一データに対するFFT
def fft_single_data(datapath, N, Fs):
    
    with open(datapath, mode="r") as f:

        r_data = [d.strip().split(",") for d in f.readlines()] #fを\n毎に分割し、さらに","毎に分割する

    c = 0
    for i in range(len(r_data)):

        #ADCデータに対する処理
        # if r_data[i][0] == "ADC_DATA": #データ抽出開始のキーワード
        if r_data[i][0] == "ADDRESS":
            c += 1

        if c== 2:
            data = []
            for j in range(N): #データ抽出
                
                data.append(r_data[i+j+1][2]) 

            break
        
    
    ENOB = fft(data, N, Fs)
    print(ENOB)

    return ENOB

if __name__ == "__main__" :
    
    fft_multi_data(datapath="./teraterm.csv", Fs=1000000)

    # fft_single_data(datapath="./data_con26.csv", N=4096*4, Fs=1000000)