<?php
require dirname(__FILE__) . '/kerl.php';
echo "Testing 'Message' Hash To ensure Keccak is implemented correctly...\n";
$hashcheck = "0c8d6ff6e6a1cf18a0d55b20f0bca160d0d1c914a5e842f3707a25eeb20a279f6b4e83eda8e43a67697832c7f69f53ca";
$x = new Kerl();
$x->k->absorb("Message");
$hash = bin2hex($x->k->squeeze());
echo $hash;
echo "\n";
echo $hashcheck;
echo "\n";
if ($hash == $hashcheck){
    echo "SUCCESS: Keccack 384 is implemented correctly!";
}else{
    echo "\nERROR: Keccack 384 is NOT implemented correctly. Kerl will not perform properly. \nDid you edit line 51 of '/PHP-SHA3-Streamable/SHA3.py' and change '0x06' to '0x01'?";
}
echo "\n";
echo "\n";
echo "Test 1";
$trits = trytes_to_trits("EMIDYNHBWMBCXVDEFOFWINXTERALUKYYPPHKP9JJFGJEIUY9MUDVNFZHMMWZUYUSWAIOWEVTHNWMHANBH");


$kerl = new Kerl();
$kerl->absorb($trits);
$output_trits = array();
$kerl->squeeze($output_trits, 0, 243);

$x = trits_to_trytes($output_trits);
echo "\n";
echo "EMIDYNHBWMBCXVDEFOFWINXTERALUKYYPPHKP9JJFGJEIUY9MUDVNFZHMMWZUYUSWAIOWEVTHNWMHANBH";
echo "\n";
echo $x;

echo "\n";
if ($x == "EJEAOOZYSAWFPZQESYDHZCGYNSTWXUMVJOVDWUNZJXDGWCLUFGIMZRMGCAZGKNPLBRLGUNYWKLJTYEAQX"){
    echo "Test 1 Passed";
} else {
    echo "Test 1 Failed";
}



echo "\n";
echo "\n";
echo "Test 2";
$trits = trytes_to_trits("9MIDYNHBWMBCXVDEFOFWINXTERALUKYYPPHKP9JJFGJEIUY9MUDVNFZHMMWZUYUSWAIOWEVTHNWMHANBH");


$kerl = new Kerl();
$kerl->absorb($trits);
$output_trits = array();
$kerl->squeeze($output_trits, 0, 486);


$x = trits_to_trytes($output_trits);
echo "\n";
echo "9MIDYNHBWMBCXVDEFOFWINXTERALUKYYPPHKP9JJFGJEIUY9MUDVNFZHMMWZUYUSWAIOWEVTHNWMHANBH";
echo "\n";
echo $x;

echo "\n";
if ($x == "G9JYBOMPUXHYHKSNRNMMSSZCSHOFYOYNZRSZMAAYWDYEIMVVOGKPJBVBM9TDPULSFUNMTVXRKFIDOHUXXVYDLFSZYZTWQYTE9SPYYWYTXJYQ9IFGYOLZXWZBKWZN9QOOTBQMWMUBLEWUEEASRHRTNIQWJQNDWRYLCA"){
    echo "Test 2 Passed";
} else {
    echo "Test 2 Failed";
}


echo "\n";
echo "\n";
echo "Test 3";
$trits = trytes_to_trits("G9JYBOMPUXHYHKSNRNMMSSZCSHOFYOYNZRSZMAAYWDYEIMVVOGKPJBVBM9TDPULSFUNMTVXRKFIDOHUXXVYDLFSZYZTWQYTE9SPYYWYTXJYQ9IFGYOLZXWZBKWZN9QOOTBQMWMUBLEWUEEASRHRTNIQWJQNDWRYLCA");

$kerl = new Kerl();
$kerl->absorb($trits);
$output_trits = array();
$kerl->squeeze($output_trits, 0, 486);

$x = trits_to_trytes($output_trits);
echo "\n";
echo "G9JYBOMPUXHYHKSNRNMMSSZCSHOFYOYNZRSZMAAYWDYEIMVVOGKPJBVBM9TDPULSFUNMTVXRKFIDOHUXXVYDLFSZYZTWQYTE9SPYYWYTXJYQ9IFGYOLZXWZBKWZN9QOOTBQMWMUBLEWUEEASRHRTNIQWJQNDWRYLCA";
echo "\n";
echo $x;

echo "\n";
if ($x == "LUCKQVACOGBFYSPPVSSOXJEKNSQQRQKPZC9NXFSMQNRQCGGUL9OHVVKBDSKEQEBKXRNUJSRXYVHJTXBPDWQGNSCDCBAIRHAQCOWZEBSNHIJIGPZQITIBJQ9LNTDIBTCQ9EUWKHFLGFUVGGUWJONK9GBCDUIMAYMMQX"){
    echo "Test 3 Passed";
} else {
    echo "Test 3 Failed";
}

?>
