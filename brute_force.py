import S_AES
class meet_in_the_middle_attack():
    def __init__(self,plaintext,cypertext):
        self.plaintext = plaintext
        self.cypertext = cypertext
        self.pair = []
    def brute_force(self):
        """
            暴力破解
        """   
        ans=[]
        for i in range(2**16):
            binary_string_i = format(i, '016b')
            S1 = S_AES.S_AES(binary_string_i)
            middle_text = S1.encrypt(self.plaintext)
            ans.append([int(middle_text, 2),i])#middletext(int) i->K1
        sorted_ans = sorted(ans, key=lambda x: x[0])    
        print(sorted_ans)       
        for j in range(2**16):
            binary_string_j = format(j, '016b')
            S2 = S_AES.S_AES(binary_string_j)
            middle_text = S2.decrypt(self.cypertext)
            self.binary_search(sorted_ans,[int(middle_text, 2),j])
        return self.pair
    def binary_search(self, sorted_ans, key):
            l = 0
            r = len(sorted_ans) - 1
            while(l<=r):
                mid = (int)((l+r)/2)
                if sorted_ans[mid][0] < key[0]:
                    l = mid + 1
                else:
                    r = mid - 1
            if sorted_ans[l][0] == key[0]:
                # print(sorted_ans[l][0],key[0])
                # print([format(sorted_ans[l][1], '016b'),format(key[1], '016b')])
                self.pair.append([format(sorted_ans[l][1], '016b'),format(key[1], '016b')])
            else:
                return 0
            while(1):
                l = l - 1
                if l == -1:
                    break
                if sorted_ans[l][0]== key[0]:
                    # print(sorted_ans[l][0],key[0])
                    # print([format(sorted_ans[l][1], '016b'),format(key[1], '016b')])
                    self.pair.append([format(sorted_ans[l][1], '016b'),format(key[1], '016b')])
                else:
                    break
            while(1):
                r = r + 1
                if r == len(sorted_ans):
                    break
                if sorted_ans[r][0]== key[0]:
                    # print(sorted_ans[r][0],key[0])
                    # print([format(sorted_ans[r][1], '016b'),format(key[1], '016b')])
                    self.pair.append([format(sorted_ans[r][1], '016b'),format(key[1], '016b')])
                else:
                    break
    def bf(self):
        mid_texts = []
        find_keys = []
        for key in range(2**16):
            mid_texts.append()

if __name__=='__main__':
    plain_text = '1010101010101010'
    cyper_text = '1111111111111111'
    M=meet_in_the_middle_attack(plain_text,cyper_text)
    print(len(M.brute_force()))