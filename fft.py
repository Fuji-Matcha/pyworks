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

    #add
    func_cnt = 0
    FUNC_NAME = ["ADCParameterSet1","ADCParameter_S10","ADCParameter_S9","ADCParameter_S8","ADCParameter_SX","AllParameter_examined"]

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
            
            #add
            #各ADCParameter終了時
            if r_data[0] == FUNC_NAME[func_cnt+1]:
                #最大のENOBを探す
                max_ENOB  = max(ENOBs)
                max_reg_param = regs[ENOBs.index(max(ENOBs))]

                print("{}".format(FUNC_NAME[func_cnt]))
                print(max_ENOB)
                print(max_reg_param)
                print("tried parameter number: {}".format(c))
                print("")                       

                func_cnt += 1
                c = 0
                del ENOBs
                del regs
                ENOBs = []
                regs  = []
            

            #データ終了フラグ
            if r_data[0] == "AllParameter_examined":
                break
            # if r_data[0] == "MEASURE_FINISHED":
            #     break
        
        
    #最大のENOBを探す
    # max_ENOB  = max(ENOBs)
    # max_reg_param = regs[ENOBs.index(max(ENOBs))]

    # print(max_ENOB)
    # print(max_reg_param)
    # print("tried parameter number: {}".format(c))

    # return max_ENOB, max_reg_param

#単一データに対するFFT
def fft_single_data(datapath, Fs):
    
    with open(datapath, mode="r") as f:

        r_data = [d.strip().split(",") for d in f.readlines()] #fを\n毎に分割し、さらに","毎に分割する

    c = 0
    for i in range(len(r_data)):

        #ADCデータに対する処理
        if r_data[i][0] == "ADC_DATA": #データ抽出開始のキーワード

            c += 1
        
        if c==1 and r_data[i][0] == "Data_Number":

            N = int(r_data[i][1])
            c += 1
        
        if c==2 and r_data[i][0] == "128":

            data = []
            for j in range(N): #データ抽出
                
                data.append(r_data[i+j][2]) 

            c = 0
            break   
    
    ENOB = fft(data, N, Fs)
    print(ENOB)

    return ENOB

if __name__ == "__main__" :
    
    fft_multi_data(datapath="/mnt/c/Users/00002/Desktop/consecutive_measure.log", Fs=1000000)

    # fft_single_data(datapath="/mnt/c/Users/00002/Desktop/teraterm.log", Fs=1000000)