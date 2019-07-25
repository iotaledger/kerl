# IOTA Kerl:

##### IOTA is adding an additional hashing function, based on Keccak, with conversion to ternary.
##### The following document describes the functionality and specification to be implemented.
---

### Kerl integration in IOTA:
Kerl is used in IOTA for the following tasks:

| Functionality |Curl-P-27 | Curl-P-81     | Kerl   |
| ------------- |:--------:|:--------:| :-----:|
|Address generation |   |      | V^ |
|Signature generation|   |     | V |
|Signature verification|   |   | V |
|Essence calculation (bundleHash)| | | V |
|Proof of Work         |   | V |   |
|Transaction Hash      |   | V |   |
|Milestone verification|   |   |   | V

_Curl-P-N: N number of rounds_

_^ CheckSums are calculated using the **last** 9 trytes._ 

---
### Keccak implementation:

**keccak_384()** is the underlying hash function being used,
To make sure you are using the same version:
`keccak_384("Message") = 0c8d6ff6e6a1cf18a0d55b20f0bca160d0d1c914a5e842f3707a25eeb20a279f6b4e83eda8e43a67697832c7f69f53ca`

It is important to follow industry best practices, hence we chose to use the best known crypto suites for each component:

**Java**: Bouncy Castle Provider: https://mvnrepository.com/artifact/org.bouncycastle/bcprov-jdk15on

**JavaScript**:crypto-js: https://www.npmjs.com/package/crypto-js

**Python**: pysha3 (native hashlib in py >= 3.6): https://pypi.python.org/pypi/pysha3

**Reference implementation** (in C) : https://github.com/gvanas/KeccakCodePackage

---
### Kerl implementation:
Kerl implements the same interface as Curl:
Trits are absorbed by the sponge function. And later squeezed to provide message digest, derive keys etc.

`Kerl()` initializes a new Kerl instance (with a clean keccak instance.)

`reset()` resets Kerl’s internal state.

`absorb(trits, offset, length) `

&nbsp;&nbsp;&nbsp;&nbsp;**Inputs**:
	`trits`: array of trits to be absorbed.
	`offset`: offset in array to start absorbing from.
	`length`: amount of trits to absorb.

&nbsp;&nbsp;&nbsp;&nbsp;**Output**:
	None

&nbsp;&nbsp;&nbsp;&nbsp;**Function**:
The trits will be absorbed `trits[offset:offset+length]`, in chunks of 243 (or less if length isn’t a multiple of 243).
Each 243-trit chunk’s last trit zeroed-out, then converted to 384-bits and absorbed by keccak.

`squeeze(trits, offset, length) `

&nbsp;&nbsp;&nbsp;&nbsp;**Inputs**:
	`trits`: array of trits to copy squeezed trits to.
	`offset`: offset in array to start copying squeezed trits to.
	`length`: amount of trits to squeeze.

&nbsp;&nbsp;&nbsp;&nbsp;**Output**:
	None - trits is updated in-place.

&nbsp;&nbsp;&nbsp;&nbsp;**Function**:
`length` trits will be squeezed and copied to `trits[offset:offset+length]`, in chunks of 243 (or less if length isn’t a multiple of 243).
Squeeze is done by receiving a 384-bit digest() from keccak, then converting to 243-trits.
Each 243-trit chunk’s last trit zeroed-out, and trits are copied to `trits`.

#### Kerl pseudo code:
```
class Kerl(object):
 def Kerl():
   self.k = sha3.keccak_384()

```
```
def reset():
   self.k.reset()

```
```
 def absorb(trits, offset, length):
    if length not a multiple of 243: throw "Illegal length"
    while has trits to consume:
       trits[242] = 0 #avoid conversion undefined edge-case
       bytes = convertToBytes(trits[243_chunks]) #offset in used as in Curl
       self.k.update(bytes)

```
```
 def squeeze(trits, offset, length):
    if length not a multiple of 243: throw "Illegal length"
    while has trits to fill:
       bytes = self.k.digest()
       trits.copy(convertToTrits(bytes)) #offset in used as in Curl
       trits[242] = 0 #avoid conversion undefined edge-case
       self.k.reset() # [1]
       for byte in bytes: 
           byte = ~byte #flip bits
       self.k.update(bytes)
```
[1] dependent on keccak library implementation, some reset after digest() and this can be removed, test with expected results "output with more than 243-trits". 

#### Expected results:
_stated in trytes for convenience_

input with 243-trits: `Kerl(EMIDYNHBWMBCXVDEFOFWINXTERALUKYYPPHKP9JJFGJEIUY9MUDVNFZHMMWZUYUSWAIOWEVTHNWMHANBH) = EJEAOOZYSAWFPZQESYDHZCGYNSTWXUMVJOVDWUNZJXDGWCLUFGIMZRMGCAZGKNPLBRLGUNYWKLJTYEAQX`

output with more than 243-trits: `Kerl(9MIDYNHBWMBCXVDEFOFWINXTERALUKYYPPHKP9JJFGJEIUY9MUDVNFZHMMWZUYUSWAIOWEVTHNWMHANBH,length=486-trits) = G9JYBOMPUXHYHKSNRNMMSSZCSHOFYOYNZRSZMAAYWDYEIMVVOGKPJBVBM9TDPULSFUNMTVXRKFIDOHUXXVYDLFSZYZTWQYTE9SPYYWYTXJYQ9IFGYOLZXWZBKWZN9QOOTBQMWMUBLEWUEEASRHRTNIQWJQNDWRYLCA`

