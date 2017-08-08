var chai = require('chai');
var assert = chai.assert;
var Converter = require('../converter');
var Kerl = require('../kerl');

describe('kerl.absorb-squeeze', function() {

  var tests = [{
    input: 'GYOMKVTSNHVJNCNFBBAH9AAMXLPLLLROQY99QN9DLSJUHDPBLCFFAIQXZA9BKMBJCYSFHFPXAHDWZFEIZ',
    expected: 'OXJCNFHUNAHWDLKKPELTBFUCVW9KLXKOGWERKTJXQMXTKFKNWNNXYD9DMJJABSEIONOSJTTEVKVDQEWTW'
  }];
  
  tests.forEach(function(test){
  
    it('Should produce valid hash: ' + test.expected, function() {
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
