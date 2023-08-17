# DiVerT

## About
DiVerT (**Di**sjunctive **Ver**ification with **T**ypes) is a prototype tool for verifying disjunctive security policies in database-backed application.

## Install
- DiVerT requires [Z3](https://github.com/Z3Prover/z3) and its Python [bindings](https://pypi.org/project/z3-solver/). 

- To begin, you should [Install](https://github.com/Z3Prover/z3/releases) Z3 on your platform, make sure it is in your path, and then proceed to install [z3-solver](https://pypi.org/project/z3-solver/) bindings using the command `pip install z3-solver`. 

- DiVerT was tested and is known to work with Z3 version 4.8.7.

- Clone the repo, or download it as a ZIP file.

## Running the use cases

You can run the benchmarks and the use cases using the following commnad:

`python main.py -i examples/DataPublishing/get_data.txt -d -r -o usr`

### Available arguments

- To specify the input source program, one should use the `-i` argument. In this case it is `examples/DataPublishing/get_data.txt`, which is the secure example of the Data Publishing use case.
- Debug information, including the final Gamma environment, the observer's dependency set, program labels, and policy labels, can be displayed by specifying the `-d` argument.
- In instances where the program is insecure, specifying the `-r` argument will provide insights into the reasons for the program's rejection.
- The observer's identifier can be (optionally) defined using the `-o` argument. In this case (and by default) it is `usr`.
