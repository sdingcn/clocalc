import subprocess
import sys
import time

def run_and_read(cmd: str, inp: str) -> str:
    return subprocess.run(cmd,
        input = inp,
        stdout = subprocess.PIPE,
        universal_newlines = True,
        timeout = 60
    ).stdout

def check_io_expr(path: str, i: str, o: str) -> bool:
    try:
        raw_o = run_and_read(['python3', 'src/exprscript.py', path], i)
    except subprocess.TimeoutExpired:
        sys.stderr.write('*** Timeout expired\n')
        return False
    if raw_o != o:
        sys.stderr.write(f'*** Expected: [{o}], Got: [{raw_o}]\n')
        return False
    return True

def check_io_py(path: str, i: str, o: str) -> bool:
    try:
        raw_o = run_and_read(['python3', path], i)
    except subprocess.TimeoutExpired:
        sys.stderr.write('*** Timeout expired\n')
        return False
    if raw_o != o:
        sys.stderr.write(f'*** Expected: [{o}], Got: [{raw_o}]\n')
        return False
    return True

def main():
    expr_tests = [
        ('test/average.expr', '', '500943/77000\n'),

        ('test/binary-tree.expr', '',
'''\
1
2
3
4
5
<void>
'''),

        ('test/comprehensive.expr', '', '0\n1\n' * 15),
        
        ('test/coroutines.expr', '',
'''\
main
task 1
main
task 2
main
task 3
<void>
'''),

        ('test/ffi.expr', '', 'Hello FFI-Call from Python!\n'),

        ('test/gcd.expr', '100\n0\n', '100\n<void>\n'),
        ('test/gcd.expr', '0\n100\n', '100\n<void>\n'),
        ('test/gcd.expr', '30\n30\n', '30\n<void>\n'),
        ('test/gcd.expr', '25\n45\n', '5\n<void>\n'),
        ('test/gcd.expr', '7\n100\n', '1\n<void>\n'),

        ('test/intensive.expr', '', '50005000\n'),

        ('test/lazy-evaluation.expr', '',
'''\
3
2
1
thunk
<void>
'''),

        ('test/scope.expr', '', '1\n303\n<void>\n'),

        ('test/multi-stage.expr', '',
'''\
EVAL
hello world
hello world
<void>
'''),

        ('test/oop.expr', '',
'''\
1
2
100
2
<void>
'''),

        ('test/reg.expr', '', 'registered function\n'),

        ('test/y-combinator.expr', '', '1 120 3628800\n<void>\n')
    ]
    py_tests = [
        ('src/call-python-from-exprscript.py', '', 'EMAN\n'),
        
        ('src/call-exprscript-from-python.py', '', '15\n')
    ]
    cnt = 0
    for test in expr_tests:
        cnt += 1
        sys.stderr.write(f'====================\n')
        sys.stderr.write(f'Running on test {cnt}\n')
        start_time = time.time()
        ok = check_io_expr(*test)
        end_time = time.time()
        sys.stderr.write(f'Total time (seconds): {end_time - start_time}\n')
        if not ok:
            sys.exit(f'*** Failed on test {cnt}')
    for test in py_tests:
        cnt += 1
        sys.stderr.write(f'====================\n')
        sys.stderr.write(f'Running on test {cnt}\n')
        start_time = time.time()
        ok = check_io_py(*test)
        end_time = time.time()
        sys.stderr.write(f'Total time (seconds): {end_time - start_time}\n')
        if not ok:
            sys.exit(f'*** Failed on test {cnt}')
    sys.stderr.write(f'\nPassed all {cnt} tests\n')

if __name__ == '__main__':
    main()
