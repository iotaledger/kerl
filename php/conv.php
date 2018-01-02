<?php
function gmp_shiftl($x, $n)
{ // shift left
    return(gmp_mul($x, gmp_pow(2, $n)));
}

function gmp_shiftr($x, $n)
{ // shift right
    return(gmp_div($x, gmp_pow(2, $n)));
}


$tryte_table = array(
    "9" =>array(0, 0, 0), // 0
    "A" =>array(1, 0, 0), // 1
    "B" =>array(-1, 1, 0), // 2
    "C" =>array(0, 1, 0), // 3
    "D" =>array(1, 1, 0), // 4
    "E" =>array(-1, -1, 1), // 5
    "F" =>array(0, -1, 1), // 6
    "G" =>array(1, -1, 1), // 7
    "H" =>array(-1, 0, 1), // 8
    "I" =>array(0, 0, 1), // 9
    "J" =>array(1, 0, 1), // 10
    "K" =>array(-1, 1, 1), // 11
    "L" =>array(0, 1, 1), // 12
    "M" =>array(1, 1, 1), // 13
    "N" =>array(-1, -1, -1), // -13
    "O" =>array(0, -1, -1), // -12
    "P" =>array(1, -1, -1), // -11
    "Q" =>array(-1, 0, -1), // -10
    "R" =>array(0, 0, -1), // -9
    "S" =>array(1, 0, -1), // -8
    "T" =>array(-1, 1, -1), // -7
    "U" =>array(0, 1, -1), // -6
    "V" =>array(1, 1, -1), // -5
    "W" =>array(-1, -1, 0), // -4
    "X" =>array(0, -1, 0), // -3
    "Y" =>array(1, -1, 0), // -2
    "Z" =>array(-1, 0, 0)); // -1

$trit_table = array_reverse($tryte_table, false);


function trytes_to_trits($trytes)
{
    global $tryte_table;

    $trits = array();
    foreach (str_split($trytes) as $tryte) {
        foreach ($tryte_table[$tryte] as $trit) {
            array_push($trits, $trit);
        }
    }
    return $trits;
}


function trits_to_trytes($trits)
{
    global $trit_table;
    global $tryte_table;
    $trytes = array();
    $length = count($trits);

    $trits_chunks = array();
    foreach ($trits as $key => $t){
        $trits[$key] = (int) $t;
    }
    for ($i = 0; $i < $length; $i+=3) {
        $char = array_slice($trits, $i, 3);
        array_push($trits_chunks, $char);
    }

    foreach ($trits_chunks as $chunk) {
        foreach ($tryte_table as $letter => $array){
            if ($chunk === $array){
                array_push($trytes, $letter);
            }
        }
    }
    return implode("", $trytes);
}


function convertToTrits($bytes_k)
{
    $TRIT_HASH_LENGTH = 243;
    $bigInt = convertBytesToBigInt($bytes_k);
    $trits = convertBigintToBase($bigInt, 3, $TRIT_HASH_LENGTH);
    return $trits;
}


function convertToBytes($trits)
{
    $bigInt = convertBaseToBigint($trits, 3);
    $bytes_k = convertBigintToBytes($bigInt);
    return $bytes_k;
}


function convertBaseToBigint($array, $base)
{
    $bigint = '0';

    foreach ($array as $key=>$value) {
        $newbigint = gmp_add($bigint, gmp_mul($array[$key], gmp_pow($base, $key)));
        $bigint = $newbigint;
    }

    return $bigint;
}


function convertBigintToBase($bigInt, $base, $length)
{
    $result = array();

    $is_negative = ($bigInt < 0);
    $quotient = gmp_abs($bigInt);
    $MAX = gmp_div(($base-1), 2);
    if ($is_negative) {
        $MAX = gmp_div($base, 2);
    }

    for ($i = 0; $i < $length; $i++) {
        $qr = gmp_div_qr($quotient, (string)$base);
        $remainder = $qr[1];
        $quotient = $qr[0];


        if ($remainder > $MAX) {
            # Lend 1 to the next place so we can make this digit negative.

            $remainder = gmp_sub($remainder, $base);
            $quotient = gmp_add($quotient, 1);
        }
        if ($is_negative) {
            $remainder = gmp_mul($remainder, -1);
        }
        array_push($result, $remainder);
    }

    return $result;
}


function flipBits(&$bit)
{
    $bit = ((-$bit) - 1);
}


function convertBigintToBytes($big)
{
    $bytesArrayTemp = array();
    for ($i = 0; $i <= 48; $i++) {
        array_push(
            $bytesArrayTemp,
            gmp_mod(
                gmp_shiftr(gmp_strval(gmp_abs($big)), gmp_strval(gmp_mul($i, 8))),
                gmp_shiftl('1', '8')
            )
        );
    }

    # big endian and balanced
    $bytesArray = array();
    foreach (array_reverse($bytesArrayTemp, false) as $x) {
        if ($x <= 0x7F) {
            array_push($bytesArray, $x);
        } else {
            array_push($bytesArray, $x - 0x100);
        }
    }

    if ($big < 0) {
        # 1-compliment
        array_walk($bytesArray, 'flipBits');

        # add1
        for ($i = count($bytesArray) -1; $i >= 0; $i-1) {
            $add = (($bytesArray[$i] & 0xFF) + 1);
            if ($add <= 0x7F) {
                $bytesArray[$i] = $add;
            } else {
                $bytesArray[$i] = $add - 0x100;
            }
            if ($bytesArray[$i] != 0) {
                break;
            }
        }
    }
    $removed = array_shift($bytesArray);

    return $bytesArray;
}


function convertBytesToBigInt($ba)
{
    # copy of array
    $bytesArray = $ba;

    # number sign in MSB
    if (array_values($bytesArray)[0] >= 0) {
        $signum = 1;
    } else {
        $signum = -1;
    }

    if ($signum == -1) {
        # sub1
        for ($pos = count($bytesArray) - 1; $pos >= 0; $pos-1) {
            $sub = gmp_sub(($bytesArray[$pos] & 0xFF), 1);
            if ($sub <= 0x7F) {
                $bytesArray[$pos] = $sub;
            } else {
                $bytesArray[$pos] = gmp_sub($sub,0x100);
            }
            if ($bytesArray[$pos] != -1) {
                break;
            }
        }
        # 1-compliment
        array_walk($bytesArray, 'flipBits');
    }



    # sum magnitudes and set sign
    $sum = '0';
    foreach (array_reverse($bytesArray, false) as $pos => $value) {
        $sum_add = gmp_shiftl(($value & 0xFF), gmp_strval(gmp_mul($pos,8)));
        $sum = gmp_add($sum, $sum_add);
    }
    return gmp_mul($sum, $signum);
}


function convert_sign($byte)
{
    //Convert between signed and unsigned bytes
    if ($byte < 0) {
        return 256 + $byte;
    }
    if ($byte > 127) {
        return -256 + $byte;
    }
    return $byte;
}
