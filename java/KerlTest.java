//import com.iota.iri.model.Hash; //used for generate* tests - can be imported from IRI.
import org.junit.Assert;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.math.BigInteger;
import java.util.Arrays;
import java.util.Random;

/**
 * Created by alon on 04/08/17.
 */
public class KerlTest {
    final static Random seed = new Random();
    Logger log = LoggerFactory.getLogger(CurlTest.class);

    //Test conversion functions:
    @Test
    public void bytesFromBigInt() throws Exception {
        int byte_size = 48;
        BigInteger bigInteger = new BigInteger("13190295509826637194583200125168488859623001289643321872497025844241981297292953903419783680940401133507992851240799");
        byte[] outBytes = Kerl.convertBigintToBytes(bigInteger,byte_size);
        BigInteger out_bigInteger = Kerl.convertBytesToBigInt(outBytes,0,outBytes.length);
        Assert.assertTrue(bigInteger.equals(out_bigInteger));
    }

    @Test
    public void loopRandBytesFromBigInt() throws Exception {
        //generate random bytes, turn them to trits and back
        int byte_size = 48;
        int trit_size = 243;
        byte[] inBytes = new byte[byte_size];
        int[] trits;
        byte[] outBytes;
        for (int i = 0; i<10_000; i++) {
            seed.nextBytes(inBytes);
            BigInteger in_bigInteger = Kerl.convertBytesToBigInt(inBytes,0,inBytes.length);
            trits = Kerl.convertBigintToTrits(in_bigInteger, trit_size);
            BigInteger out_bigInteger = Kerl.convertTritsToBigint(trits, 0, trit_size);
            outBytes = Kerl.convertBigintToBytes(out_bigInteger,byte_size);
            if(i % 1_000 == 0) {
                System.out.println(String.format("%d iteration: %s",i, in_bigInteger ));
            }
            Assert.assertTrue(String.format("bigInt that failed: %s",in_bigInteger),Arrays.equals(inBytes,outBytes));
        }
    }

    @Test
    public void loopRandTritsFromBigInt() throws Exception {
        //generate random bytes, turn them to trits and back
        int byte_size = 48;
        int trit_size = 243;
        int[] inTrits;
        byte[] bytes;
        int[] outTrits;
        for (int i = 0; i<10_000; i++) {
            inTrits = getRandomTrits(trit_size);
            inTrits[242] = 0;

            BigInteger in_bigInteger = Kerl.convertTritsToBigint(inTrits, 0, trit_size);
            bytes = Kerl.convertBigintToBytes(in_bigInteger,byte_size);
            BigInteger out_bigInteger = Kerl.convertBytesToBigInt(bytes,0,bytes.length);
            outTrits = Kerl.convertBigintToTrits(out_bigInteger, trit_size);

            if(i % 1_000 == 0) {
                System.out.println(String.format("%d iteration: %s",i, in_bigInteger ));
            }
            Assert.assertTrue(String.format("bigInt that failed: %s",in_bigInteger),Arrays.equals(inTrits,outTrits));
        }
    }

    //@Test
    public void generateBytesFromBigInt() throws Exception {
        System.out.println("bigInteger,ByteArray");
        for (int i = 0; i<100_000; i++) {
            int byte_size = 48;
            byte[] outBytes = new byte[byte_size];
            seed.nextBytes(outBytes);
            BigInteger out_bigInteger = new BigInteger(outBytes);
            System.out.println(String.format("%s,%s", out_bigInteger, Arrays.toString(out_bigInteger.toByteArray())));
            //Assert.assertTrue(bigInteger.equals(out_bigInteger));
        }
    }

    @Test
    public void kurlOneAbsorb() throws Exception {
        int[] initial_value = trits("EMIDYNHBWMBCXVDEFOFWINXTERALUKYYPPHKP9JJFGJEIUY9MUDVNFZHMMWZUYUSWAIOWEVTHNWMHANBH");
        Curl k = SpongeFactory.create(SpongeFactory.Mode.KERL);
        k.absorb(initial_value, 0, initial_value.length);
        int[] hash_value = new int[Curl.HASH_LENGTH];
        k.squeeze(hash_value, 0, hash_value.length);
        String hash = trytes(hash_value);
        Assert.assertEquals("EJEAOOZYSAWFPZQESYDHZCGYNSTWXUMVJOVDWUNZJXDGWCLUFGIMZRMGCAZGKNPLBRLGUNYWKLJTYEAQX", hash);
    }

