<?php
require dirname(__FILE__) . '/PHP-SHA3-Streamable/SHA3.php';
require dirname(__FILE__) . '/conv.php';

global $BYTE_HASH_LENGTH;


class Kerl
{
    public $k;
    public $absorbArray;
    public $BYTE_HASH_LENGTH = 48;
    public $TRIT_HASH_LENGTH = 243;

    public function __construct()
    {
        $this->k = SHA3::init(SHA3::SHA3_384);
        $this->absorbArray = array();
    }

    public function reset()
    {
        $this->k = SHA3::init(SHA3::SHA3_384);
        $this->absorbArray = array();
    }


    public function absorb($trits, $offset = 0, $length = null)
    {
        if (is_null($length)) {
            $length = count($trits);
        }

        if ($length % 243 != 0) {
            echo "error";
            return "Illegal length"; //raise Exception("Illegal length")
        }
        while ($offset < $length) {
            $stop = min($offset + $this->TRIT_HASH_LENGTH, $length);

            # If we're copying over a full chunk, zero last trit

            if ($stop - $offset == $this->TRIT_HASH_LENGTH) {
                $trits[$stop - 1] = 0;
            }
            $to_bytes = array_slice($trits, $offset, $stop);
            $signed_nums = convertToBytes($to_bytes);

            $unsigned_bytes = array();
            foreach ($signed_nums as $b) {
                array_push($unsigned_bytes, (int) gmp_strval(convert_sign($b)));
            }

            array_push($this->absorbArray, $unsigned_bytes);

            $offset += $this->TRIT_HASH_LENGTH;
        }
    }


    public function squeeze(&$trits, $offset=0, $length=null){
        if ($length == null) {
            $length = $this->TRIT_HASH_LENGTH;
        }
        if ($length % 243 != 0) {
            echo("Illegal length");
            return "Illegal length";
        }

        while ($offset < $length) {
            foreach ($this->absorbArray as $a) {
                foreach ($a as $byte) {
                    $ex = gmp_export($byte, 1);
                    $this->k->absorb($ex);
                }
            }
            $unsigned_hash =  unpack("C*", $this->k->squeeze());

            $signed_hash = array();
            for ($i = 1; $i <= count($unsigned_hash); $i++) {
                array_push($signed_hash, convert_sign($unsigned_hash[$i]));
            }

            $trits_from_hash = convertToTrits($signed_hash);
            $trits_from_hash[$this->TRIT_HASH_LENGTH - 1] = 0;


            $stop = $this->TRIT_HASH_LENGTH;
            if ($length < $this->TRIT_HASH_LENGTH) {
                $stop = $length;
            }
            $tfh = array_slice($trits_from_hash, 0, $stop);
            foreach ($tfh as $key => $value) {
                $trits[$offset + $key] = $value;
            }

            $new_unsigned_hash = array();
            foreach ($unsigned_hash as $b) {
                array_push($new_unsigned_hash, (int) gmp_strval(convert_sign(~$b)));
            }

            // Reset internal state before feeding back in
            $this->reset();
            array_push($this->absorbArray, $new_unsigned_hash);

            $offset +=  $this->TRIT_HASH_LENGTH;
        }

    }
}

