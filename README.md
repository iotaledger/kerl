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
|Milestone verification| V |   |   |

Curl-P-N: N number of rounds 
_^ CheckSums are calculated using the **last** 9 trytes._ 

_^ CheckSums are calculated using the **last** 9 trytes._ 

---
## Kerl specification:
#### [Kerl Specification](IOTA-Kerl-spec.md): specification and implementation details for kerl
#### [Kerl Test vectors](test_vectors/): extensive test vectors for independent implementations


## Kerl implementation examples:
#### [Java](java/)
#### [JavaScript](javascript/)
#### [Python2](python2/)
#### [Python3](python3/)

