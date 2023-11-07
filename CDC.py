import S_AES
import random
class CDC():
    def __init__(self):
        self.iv = random.randint(0,2**16-1)
    def encrypt(self,plaintext,key):
        plain_text = []
        length = (len(plaintext)//16)
        for i in range(0,length):
            plt = plaintext[16*i:16*(i+1)]
            plain_text.append(plt)
        S = S_AES.S_AES(key)
        cyper_text=[]
        cyper_text.append(S.encrypt(format(self.iv^int(plain_text[0],2),'016b')))
        for i in range(1,length):
            cyper_text.append(S.encrypt(format(int(cyper_text[i-1], 2)^int(plain_text[i],2), '016b')))
        return cyper_text
    def decrypt(self,cypertext,key):
        cyper_text = []
        length = (len(cypertext)//16)
        for i in range(0,length):
            plt = cypertext[16*i:16*(i+1)]
            cyper_text.append(plt)
        S = S_AES.S_AES(key)
        plain_text=[]
        plain_text.append(format(self.iv^int(S.decrypt(cyper_text[0]), 2),'016b'))
        for i in range(1,length):
            plain_text.append(format(int(cyper_text[i-1],2)^int(S.decrypt(cyper_text[i]),2), '016b'))
        return plain_text
    
if __name__=='__main__':
    C=CDC()
    plaintext = '10100101101001011111000011110000'
    key = '1010101010101010'
    cyper_text = C.encrypt(plaintext,key)
    print(cyper_text)
    print(C.decrypt(cyper_text[0]+cyper_text[1],key))