    @Test
    public void kurlMultiSqueeze() throws Exception {
        int[] initial_value = trits("9MIDYNHBWMBCXVDEFOFWINXTERALUKYYPPHKP9JJFGJEIUY9MUDVNFZHMMWZUYUSWAIOWEVTHNWMHANBH");
        Curl k = SpongeFactory.create(SpongeFactory.Mode.KERL);
        k.absorb(initial_value, 0, initial_value.length);
        int[] hash_value = new int[Curl.HASH_LENGTH * 2];
        k.squeeze(hash_value, 0, hash_value.length);
        String hash = trytes(hash_value);
        Assert.assertEquals("G9JYBOMPUXHYHKSNRNMMSSZCSHOFYOYNZRSZMAAYWDYEIMVVOGKPJBVBM9TDPULSFUNMTVXRKFIDOHUXXVYDLFSZYZTWQYTE9SPYYWYTXJYQ9IFGYOLZXWZBKWZN9QOOTBQMWMUBLEWUEEASRHRTNIQWJQNDWRYLCA", hash);
    }

    @Test
    public void kurlMultiAbsorbMultiSqueeze() throws Exception {
        int[] initial_value = trits("G9JYBOMPUXHYHKSNRNMMSSZCSHOFYOYNZRSZMAAYWDYEIMVVOGKPJBVBM9TDPULSFUNMTVXRKFIDOHUXXVYDLFSZYZTWQYTE9SPYYWYTXJYQ9IFGYOLZXWZBKWZN9QOOTBQMWMUBLEWUEEASRHRTNIQWJQNDWRYLCA");
        Curl k = SpongeFactory.create(SpongeFactory.Mode.KERL);
        k.absorb(initial_value, 0, initial_value.length);
        int[] hash_value = new int[Curl.HASH_LENGTH * 2];
        k.squeeze(hash_value, 0, hash_value.length);
        String hash = trytes(hash_value);
        Assert.assertEquals("LUCKQVACOGBFYSPPVSSOXJEKNSQQRQKPZC9NXFSMQNRQCGGUL9OHVVKBDSKEQEBKXRNUJSRXYVHJTXBPDWQGNSCDCBAIRHAQCOWZEBSNHIJIGPZQITIBJQ9LNTDIBTCQ9EUWKHFLGFUVGGUWJONK9GBCDUIMAYMMQX", hash);
    }

    public static int[] getRandomTrits(int length) {
        return Arrays.stream(new int[length]).map(i -> seed.nextInt(3)-1).toArray();
    }

//    public static int[] getRandomTransactionTrits() {
//        return new Hash(getRandomTrits(Hash.SIZE_IN_TRITS));
//    }
//
//    //@Test
//    public void generateTrytesAndHashes() throws Exception {
//        System.out.println("trytes,Kerl_hash");
//        for (int i = 0; i< 10000 ; i++) {
//            Hash trytes = getRandomTransactionHash();
//            int[] initial_value = trytes.trits();
//            Curl k = SpongeFactory.create(SpongeFactory.Mode.KERL);
//            k.absorb(initial_value, 0, initial_value.length);
//            int[] hash_value = new int[Curl.HASH_LENGTH];
//            k.squeeze(hash_value, 0, hash_value.length);
//            String hash = trytes(hash_value);
//            System.out.println(String.format("%s,%s",trytes,hash));
//        }
//    }
//
//    //@Test
//    public void generateTrytesAndMultiSqueeze() throws Exception {
//        System.out.println("trytes,Kerl_squeeze1,Kerl_squeeze2,Kerl_squeeze3");
//        for (int i = 0; i< 10000 ; i++) {
//            Hash trytes = getRandomTransactionHash();
//            int[] initial_value = trytes.trits();
//            Curl k = SpongeFactory.create(SpongeFactory.Mode.KERL);
//            k.absorb(initial_value, 0, initial_value.length);
//            int[] hash_value = new int[Curl.HASH_LENGTH];
//            k.squeeze(hash_value, 0, hash_value.length);
//            String hash1 = trytes(hash_value);
//            k.squeeze(hash_value, 0, hash_value.length);
//            String hash2 = trytes(hash_value);
//            k.squeeze(hash_value, 0, hash_value.length);
//            String hash3 = trytes(hash_value);
//            System.out.println(String.format("%s,%s,%s,%s",trytes,hash1,hash2,hash3));
//        }
//    }
//
//    //@Test
//    public void generateMultiTrytesAndHash() throws Exception {
//        System.out.println("multiTrytes,Kerl_hash");
//        for (int i = 0; i< 10000 ; i++) {
//            String multi = String.format("%s%s%s",getRandomTransactionHash(),getRandomTransactionHash(),getRandomTransactionHash());
//            int[] initial_value = trits(multi);
//            Curl k = SpongeFactory.create(SpongeFactory.Mode.KERL);
//            k.absorb(initial_value, 0, initial_value.length);
//            int[] hash_value = new int[Curl.HASH_LENGTH];
//            k.squeeze(hash_value, 0, hash_value.length);
//            String hash = trytes(hash_value);
//            System.out.println(String.format("%s,%s",multi,hash));
//        }
//    }
//
//
//    //@Test
//    public void generateHashes() throws Exception {
//        //System.out.println("trytes,Kerl_hash");
//        for (int i = 0; i< 1_000_000 ; i++) {
//            Hash trytes = getRandomTransactionHash();
//            int[] initial_value = trytes.trits();
//            Curl k = SpongeFactory.create(SpongeFactory.Mode.KERL);
//            k.absorb(initial_value, 0, initial_value.length);
//            int[] hash_value = new int[Curl.HASH_LENGTH];
//            k.squeeze(hash_value, 0, hash_value.length);
//            String hash = trytes(hash_value);
//            //System.out.println(String.format("%s,%s",trytes,hash));
//            System.out.println(String.format("%s",hash));
//        }
//    }



