#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sha3
import conv

BYTE_HASH_LENGTH = 48
TRIT_HASH_LENGTH = 243

class Kerl(object):
    def __init__(self):
        self.k = sha3.keccak_384()

    def absorb(self, trits, offset=0, length=None):
        if length == None:
            length = len(trits)

        if length % 243 != 0:
            raise Exception("Illegal length") 

        while offset < length:
            stop = min(offset + TRIT_HASH_LENGTH, length)

            # If we're copying over a full chunk, zero last trit
            if stop - offset == TRIT_HASH_LENGTH:
                trits[stop - 1] = 0

            signed_nums = conv.convertToBytes(trits[offset:stop])

            # Convert signed bytes into their equivalent unsigned representation
            # In order to use Python's built-in bytes type
            unsigned_bytes = bytes([conv.convert_sign(b) for b in signed_nums])

            self.k.update(unsigned_bytes)

            offset += TRIT_HASH_LENGTH

    def squeeze(self, trits, offset=0, length=None):
        if length == None:
            length = TRIT_HASH_LENGTH

        if length % 243 != 0:
            raise Exception("Illegal length") 

        while offset < length:
            unsigned_hash = self.k.digest()

            signed_hash = [conv.convert_sign(b) for b in unsigned_hash]

            trits_from_hash = conv.convertToTrits(signed_hash)
            trits_from_hash[TRIT_HASH_LENGTH - 1] = 0

            stop = TRIT_HASH_LENGTH
            if length < TRIT_HASH_LENGTH:
                stop = length
            trits[offset:stop] = trits_from_hash[0:stop]

            flipped_bytes = bytes([conv.convert_sign(~b) for b in unsigned_hash])

            # Reset internal state before feeding back in
            self.__init__()
            self.k.update(flipped_bytes)

            offset += TRIT_HASH_LENGTH


if __name__ == '__main__':
    inp = 'G9JYBOMPUXHYHKSNRNMMSSZCSHOFYOYNZRSZMAAYWDYEIMVVOGKPJBVBM9TDPULSFUNMTVXRKFIDOHUXXVYDLFSZYZTWQYTE9SPYYWYTXJYQ9IFGYOLZXWZBKWZN9QOOTBQMWMUBLEWUEEASRHRTNIQWJQNDWRYLCA'

    trits = conv.trytes_to_trits(inp)

    kerl = Kerl()
    kerl.absorb(trits)

    trits_out = []

    kerl.squeeze(trits_out, length=486)

    print('Out: ' + conv.trits_to_trytes(trits_out))
