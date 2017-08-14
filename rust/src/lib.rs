#![no_std]
#![feature(alloc)]
#![feature(core_intrinsics)]

#[cfg(test)]
#[macro_use]
extern crate std;

#[cfg(test)]
extern crate rand;

#[macro_use]
extern crate alloc;


extern crate iota_trytes as trytes;

mod curl;
mod keccak;

mod constants;
mod converter;
mod cpukerl;

pub use converter::*;
pub use cpukerl::*;
