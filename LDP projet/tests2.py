#!/usr/bin/env python3
#
# Fichier de tests pour la phase 2 du projet.
#
# Vous pouvez tester votre projet avec la commande :
#
#   python3 tests2.py chemin/vers/votre/executable

import os
import subprocess
import sys



PROGRAM_FILE = "program.txt"

PROGRAMS = [
"""SET a 5
ADD a 6
PRINT a
SUB a 4
IFNZ a
PRINT a
SUB a 10
IFNZ a
PRINT a
""",

"""SET a 0
IFNZ a
PRINT a
SET a 5
IFNZ a
PRINT a
""",

"""SET c 50000
PRINT c
ADD c 50000
PRINT c
""",

"""PRINT a
PRINT b
PRINT c
PRINT d
""",

"""SET a 120
ADD a 30
PRINT a
SET b 130
PRINT b
SUB a b
PRINT a
""",

"""SET a 5
PUSH a
ADD a a
PUSH a
SUB a 20
PUSH a
POP d
PRINT d
POP b
PRINT b
POP c
PRINT c
""",

"""SET a 5
SET b 8
STORE 100 a
STORE 102 b
LOAD 100 d
PRINT d
LOAD 102 c
PRINT c
""",

"""SET a 150
SET b 130
PUSH a
ADD a b
PUSH a
STORE 100 a
STORE 101 b
POP c
PRINT c
POP d
PRINT d
LOAD 100 b
IFNZ b
PRINT b
LOAD 101 a
PRINT a
SUB b b
IFNZ b
PRINT b
""",
]

OUTPUTS = [
  [
    ["11"],
    ["7"],
  ],
  [
    ["5"],
  ],
  [
    ["50000"],
    ["65535"],
  ],
  [
    ["0"],
    ["0"],
    ["0"],
    ["0"],
  ],
  [
    ["150"],
    ["130"],
    ["20"],
  ],
  [
    ["0"],
    ["10"],
    ["5"],
  ],
  [
    ["5"],
    ["8"],
  ],
  [
    ["280", "280"],
    ["150", "150"],
    ["256", "33304"],
    ["130", "130"],
  ],
]



def write_program(n: int):
  with open(PROGRAM_FILE, "w+") as f:
    f.write(PROGRAMS[n])


def remove_program():
  os.remove(PROGRAM_FILE)


def check_program_output(n: int):
  program = subprocess.run([sys.argv[1], PROGRAM_FILE], capture_output=True, encoding="utf-8")
  output = program.stdout.split('\n')[:-1]

  if len(output) > len(OUTPUTS[n]):
    OUTPUTS[n].append('')
  elif len(OUTPUTS[n]) > len(output):
    output.append('')

  for output_line, expected_line in zip(output, OUTPUTS[n], strict=True):
    if output_line not in expected_line:
      print(f"### FAIL ###   Expected {expected_line} but output is '{output_line}'", file=sys.stderr)
      print(program.stderr, file=sys.stderr)
      return False

  return True


if __name__ == "__main__":
  for i in range(len(PROGRAMS)):
    write_program(i)
    if check_program_output(i):
      print(f"OK {i}")
    else:
      print(f"--> Erreur avec le programme {i}", file=sys.stderr)
      break
  remove_program()
