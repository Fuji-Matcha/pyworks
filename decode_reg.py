#coding;utf-8
#send_dataからADCreg_set_dataへデコードする。ADCreg_set.pyの逆。

def main():

    with open("/mnt/c/Users/00002/Desktop/s9s8s10.txt", mode='r') as f:

        regs = []
        for num in f.readlines():

            regs.append(bin(int(num))[2:].zfill(32))
        
    MODE  = regs[1][-2]
    R     = regs[1][-1]
    GATE  = regs[2][26:21:-1]
    SNX   = regs[3][:16]
    SN8   = regs[3][31:15:-1]
    SN9   = regs[4][15::-1]
    dSN10 = regs[4][16:]
    uSN10 = regs[5][:16]
    DLN   = regs[6][16:24]
    DLP   = regs[6][31:23:-1]
    SDN1  = regs[7][16:24]
    SDN0  = regs[7][24:32]
    SDP0  = regs[8][23:15:-1]
    SDP1  = regs[8][31:23:-1]
    uSP10 = regs[9][16:]
    dSP10 = regs[10][15::-1]
    SP9   = regs[10][16:]
    SP8   = regs[11][:16]
    SPX   = regs[11][16:]

    SN10 = uSN10 + dSN10
    SP10 = uSP10 + dSP10

    sets = []
    sets.append("MODE {}".format(MODE))
    sets.append("R {}".format(R))
    sets.append("GATE {}".format(GATE))
    sets.append("SDN0 {} {}".format(SDN0[:4], SDN0[4:]))
    sets.append("SDN1 {} {}".format(SDN1[:4], SDN1[4:]))
    sets.append("SDP0 {} {}".format(SDP0[:4], SDP0[4:]))
    sets.append("SDP1 {} {}".format(SDP1[:4], SDP1[4:]))
    sets.append("SN8 {} {} {} {}".format(SN8[:4], SN8[4:8], SN8[8:12], SN8[12:16]))
    sets.append("SN9 {} {} {} {}".format(SN9[:4], SN9[4:8], SN9[8:12], SN9[12:16]))
    sets.append("SN10 {} {} {} {} {} {} {} {}".format(SN10[:4], SN10[4:8], SN10[8:12], SN10[12:16], SN10[16:20], SN10[20:24], SN10[24:28], SN10[28:32]))
    sets.append("SNX {} {} {} {}".format(SNX[:4], SNX[4:8], SNX[8:12], SNX[12:16]))
    sets.append("SP8 {} {} {} {}".format(SP8[:4], SP8[4:8], SP8[8:12], SP8[12:16]))
    sets.append("SP9 {} {} {} {}".format(SP9[:4], SP9[4:8], SP9[8:12], SP9[12:16]))
    sets.append("SP10 {} {} {} {} {} {} {} {}".format(SP10[:4], SP10[4:8], SP10[8:12], SP10[12:16], SP10[16:20], SP10[20:24], SP10[24:28], SP10[28:32]))
    sets.append("SPX {} {} {} {}".format(SPX[:4], SPX[4:8], SPX[8:12], SPX[12:16]))
    sets.append("DLN {} {}".format(DLN[:4], DLN[4:]))
    sets.append("DLP {} {}".format(DLP[:4], DLP[4:]))


    with open("/mnt/c/Users/00002/Desktop/decoded_data.txt", mode='w') as f:

        f.write("\r\n".join(sets))





if __name__ == "__main__":
    
    main()