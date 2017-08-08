import sha3

HASH_LENGTH = 243
BYTE_HASH_LENGH = 48

class Kerl(object):

  k = None
  trits_state = None
  bytes_state = None

  def __init__(self):
    self.reset()
    self.trits_state = []
    self.bytes_state = []

  def reset(self):
    self.k = sha3.keccak_384()

  def absorb(self, trits):
    length = len(trits)
    if length % 243 != 0:
        raise Exception("Illegal length")

    offset = 0
    while offset < length:
      start = offset
      stop  = min(start + HASH_LENGTH, length)
      self.trits_state[0:stop - start] = trits[start:stop]

      # Transform.
      # byte encoding
      self.trits_state[HASH_LENGTH-1] = 0
      un_bytes = Kerl.convertBigintToBytes(Kerl.convertTritsToBigint(self.trits_state)) #may be a flaw - what if length % HASH_LENGTH != 0
      _bytes = map(lambda x: x % 256, un_bytes)

      self.k.update(bytearray(_bytes))

      # Move on to the next hash.
      offset += HASH_LENGTH


  def squeeze(self, trits):

    if len(trits) % 243 != 0:
      raise Exception("Illegal length")

    self.bytes_state = bytearray.fromhex(self.k.hexdigest())
    _bytes = map(lambda x: x if x<=127 else x-256 , self.bytes_state)


    #trits encoding
    trits.extend([0] * max(0, HASH_LENGTH - len(trits)))
    self.trits_state = Kerl.convertBigintToTrits(Kerl.convertBytesToBigInt(_bytes))

    # Copy exactly one hash.
    trits[0:HASH_LENGTH] = self.trits_state[0:HASH_LENGTH]
    trits[HASH_LENGTH - 1] = 0

    # One hash worth of trits copied; now transform.
    self.bytes_state = map(lambda x: x ^ 0xFF, self.bytes_state)
    self.reset()
    self.k.update(bytearray(self.bytes_state))



  @staticmethod
  def convertTritsToBigint(trits):
    return sum(base * (3 ** power) for power, base in enumerate(trits))

  @staticmethod
  def convertBigintToTrits(n):
    return Kerl.convertBigintToBase(n, 3, HASH_LENGTH)

  @staticmethod
  def convertBigintToBytes(big):
    bytesArrayTemp = [((abs(big) >> pos * 8) % (1 << 8)) for pos in range(48)]
    # big endian and balanced
    bytesArray = map(lambda x: x if x <= 0x7F else (x - 0x100), reversed(bytesArrayTemp))

    if big < 0:
      # 1-compliment
      bytesArray = map(lambda x: ~x, bytesArray)
      # add1
      for pos in reversed(range(len(bytesArray))):
        add = ((bytesArray[pos] & 0xFF) + 1)
        bytesArray[pos] = add if add <= 0x7F else (add - 0x100)
        if bytesArray[pos] != 0:
          break

    return bytesArray


  @staticmethod
  def convertBytesToBigInt(ba):
    # copy of array
    bytesArray = map(lambda x: x, ba)
    # number sign in MSB
    signum = 1 if bytesArray[0] >= 0 else -1

    if signum == -1:
      # sub1
      for pos in reversed(range(len(bytesArray))):
        sub = ((bytesArray[pos] & 0xFF) - 1)
        bytesArray[pos] = sub if sub <= 0x7F else (sub - 0x100)
        if bytesArray[pos] != -1:
          break
      # 1-compliment
      bytesArray = map(lambda x: ~x, bytesArray)

    # sum magnitudes and set sign
    return sum((x & 0xFF) << pos * 8 for pos, x in enumerate(reversed(bytesArray))) * signum

  @staticmethod
  def convertBigintToBase(n, radix, pad):
    base = [0] * pad
    negative = n<0
    n = -n if negative else n
    MAX = int((radix) / 2) if negative else int((radix-1) / 2)
    for i in range(pad):
      n, remainder = divmod(n, radix)

      if remainder > MAX:
        # Lend 1 to the next place so we can make this trit negative.
        n += 1
        remainder -= radix

      base[i] = -remainder if negative else remainder

    return base

