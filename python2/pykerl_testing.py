import csv
import random

import iota
from pykerl import Kerl



def H(in_trytes):
    out = H_Kerl(iota.TryteString(in_trytes).as_trits())
    return str(iota.TryteString.from_trits(out))

#test Kerl iteration:
def H_Kerl(in_trits):
    k = Kerl()
    k.absorb(in_trits)
    out_trits = []
    k.squeeze(out_trits)
    return out_trits

def addChecksum(trytes):
    out = H(trytes)
    checksum = out[-9:]
    return trytes+checksum

#Test keccak impl.
import sha3
k = sha3.keccak_384()
k.update("Message")
n = k.hexdigest()
assert n=="0c8d6ff6e6a1cf18a0d55b20f0bca160d0d1c914a5e842f3707a25eeb20a279f6b4e83eda8e43a67697832c7f69f53ca"

############################
#Test conversions:
############################

value = 10234
trits = Kerl.convertBigintToTrits(value)
big = Kerl.convertTritsToBigint(trits)
assert big==value

value = 13190295509826637194583200125168488859623001289643321872497025844241981297292953903419783680940401133507992851240799
bytes = Kerl.convertBigintToBytes(value)
big = Kerl.convertBytesToBigInt(bytes)
assert big==value


value = 1433452143
trits = Kerl.convertBigintToTrits(value)
big = Kerl.convertTritsToBigint(trits)
out_trits = Kerl.convertBigintToTrits(big)
assert out_trits==trits


for i in range(-128,128):
    #fill
    in_bytes = [i] * 48
    in_big = Kerl.convertBytesToBigInt(in_bytes)
    trits = Kerl.convertBigintToTrits(in_big)
    out_big = Kerl.convertTritsToBigint(trits)
    out_bytes = Kerl.convertBigintToBytes(out_big)
    assert in_bytes==out_bytes

for i in range(1000):
    #fill
    in_bytes = [long(random.randrange(-128,128)) for j in range(48)]
    in_big = Kerl.convertBytesToBigInt(in_bytes)
    trits = Kerl.convertBigintToTrits(in_big)
    out_big = Kerl.convertTritsToBigint(trits)
    out_bytes = Kerl.convertBigintToBytes(out_big)
    assert in_bytes==out_bytes, "{} != {}".format(in_bytes,out_bytes)

for i in range(1000):
    #fill
    in_trits = [long(random.randrange(-1,2)) for j in range(243)]
    in_trits[242] = 0
    in_big = Kerl.convertTritsToBigint(in_trits)
    bytes = Kerl.convertBigintToBytes(in_big)
    out_big = Kerl.convertBytesToBigInt(bytes)
    out_trits = Kerl.convertBigintToTrits(out_big)
    assert in_trits==out_trits, "{}\n{} != \nAssertionError: {}\n{}\n{}".format(i,in_trits,out_trits,in_big,out_big)


############################
#Test Kerl:
############################

#kerlOneAbsorb
TS = "EMIDYNHBWMBCXVDEFOFWINXTERALUKYYPPHKP9JJFGJEIUY9MUDVNFZHMMWZUYUSWAIOWEVTHNWMHANBH"
in_value = iota.TryteString(TS).as_trits()
out_value = H_Kerl(in_value)
out_value_trytes = iota.TryteString.from_trits(out_value)
expected = "EJEAOOZYSAWFPZQESYDHZCGYNSTWXUMVJOVDWUNZJXDGWCLUFGIMZRMGCAZGKNPLBRLGUNYWKLJTYEAQX"
assert str(out_value_trytes)==expected

#kerlMultiSqeeze
TS = "9MIDYNHBWMBCXVDEFOFWINXTERALUKYYPPHKP9JJFGJEIUY9MUDVNFZHMMWZUYUSWAIOWEVTHNWMHANBH"
in_value = iota.TryteString(TS).as_trits()
k = Kerl()
k.absorb(in_value)
out_value = []
k.squeeze(out_value)
out_value_trytes = iota.TryteString.from_trits(out_value)
expected = "G9JYBOMPUXHYHKSNRNMMSSZCSHOFYOYNZRSZMAAYWDYEIMVVOGKPJBVBM9TDPULSFUNMTVXRKFIDOHUXX"
assert str(out_value_trytes)==expected
k.squeeze(out_value)
out_value_trytes = iota.TryteString.from_trits(out_value)
expected = "VYDLFSZYZTWQYTE9SPYYWYTXJYQ9IFGYOLZXWZBKWZN9QOOTBQMWMUBLEWUEEASRHRTNIQWJQNDWRYLCA"
assert str(out_value_trytes)==expected



