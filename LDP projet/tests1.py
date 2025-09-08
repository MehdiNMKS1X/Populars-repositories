#!/usr/bin/env python3
#
# Fichier de tests pour la phase 1 du projet.
#
# Vous pouvez tester votre projet avec la commande :
#
#   python3 tests1.py chemin/vers/votre/executable

import os
import subprocess
import sys



PROGRAM_FILE = "program.txt"

PROGRAMS = [
"""
SET 5
PRINT
ADD 10
PRINT
SUB 3
PRINT
""",

"""
PRINT
ADD 5
PRINT
""",

"""
SET 5
PRINT
SUB 8
PRINT
""",

"""
SET 50000
PRINT
ADD 50000
PRINT
""",

"""
SET 5
ADD 6
PRINT
SUB 4
IFNZ
PRINT
SUB 10
IFNZ
PRINT
""",
]

OUTPUTS = [
  [
    "5",
    "15",
    "12",
  ],
  [
    "0",
    "5",
  ],
  [
    "5",
    "0",
  ],
  [
    "50000",
    "65535",
  ],
  [
    "11",
    "7",
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
    if output_line != expected_line:
      print(f"### FAIL ###   Expected '{expected_line}' but output is '{output_line}'", file=sys.stderr)
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
