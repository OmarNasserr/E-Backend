import base64, re
from Crypto.Cipher import AES
from Crypto import Random
from django.conf import settings

import codecs

# make utf8mb4 recognizable.
codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)


class AESCipher:

    def __init__(self, key, blk_sz):
        self.key = key
        self.blk_sz = blk_sz

    def encrypt( self, raw ):
        # raw is the main value
        if raw is None or len(raw) == 0:
            raise NameError("No value given to encrypt")
        raw = raw + '\0' * (self.blk_sz - len(raw) % self.blk_sz)
        raw = raw.encode('utf8mb4')
        # Initialization vector to avoid same encrypt for same strings.
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key.encode('utf8mb4'), AES.MODE_CFB, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) ).decode('utf8mb4')

    def decrypt( self, enc ):
        # enc is the encrypted value
        if enc is None or len(enc) == 0:
            raise NameError("No value given to decrypt")
        
        ## decoding in a try-catch block because passed encryped value can be in
        ## a wrong format and that raises an error, therefore we return decoded value
        ## of text 'wrong id format' and in the view we check if the decoded value is int 
        ## and if not we raise a view error
        try:
            enc = base64.b64decode(enc)
        except:
            enc=self.encrypt('wrong id format')
            enc=base64.b64decode(enc)            
        iv = enc[:16]
        # AES.MODE_CFB that allows bigger length or latin values
        cipher = AES.new(self.key.encode('utf8mb4'), AES.MODE_CFB, iv )
        return re.sub(b'\x00*$', b'', cipher.decrypt( enc[16:])).decode('utf8mb4')