#kerlDiscardTrit
TS = "LTSTDRQOOLUTLNUTGTKUOILVKWQJOMLAQBRMJDPHRRGYNNLQGPQIWNAPLKMVTKJQUTRPUOCUUCKEXSHBD"
in_value = iota.TryteString(TS).as_trits()
out_value = H_Kerl(in_value)
out_value_trytes = iota.TryteString.from_trits(out_value)
TS2 = "LTSTDRQOOLUTLNUTGTKUOILVKWQJOMLAQBRMJDPHRRGYNNLQGPQIWNAPLKMVTKJQUTRPUOCUUCKEXSHBM"
in_value2 = iota.TryteString(TS2).as_trits()
out_value2 = H_Kerl(in_value2)
out_value_trytes2 = iota.TryteString.from_trits(out_value2)
assert str(out_value_trytes)==str(out_value_trytes2)



############################
#Validate test-vectors (Java generate*)
############################

file = 'test_vectors/generateTrytesAndHashes'
with open(file,'r') as f:
    reader = csv.DictReader(f)
    for count,line in enumerate(reader):
        trytes = line['trytes']
        hashes = line['Kerl_hash']
        assert hashes==H(trytes),'line:' + str(count+2) +' '+ hashes + '!=' + H(trytes)
        if count % 100 ==0:
            print count,"passed",file


file = 'test_vectors/generateMultiTrytesAndHash'
with open(file,'r') as f:
    reader = csv.DictReader(f)
    for count,line in enumerate(reader):
        trytes = line['multiTrytes']
        hashes = line['Kerl_hash']
        assert hashes==H(trytes),hashes + '!=' + H(trytes)
        if count % 100 ==0:
            print count,"passed",file

file = 'test_vectors/generateTrytesAndMultiSqueeze'
with open(file,'r') as f:
    reader = csv.DictReader(f)
    for count,line in enumerate(reader):
        trytes = line['trytes']
        hash1 = line['Kerl_squeeze1']
        hash2 = line['Kerl_squeeze2']
        hash3 = line['Kerl_squeeze3']
        in_value = iota.TryteString(trytes).as_trits()
        k = Kerl()
        k.absorb(in_value)
        out_value = []
        k.squeeze(out_value)
        out_value_trytes = iota.TryteString.from_trits(out_value)
        expected = hash1
        assert str(out_value_trytes) == expected
        k.squeeze(out_value)
        out_value_trytes = iota.TryteString.from_trits(out_value)
        expected = hash2
        assert str(out_value_trytes) == expected
        k.squeeze(out_value)
        out_value_trytes = iota.TryteString.from_trits(out_value)
        expected = hash3
        assert str(out_value_trytes) == expected
        if count % 100 ==0:
            print count,"passed",file



## Needs to replace Kerl->Curl in pycurl to run.

# seed = "NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN"
# i = iota.Iota("http://localhost:10001",seed)
# addy = i.get_new_addresses(0,1)
# #Kerl
# expected = "MDWYEJJHJDIUVPKDY9EACGDJUOP9TLYDWETUBOYCBLYXYYYJYUXYUTCTPTDGJYFKMQMCNZDQPTBE9AFIW"
# #Curl
# #expected = "FS9KT9CLDAADRVMCEIPVTVUSCBORRKUOBEDKUZJUQUFLRRJUWIMFCTBDOTX9PPGRQNXRGERJSY9FBTAWM"
# assert str(addy['addresses'][0])==expected



# file = 'test_vectors/generateNAddressesForSeed'
# with open(file,'r') as f:
#     reader = csv.DictReader(f)
#     for count,line in enumerate(reader):
#         seed = line['seed']
#         address_0 = line['address_0']
#         address_1 = line['address_1']
#         address_2 = line['address_2']
#         address_3 = line['address_3']
#         i = iota.Iota("http://localhost:10001", seed)
#         addy = i.get_new_addresses(0, 4)['addresses']
#
#         assert address_0==addy[0],'line:' + str(count+2) +' '+ seed
#         assert address_1==addy[1],'line:' + str(count+2) +' '+ seed
#         assert address_2==addy[2],'line:' + str(count+2) +' '+ seed
#         assert address_3==addy[3],'line:' + str(count+2) +' '+ seed
#
#         if count % 1 ==0:
#             print count,"passed",file


