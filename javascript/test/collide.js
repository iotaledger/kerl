var chai = require('chai');
var assert = chai.assert;
var Converter = require('../converter');
var Kerl = require('../kerl');

describe('kerlission', function() {
    var tests = [{
        input: 'GYOMKVTSNHVJNCNFBBAH9AAMXLPLLLROQY99QN9DLSJUHDPBLCFFAIQXZA9BKMBJCYSFHFPXAHDWZFEIZ',
        expected: 'OXJCNFHUNAHWDLKKPELTBFUCVW9KLXKOGWERKTJXQMXTKFKNWNNXYD9DMJJABSEIONOSJTTEVKVDQEWTW'
    },{
        input: 'GYOMKVTSNHVJNCNFBBAH9AAMXLPLLLROQY99QN9DLSJUHDPBLCFFAIQXZA9BKMBJCYSFHFPXAHDWZFEIH',
        expected: 'OXJCNFHUNAHWDLKKPELTBFUCVW9KLXKOGWERKTJXQMXTKFKNWNNXYD9DMJJABSEIONOSJTTEVKVDQEWTW'
    },{
        input: 'GYOMKVTSNHVJNCNFBBAH9AAMXLPLLLROQY99QN9DLSJUHDPBLCFFAIQXZA9BKMBJCYSFHFPXAHDWZFEIQ',
        expected: 'OXJCNFHUNAHWDLKKPELTBFUCVW9KLXKOGWERKTJXQMXTKFKNWNNXYD9DMJJABSEIONOSJTTEVKVDQEWTW'
    }];

    tests.forEach(function(test){

        it('Should collide: ' + test.expected, function() {
            var trits = Converter.trits(test.input);
            var kerl = new Kerl();
            kerl.initialize();
            kerl.absorb(trits, 0, trits.length);
            var hashTrits = [];
            kerl.squeeze(hashTrits, 0, kerl.HASH_LENGTH);
            var hash = Converter.trytes(hashTrits);
            assert.deepEqual(test.expected, hash);
        });

    });

});