    //Conversion helper function
    public static final int RADIX = 3;
    public static final int MAX_TRIT_VALUE = (RADIX - 1) / 2, MIN_TRIT_VALUE = -MAX_TRIT_VALUE;

    public static final int NUMBER_OF_TRITS_IN_A_BYTE = 5;
    public static final int NUMBER_OF_TRITS_IN_A_TRYTE = 3;

    static final int[][] BYTE_TO_TRITS_MAPPINGS = new int[243][];
    static final int[][] TRYTE_TO_TRITS_MAPPINGS = new int[27][];

    public static final String TRYTE_ALPHABET = "9ABCDEFGHIJKLMNOPQRSTUVWXYZ";


    static {

        final int[] trits = new int[NUMBER_OF_TRITS_IN_A_BYTE];

        for (int i = 0; i < 243; i++) {
            BYTE_TO_TRITS_MAPPINGS[i] = Arrays.copyOf(trits, NUMBER_OF_TRITS_IN_A_BYTE);
            increment(trits, NUMBER_OF_TRITS_IN_A_BYTE);
        }

        for (int i = 0; i < 27; i++) {
            TRYTE_TO_TRITS_MAPPINGS[i] = Arrays.copyOf(trits, NUMBER_OF_TRITS_IN_A_TRYTE);
            increment(trits, NUMBER_OF_TRITS_IN_A_TRYTE);
        }
    }
    private static void increment(final int[] trits, final int size) {
        for (int i = 0; i < size; i++) {
            if (++trits[i] > MAX_TRIT_VALUE) {
                trits[i] = MIN_TRIT_VALUE;
            } else {
                break;
            }
        }
    }

    public static int[] trits(final String trytes) {

        final int[] trits = new int[trytes.length() * NUMBER_OF_TRITS_IN_A_TRYTE];
        for (int i = 0; i < trytes.length(); i++) {
            System.arraycopy(TRYTE_TO_TRITS_MAPPINGS[TRYTE_ALPHABET.indexOf(trytes.charAt(i))], 0, trits, i * NUMBER_OF_TRITS_IN_A_TRYTE, NUMBER_OF_TRITS_IN_A_TRYTE);
        }
        return trits;
    }

    public static String trytes(final int[] trits, final int offset, final int size) {

        final StringBuilder trytes = new StringBuilder();
        for (int i = 0; i < (size + NUMBER_OF_TRITS_IN_A_TRYTE - 1) / NUMBER_OF_TRITS_IN_A_TRYTE; i++) {
            int j = trits[offset + i * 3] + trits[offset + i * 3 + 1] * 3 + trits[offset + i * 3 + 2] * 9;
            if (j < 0) {
                j += TRYTE_ALPHABET.length();
            }
            trytes.append(TRYTE_ALPHABET.charAt(j));
        }
        return trytes.toString();
    }

    public static String trytes(final int[] trits) {
        return trytes(trits, 0, trits.length);
    }
}
