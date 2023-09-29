# DiVerT

## About
DiVerT (**Di**sjunctive **Ver**ification with **T**ypes) is a prototype tool for verifying disjunctive security policies in database-backed application.

## Install
- DiVerT requires [Z3](https://github.com/Z3Prover/z3) and its Python [bindings](https://pypi.org/project/z3-solver/). 

- To begin, you should [Install](https://github.com/Z3Prover/z3/releases) Z3 on your platform, make sure it is in your path, and then proceed to install [z3-solver](https://pypi.org/project/z3-solver/) bindings using the command `pip install z3-solver`. 

- DiVerT was tested and is known to work with Z3 version 4.8.7.

- Clone the repo, or download it as a ZIP file.

## Running the use cases

You can run the tests or the use cases using the following commnad:

`python main.py -i examples/DataPublishing/get_data.txt -d -r -o usr`

### Available arguments

- To specify the input source program, one should use the `-i` argument. In this case it is `examples/DataPublishing/get_data.txt`, which is the secure example of the Data Publishing use case.
- Debug information, including the final Gamma environment, the observer's dependency set, program labels, and policy labels, can be displayed by specifying the `-d` argument.
- In instances where the program is insecure, specifying the `-r` argument will provide insights into the reasons for the program's rejection.
- The observer's identifier can be (optionally) defined using the `-o` argument. In this case (and by default) it is `usr`.

### Example
For example, test number 10 is a simple insecure program with the following code:

```
@Table(emp, n:str, r:str, s:int)@
@Policy(SELECT n,s FROM emp WHERE s > 1000; | SELECT n,r FROM emp; )@

x = @Query(SELECT n FROM emp WHERE s > 0;)@;
out(x,usr);
```

We can run this program with:

`python main.py -i examples/Tests/test10.imp -r -d`

The output of DiVerT for this program would look like:

```
######################### DEBUG #########################
Gamma final : 
		pc ↦ { {'pc'} }
		usr ↦ { {'pc', 'usr', Query<<SELECT n FROM emp WHERE s > 0;>>} }
		x ↦ { {'pc', Query<<SELECT n FROM emp WHERE s > 0;>>} }

usr's Dependency:
		usr ↦ { {'pc', 'usr', Query<<SELECT n FROM emp WHERE s > 0;>>} }

Program Labels : 
		{ < {'emp'}, (s>0), {'n'} > }


Policy Labels : 
		{ < {'emp'}, true, {'n', 'r'} > }
		{ < {'emp'}, (s>1000), {'n', 's'} > }


######################### REASON(S) #########################
Because: 
	< {'emp'}, (s>0), {'n'} > ⋢ < {'emp'}, true, {'n', 'r'} >
		Reason dep((s>0)) ∪ {'n'} ⊄ {'n', 'r'}

	< {'emp'}, (s>0), {'n'} > ⋢ < {'emp'}, (s>1000), {'n', 's'} >
		Reason (s>0) ⊭ (s>1000)

######################### VERDICT #########################

>>> The program is insecure. ⨉
```

Which clearly states that the program is insecure because none of the disjuncts of the policy allow query `SELECT n FROM emp WHERE s > 0`.
