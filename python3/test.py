import unittest
import random
import csv
import sha3
import conv
import py3kerl
 
class TestKerl(unittest.TestCase):
 
    def test_correct_hash_function(self):
        k = sha3.keccak_384()
        k.update("Message".encode('utf-8'))

        self.assertEqual(k.hexdigest(), "0c8d6ff6e6a1cf18a0d55b20f0bca160d0d1c914a5e842f3707a25eeb20a279f6b4e83eda8e43a67697832c7f69f53ca")

    def test_correct_first(self):
        inp = 'EMIDYNHBWMBCXVDEFOFWINXTERALUKYYPPHKP9JJFGJEIUY9MUDVNFZHMMWZUYUSWAIOWEVTHNWMHANBH'

        trits = conv.trytes_to_trits(inp)

        kerl = py3kerl.Kerl()
        kerl.absorb(trits)
        trits_out = []
        kerl.squeeze(trits_out)

        trytes_out = conv.trits_to_trytes(trits_out)

        self.assertEqual(trytes_out, "EJEAOOZYSAWFPZQESYDHZCGYNSTWXUMVJOVDWUNZJXDGWCLUFGIMZRMGCAZGKNPLBRLGUNYWKLJTYEAQX")

    def test_output_greater_243(self):
        inp = '9MIDYNHBWMBCXVDEFOFWINXTERALUKYYPPHKP9JJFGJEIUY9MUDVNFZHMMWZUYUSWAIOWEVTHNWMHANBH'

        trits = conv.trytes_to_trits(inp)

        kerl = py3kerl.Kerl()
        kerl.absorb(trits)
        trits_out = []
        kerl.squeeze(trits_out, length=486)

        trytes_out = conv.trits_to_trytes(trits_out)

        self.assertEqual(trytes_out, "G9JYBOMPUXHYHKSNRNMMSSZCSHOFYOYNZRSZMAAYWDYEIMVVOGKPJBVBM9TDPULSFUNMTVXRKFIDOHUXXVYDLFSZYZTWQYTE9SPYYWYTXJYQ9IFGYOLZXWZBKWZN9QOOTBQMWMUBLEWUEEASRHRTNIQWJQNDWRYLCA")

    def test_input_greater_243(self):
        inp = 'G9JYBOMPUXHYHKSNRNMMSSZCSHOFYOYNZRSZMAAYWDYEIMVVOGKPJBVBM9TDPULSFUNMTVXRKFIDOHUXXVYDLFSZYZTWQYTE9SPYYWYTXJYQ9IFGYOLZXWZBKWZN9QOOTBQMWMUBLEWUEEASRHRTNIQWJQNDWRYLCA'

        trits = conv.trytes_to_trits(inp)

        kerl = py3kerl.Kerl()
        kerl.absorb(trits)
        trits_out = []
        kerl.squeeze(trits_out, length=486)

        trytes_out = conv.trits_to_trytes(trits_out)

        self.assertEqual(trytes_out, "LUCKQVACOGBFYSPPVSSOXJEKNSQQRQKPZC9NXFSMQNRQCGGUL9OHVVKBDSKEQEBKXRNUJSRXYVHJTXBPDWQGNSCDCBAIRHAQCOWZEBSNHIJIGPZQITIBJQ9LNTDIBTCQ9EUWKHFLGFUVGGUWJONK9GBCDUIMAYMMQX")


    def test_all_bytes(self):
        for i in range(-128, 128):
            in_bytes = [i] * 48
            trits = conv.convertToTrits(in_bytes)
            out_bytes = list(conv.convertToBytes(trits))

            self.assertEqual(in_bytes, out_bytes)

    def test_random_trits(self):
        in_trits = [random.randrange(-1,2) for _ in range(243)]
        in_trits[242] = 0
        in_bytes = conv.convertToBytes(in_trits)
        out_trits = conv.convertToTrits(in_bytes)

        self.assertEqual(in_trits, out_trits)

    def test_generate_trytes_hash(self):
        file = 'test_vectors/generateTrytesAndHashes'
        with open(file,'r') as f:
            reader = csv.DictReader(f)
            for count, line in enumerate(reader):
                trytes = line['trytes']
                hashes = line['Kerl_hash']

                trits = conv.trytes_to_trits(trytes)

                kerl = py3kerl.Kerl()
                kerl.absorb(trits)
                trits_out = []
                kerl.squeeze(trits_out)

                trytes_out = conv.trits_to_trytes(trits_out)

                self.assertEqual(hashes, trytes_out, 'line:' + str(count+2) +' '+ hashes + '!=' + trytes_out)
                # if count % 100 ==0:
                #     print(count,"passed",file)

    def test_generate_multitrytes_and_hash(self):
        file = 'test_vectors/generateMultiTrytesAndHash'
        with open(file,'r') as f:
            reader = csv.DictReader(f)
            for count, line in enumerate(reader):
                trytes = line['multiTrytes']
                hashes = line['Kerl_hash']

                trits = conv.trytes_to_trits(trytes)

                kerl = py3kerl.Kerl()
                kerl.absorb(trits)
                trits_out = []
                kerl.squeeze(trits_out)

                trytes_out = conv.trits_to_trytes(trits_out)

                self.assertEqual(hashes, trytes_out, 'line:' + str(count+2) +' '+ hashes + '!=' + trytes_out)
                # if count % 100 ==0:
                #     print(count,"passed",file)

    def test_generate_trytes_and_multisqueeze(self):
        file = 'test_vectors/generateTrytesAndMultiSqueeze'
        with open(file,'r') as f:
            reader = csv.DictReader(f)
            for count, line in enumerate(reader):
                trytes = line['trytes']
                hashes1 = line['Kerl_squeeze1']
                hashes2 = line['Kerl_squeeze2']
                hashes3 = line['Kerl_squeeze3']

                trits = conv.trytes_to_trits(trytes)

                kerl = py3kerl.Kerl()
                kerl.absorb(trits)

                trits_out = []
                kerl.squeeze(trits_out)
                trytes_out = conv.trits_to_trytes(trits_out)
                self.assertEqual(hashes1, trytes_out, 'line:' + str(count+2) +' '+ hashes1 + '!=' + trytes_out)

                trits_out = []
                kerl.squeeze(trits_out)
                trytes_out = conv.trits_to_trytes(trits_out)
                self.assertEqual(hashes2, trytes_out, 'line:' + str(count+2) +' '+ hashes2 + '!=' + trytes_out)

                trits_out = []
                kerl.squeeze(trits_out)
                trytes_out = conv.trits_to_trytes(trits_out)
                self.assertEqual(hashes3, trytes_out, 'line:' + str(count+2) +' '+ hashes3 + '!=' + trytes_out)

                # if count % 100 ==0:
                #     print(count,"passed",file)

if __name__ == '__main__':
    unittest.main()