input & output with more than 243-trits: `Kerl(G9JYBOMPUXHYHKSNRNMMSSZCSHOFYOYNZRSZMAAYWDYEIMVVOGKPJBVBM9TDPULSFUNMTVXRKFIDOHUXXVYDLFSZYZTWQYTE9SPYYWYTXJYQ9IFGYOLZXWZBKWZN9QOOTBQMWMUBLEWUEEASRHRTNIQWJQNDWRYLCA,length=486-trits) = 
LUCKQVACOGBFYSPPVSSOXJEKNSQQRQKPZC9NXFSMQNRQCGGUL9OHVVKBDSKEQEBKXRNUJSRXYVHJTXBPDWQGNSCDCBAIRHAQCOWZEBSNHIJIGPZQITIBJQ9LNTDIBTCQ9EUWKHFLGFUVGGUWJONK9GBCDUIMAYMMQX`



---
### Trits <-> Bytes encoding:
Conversion from trits to bytes utilizes bigInteger as an intermediate representation:

```
243-trits->BigInteger->384-bits (48 bytes)
384-bits (48 bytes)->BigInteger->243-trits
```
_Bytes are signed bytes (-128:127) as represented in java._

#### encoding pseudo code:
```
BYTE_HASH_LENGTH = 48
TRIT_HASH_LENGTH = 243

```
```
def convertToTrits(bytes):
	bigInt = convertBytesToBigInt(bytes)
	trits = convertBigintToTrits(bigInt)
	return trits

```
```
def convertToBytes(trits):
	bigInt = convertTritsToBigint(trits)
	bytes = convertBigintToBytes(bigInt)
	return bytes
```
#### Conversion Trits to/from BigInteger 
done by multiplying each array cell by its index and summing the results.
```
def convertTritsToBigint(trits):
	base = 3
	return convertBaseToBigint(trits,base)

```
```
def convertBaseToBigint(array,base):
	sum = 0
	for i=1:len(array):
		sum+= array[i] * (base ** i)
	return sum
```

```
def convertBigintToTrits(bigInt):
	base = 3
	length = TRIT_HASH_LENGTH
	return convertBigintToBase(bigInt,base,length)
```
```
def convertBigintToBase(bigInt,base,length):
	is_negative = bigInt < 0
	quotient = abs(bigInt)
	MAX = is_negative ? base/2 : (base-1)/2

	for i=1:length:
		quotient,remainder = divmod(quotient, base)
		if remainder > MAX:
			# Lend 1 to the next place so we can make this digit negative.
			quotient += 1
			remainder -= base #to match unsigned scheme
		result[i] = is_negative ? (-1) * remainder : remainder
	return result
```
#### Conversion Bytes to/from BigInteger 
done based on Java BigInteger 2-compliment representation:
[Source Code](http://grepcode.com/file/repository.grepcode.com/java/root/jdk/openjdk/6-b14/java/math/BigInteger.java#BigInteger.toByteArray%28%29)

all bigIntegers are represented using 48bytes in big-endiean - the most significant byte is in the zeroth element.
so numbers represented in less than 48bytes are sign-extended to fill array: '0' for positive, '-1' for negative.
```
def convertBytesToBigInt(bytes):
	return new BigInteger(Arrays.copyOfRange(bytes,0,BYTE_HASH_LENGTH)) #copy to pad bytes array
```
```
def convertBigintToBytes(bigInt):
	bigIntBytes = bigInt.toByteArray()
        #copy bigIntBytes
        for i=0:bigIntBytes.length:
               result[BYTE_HASH_LENGTH - i - 1] = bigIntBytes[bigIntBytes.length-i]
	
	#pad the rest
	signExtend = bigIntBytes[0] >= 0 ? 0 : -1
        for i=0:(BYTE_HASH_LENGTH - bigIntBytes.length):
               result[i] = signExtend
        
```

#### Expected results:
Converting `trits->bigInt->bytes->bigInt->trits => in_trits==out_trits`

Converting `bytes->bigInt->trits->bigInt->bytes => in_bytes==out_bytes`

example tests:
```
for i=-128:128:
    in_bytes = [i] * 48
    in_big = Kerl.int_from_bytes(in_bytes)
    trits = Kerl.trits_from_int(in_big)
    out_big = Kerl.int_from_trits(trits)
    out_bytes = Kerl.bytes_from_int(out_big)
    assert in_bytes==out_bytes
```
```
for i=1:1_000_000:
    in_bytes = fill with 48 randomBytes
    in_big = Kerl.int_from_bytes(in_bytes)
    trits = Kerl.trits_from_int(in_big)
    out_big = Kerl.int_from_trits(trits)
    out_bytes = Kerl.bytes_from_int(out_big)
    assert in_bytes==out_bytes
```
```
for i=1:1_000_000:
    in_trits = fill with 243 randomTrits
    in_trits[242] = 0 #not to overflow bytes
    in_big = Kerl.int_from_trits(in_trits)
    bytes = Kerl.bytes_from_int(in_big)
    out_big = Kerl.int_from_bytes(bytes)
    out_trits = Kerl.trits_from_int(out_big)
    assert in_trits==out_trits
```
