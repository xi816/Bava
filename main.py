import os
import sys

import slex
import sparse
import sevaluate

from pprint import pprint

CFILE = os.path.dirname(__file__)

assert (len(sys.argv) > 1), "BUILDER => ERROR => Expected file name"
assert (sys.argv[1].endswith(".bava")), f"BUILDER => ERROR => File extension `{sys.argv[1].split('.')[-1]}` is not supported. You need to use `.bava`"
srcFile = sys.argv[1]
if (len(sys.argv) > 2):
  needDebug = sys.argv[2] in ["-d", "-debug"]
else:
  needDebug = False

with open(f"{CFILE}/{srcFile}", "r") as fl:
  cdr = fl.read()
toks = slex.lex(cdr)

if (needDebug):
  print("LEXER => NOTE => Lexing is success!")
  print(f"LEXER => NOTE =>\n{toks}")

if (not os.path.exists("build/")):
  os.makedirs("build/")
slex.jsonOut(f"build/{'.'.join(srcFile.split('.')[:-1]).split('/')[-1]}.bava.json", toks)

btree = sparse.parse(toks)
with open(f"build/{'.'.join(srcFile.split('.')[:-1]).split('/')[-1]}-tree.bava.ast", "w") as fl:
  fl.write(btree)

if (needDebug):
  print("PARSER => NOTE => Parsing is success!")
  print(f"EVALUATOR => NOTE => Evaluation code:\n{btree}")

  print("\nOutput:")

sevaluate.evaluateBava(btree, needDebug)
