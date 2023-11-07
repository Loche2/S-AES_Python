import S_AES
class two_fold_S_AES():
    def __init__(self, key):
        self.S1 = S_AES.S_AES(key[:16])
        self.S2 = S_AES.S_AES(key[16:])

    def two_fold_encrypt(self, plain_text):
        plain_text = self.S1.encrypt(plain_text)
        cypher_text = self.S2.encrypt(plain_text)
        return cypher_text
    def two_fold_decrypt(self, cypher_text):
        cypher_text = self.S1.decrypt(plain_text)
        plain_text = self.S2.decrypt(cypher_text)
        return plain_text
    
if __name__=='__main__':
    key = '00000000000000000000000000001111'
    print(f'key = {key}')
    S_ASE = two_fold_S_AES(key)

    plain_text = '1111111111111111'
    cypher_text = S_ASE.two_fold_encrypt(plain_text)
    print(cypher_text)