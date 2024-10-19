# closure

![](https://github.com/sdingcn/closure/actions/workflows/auto-test.yml/badge.svg)

## syntax

```
<comment>   := #[^\n]*\n
<integer>   := [+-]?[0-9]+
<variable>  := [a-zA-Z_][a-zA-Z0-9_]*
<intrinsic> := .void
             | .+ | .- | .* | ./ | .% | .<
             | .type  // returns an integer representation (see below) of the object's type
                      // an object's type never changes during its lifetime
             | .get | .put  // get/put integers
<vepair>    := <variable> <expr>

<expr> := <integer>
        | <variable>
        | lambda ( <variable>* ) <expr>
        | letrec ( <vepair>* ) <expr>
        | if <expr> <expr> <expr>
        | { <expr>+ }
        | ( <intrinsic> <expr>* )
        | ( <expr> <expr>* )
        | @ <variable> <expr>  // access a closure's env variable
```

## semantics

+ Reference semantics (unobservable):
  variables are references to objects;
  expressions evaluate to references of objects;
  both `letrec` and `( <callee> <expr>* )` use pass-by-reference.
+ Three object types, all immutable: `Void` (0), `Int` (1), `Closure` (2).
+ Variables cannot be re-bound.
+ The evaluation order of `lambda` and `letrec` is left-to-right.
+ Simple periodic GC with compaction.
+ No tail-call optimization.

## dependency

`cmake` >= 3.28.1, a reasonable version of `make`, and `clang++` >= C++20

## build (on Linux/macOS)

```
mkdir build
cmake -DCMAKE_BUILD_TYPE:STRING=Debug \
      -DCMAKE_CXX_COMPILER:FILEPATH=$(which clang++) \
      -S src -B build \
      -G "Unix Makefiles"
cd build
make
```

## run

```
build/closure <source-path>
```

To run all tests, do `python3 run_test.py`.
