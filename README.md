# clo

![](https://github.com/sdingcn/clo/actions/workflows/run_test.yml/badge.svg)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/sdingcn/clo)

**Clo** is a small, dynamically-typed, garbage-collected, functional programming language.
Here is an (incomplete) summary of its syntax.
```
<comment>   := "#" [^\n]* "\n"
<intrinsic> := "." [^\s]+
<binding>   := <var> <expr>
<expr>      := <int-literal> | <str-literal> | <var>
            |  lambda ( <var>* ) <expr>
            |  letrec ( <binding>* ) <expr>
            |  if <expr> <expr> <expr>
            |  { <expr>+ }  // sequenced evaluation
            |  ( <intrinsic> <expr>* )
            |  ( <expr> <expr>* )
            |  @ <var> <expr>  // access var in closure's env (can simulate structs)
```

The distinguished feature of clo is serializing
the current program state as a string.
The built-in function `.forkstate` returns
a string encoding the program state,
and when the state is resumed using `.eval` it starts
right after the `.forkstate` call but with a return value of Void type.
This resembles Linux's `fork`, Lisp's `call/cc`, etc.
For example, the following program outputs 0, 1, 2, 2, 3 in order.
Note: `.eval` works on both source code and serialized program state.
```
{
    (.putstr "0\n")
    (.putstr "1\n")
    letrec (state (.forkstate)) {
        (.putstr "2\n")
        if (.= (.type state) 0)  # if it is a void value
           (.putstr "3\n")
           (.eval state)
    }
}
```

See [test/](test/) for more code examples (`*.clo`).

## dependencies

The source code of the interpreter
is standard C++20 and thus can be compiled
by any C++20-conforming compiler.
The current `Makefile` and `run_test.py`
need `clang++` (with C++20 support), `make`, and `python3`.

## build and run

```
make -C src/ release
bin/clo <source-path>
```

`python3 run_test.py` (re-)builds the interpreter and runs all tests.
