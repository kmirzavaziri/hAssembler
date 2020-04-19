# Assembler & DisAssembler
x64 Intel Instruction Assembler and DisAssembler written in Python 3. See [Online GCC version](https://defuse.ca/online-x86-assembler.htm) as a refrence.

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

To compare this python assembler with this [Online Assembler](https://defuse.ca/online-x86-assembler.htm) use

```
python3 tester.py foo.asm
```

where `foo.asm` is test cases file. We already provided a set of good tests in `test.asm`, use 

```
python3 tester.py test.asm
```

to see the result of comparing.

If no file is specified, i. e.,

```
python3 tester.py
```

it will generate a complete set of tests and compare our python code with online code for all tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

