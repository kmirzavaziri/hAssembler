# Assembler & DisAssembler
x64 Intel Instruction Assembler and DisAssembler written in Python 3. See [Online GCC version](https://defuse.ca/online-x86-assembler.htm) as a refrence. The operators this tool can assemble/disassemble are limited to

- Binary Operators: `add`, `or`, `adc`, `sbb`, `and`, `sub`, `xor`, and `cmp` 
- Unary Operators: `inc` and `dec` 

## Prerequisites

You need to have python3 installed in order to use this tool.

## Getting Started

To assemble file `foo.asm` just use

```
python3 hAssembler.py foo.asm
```

If you want the get raw bytes use `--raw` flag.

```
python3 hAssembler.py foo.asm --raw
```

## Running the tests

### Assembler

To compare this python assembler with this [Online Assembler](https://defuse.ca/online-x86-assembler.htm) use

```
python3 tester.py foo.asm
```

where `foo.asm` is test cases file. If no file is specified, i. e.,

```
python3 tester.py
```

it will generate a complete set of tests and compare this python code with the online refrence for all tests. If you want to see the generated tests, use

```
python3 testGen.py {id}
```

where `{id}` is a number in `range(22)`, specifying the test-case id. Once you executed the command, the result is available in `testGened.asm` file. For generating all test-cases at once, use

```
python3 testGen.py
```

without specifying any test-case id.

### DisAssembler

To compare this DisAssembler with the online version you will need a binary file, you may assemble an assembly text file i.e., `foo.asm` into it's equivalent binary machine code `foo.bin` using this command

```
python3 disTestGen.py foo.asm
```

This command uses our Assembler as a core to assemble the assembly file. Once you had the `.bin` file prepared, use

```
python3 disTester.py foo.bin
```

This command first disassembles and then assembles the result of DisAssembler and compare the machine codes. For testing all test cases similar to what `tester.py` does for the Assembler use

```
python3 disTester.py
```

without specifying any file name.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

