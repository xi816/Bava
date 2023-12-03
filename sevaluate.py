from copy import deepcopy as dcopy
from dataclasses import dataclass

# assert (len(args) == ac), f"EVALUATOR => ERROR => Function `function` expects 1 argument, but got {len(args)}"

VARS = {}
CLARGS = []

@dataclass
class IdentLit:
  val: str

class ArrayLit:
  def __init__(self, buf):
    self.cont = buf

  def __repr__(self):
    s = "{"
    for i, j in enumerate(self.cont):
      if (i != len(self.cont)-1):
        s += str(j) + " "
      else:
        s += str(j)
    return s + "}"

def PrintLn(ac, args):
  for el in args:
    print(el, end = "")
  print()
  return 0

def Add(ac, args):
  if (all([type(i) in [int, float] for i in args])):
    return sum(args)
  return False

def Sub(ac, args):
  if (all([type(i) in [int, float] for i in args])):
    ars = list(reversed(dcopy(args)))
    while (len(ars) > 1):
      ars[-1] -= ars[-2]
      ars.pop(-2)
    return ars[0]
  return False

def Mul(ac, args):
  if (all([type(i) in [int, float] for i in args])):
    ars = list(reversed(dcopy(args)))
    while (len(ars) > 1):
      ars[-1] *= ars[-2]
      ars.pop(-2)
    return ars[0]
  return False

def Div(ac, args):
  if (all([type(i) in [int, float] for i in args])):
    ars = list(reversed(dcopy(args)))
    while (len(ars) > 1):
      ars[-1] /= ars[-2]
      ars.pop(-2)
    return ars[0]
  return False

def ToInt(ac, args):
  assert (len(args) == ac), f"EVALUATOR => ERROR => Function `toInt` expects 1 argument, but got {len(args)}"
  assert (type(args[0]) is not int), "EVALUATOR => ERROR => Trying to convert type INT to type INT"
  assert (type(args[0]) in [float, str]), f"EVALUATOR => ERROR => Trying to convert type {type(args[0])} to type INT"
  return int(args[0])

def ToFloat(ac, args):
  assert (len(args) == 1), f"EVALUATOR => ERROR => Function `toFloat` expects 1 argument, but got {len(args)}"
  assert (type(args[0]) is not float), "EVALUATOR => ERROR => Trying to convert type FLOAT to type FLOAT"
  assert (type(args[0]) in [int, str]), f"EVALUATOR => ERROR => Trying to convert type {type(args[0])} to type FLOAT"
  return float(args[0])

def Let(ac, args):
  assert (type(args[0]) is IdentLit), "EVALUATOR => ERROR => Name of variable is already taken by builtin"
  VARS[args[0].val] = args[1]

def Val(ac, args):
  assert (type(args[0]) is IdentLit), "EVALUATOR => ERROR => Trying to get a value from a builtin keyword"
  assert (len(args) == ac), f"EVALUATOR => ERROR => Function `val` expects 1 argument, but got {len(args)}"
  return VARS[args[0].val]

def Int(value):
  return int(value)
def Float(value):
  return float(value)
def String(value):
  return str(value)
def Array(ac, args):
  return ArrayLit(args)

def Elem(ac, args):
  assert (len(args) >= 2), f"EVALUATOR => ERROR => Function `elem` expects at least 2 arguments, but got {len(args)}"
  assert (type(args[0]) is IdentLit), f"EVALUATOR => ERROR => Function `elem` expects type IDENT as a first argument"
  s = "VARS[args[0].val].cont"
  for i in args[1:]:
    s += f"[{i}]"
  return eval(s)

def SetElem(ac, args):
  assert (len(args) >= 3), f"EVALUATOR => ERROR => Function `set` expects at least 2 arguments, but got {len(args)}"
  assert (type(args[0]) is IdentLit), f"EVALUATOR => ERROR => Function `set` expects type IDENT as a first argument"
  s = f"VARS[args[0].val].cont"
  for i in args[2:]:
    s += f"[{i}]"
  return exec(s + f" = {args[1]}")

def Ident(name):
  return IdentLit(name)

def Input(ac, args):
  inp = input()
  return inp

def evaluateBava(code, clargs):
  global CLARGS
  CLARGS = clargs
  exec(code)
