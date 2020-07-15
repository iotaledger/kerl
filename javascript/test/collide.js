var chai = require('chai');
var assert = chai.assert;
var Converter = require('../converter');
var Kerl = require('../kerl');

describe('kerlission', function() {
    var expected = 'OXJCNFHUNAHWDLKKPELTBFUCVW9KLXKOGWERKTJXQMXTKFKNWNNXYD9DMJJABSEIONOSJTTEVKVDQEWTW';
    var tests = [
        'GYOMKVTSNHVJNCNFBBAH9AAMXLPLLLROQY99QN9DLSJUHDPBLCFFAIQXZA9BKMBJCYSFHFPXAHDWZFEIZ',
        'GYOMKVTSNHVJNCNFBBAH9AAMXLPLLLROQY99QN9DLSJUHDPBLCFFAIQXZA9BKMBJCYSFHFPXAHDWZFEIH',
        'GYOMKVTSNHVJNCNFBBAH9AAMXLPLLLROQY99QN9DLSJUHDPBLCFFAIQXZA9BKMBJCYSFHFPXAHDWZFEIQ'
    ];

    tests.forEach(function(test){

        it('Should collide: ' + expected, function() {
            var trits = Converter.trits(test);
            var kerl = new Kerl();
            kerl.initialize();
            kerl.absorb(trits, 0, trits.length);
            var hashTrits = [];
            kerl.squeeze(hashTrits, 0, kerl.HASH_LENGTH);
            var hash = Converter.trytes(hashTrits);
            assert.deepEqual(expected, hash);
        });
    });
});
