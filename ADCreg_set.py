# coding:utf-8
# 2進の各設定値入力を32bitSPIreg構成に対応させて10進で返す

def main():

    # レジスタの設定を記述したファイル(ADCreg_set_data.txt)を開く
    with open("/mnt/c/Users/00002/Desktop/ADCreg_set_data.txt", mode='r') as f:

        s_strip = [s.strip() for s in f.readlines()]

    # 各キーワードに応じて値を保存
    for line in s_strip:
        line = line.split()
        # print(s_strip)
        # print(line)
        
        if   line[0]=="MODE" : MODE=line[1]
        elif line[0]=="R"    : R = line[1]
        elif line[0]=="GATE" : GATE = "".join(line[1:])[::-1]
        elif line[0]=="SDN0" : SDN0 = "".join(line[1:])
        elif line[0]=="SDN1" : SDN1 = "".join(line[1:])
        elif line[0]=="SDP0" : SDP0 = "".join(line[1:])[::-1]
        elif line[0]=="SDP1" : SDP1 = "".join(line[1:])[::-1]
        elif line[0]=="SN8"  : SN8  = "".join(line[1:])[::-1]
        elif line[0]=="SN9"  : SN9  = "".join(line[1:])[::-1]
        elif line[0]=="SN10" : SN10 = "".join(line[1:])
        elif line[0]=="SNX"  : SNX  = "".join(line[1:])
        elif line[0]=="SP8"  : SP8  = "".join(line[1:])
        elif line[0]=="SP9"  : SP9  = "".join(line[1:])
        elif line[0]=="SP10" : SP10 = "".join(line[1:])
        elif line[0]=="SPX"  : SPX  = "".join(line[1:])
        elif line[0]=="DLN"  : DLN  = "".join(line[1:])
        elif line[0]=="DLP"  : DLP  = "".join(line[1:])[::-1]

    # レジスタ値の設定
    REG = []
    REG.append("0b0")
    REG.append("0b" + MODE + R)
    REG.append("0b" + GATE + "00000")
    REG.append("0b" + SNX + SN8)
    REG.append("0b" + SN9 + SN10[16:])
    REG.append("0b" + SN10[:16] + "0000000000000000")
    REG.append("0b" + DLN + DLP)
    REG.append("0b" + SDN1 + SDN0)
    REG.append("0b" + SDP0 + SDP1)
    REG.append("0b" + SP10[:16])
    REG.append("0b" + SP10[:15:-1] + SP9)
    REG.append("0b" + SP8 + SPX)
    REG.append("0b" + "0")
    REG.append("0b" + "0")
    REG.append("0b" + "0")
    REG.append("0b" + "0")

    #2進を10進に変換した後文字列型にする
    for i in range(16):
        REG[i] = str(int(REG[i], 0))
    
    #最終行に改行を入れる
    REG[15] = REG[15] + "\r\n"
    
    #REGを要素ごとに改行して書き込み
    with open("/mnt/c/Users/00002/Desktop/teraterm_send_data.txt", mode='w') as f:

        f.write("\r\n".join(REG))

if __name__ == "__main__":
    
    main()