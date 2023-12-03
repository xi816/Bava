def parse(toks):
  pos = 0

  body = toks["body"]

  parsed = ""

  opened = 0
  opargs = []

  while (body[pos].get("EOF") is None):
    if (body[pos].get("kw")) and (body[pos+1].get("actual") == "openbr"):
      if (len(opargs) > 0):
        if (opargs[-1] > 0):
          parsed += ", "
      curkw = body[pos].get("value")
      curac = body[pos].get("ac")
      if (curkw == "println"):
        parsed += f"PrintLn(ac={curac}, args=["
      elif (curkw == "add"):
        parsed += f"Add(ac={curac}, args=["
      elif (curkw == "sub"):
        parsed += f"Sub(ac={curac}, args=["
      elif (curkw == "mul"):
        parsed += f"Mul(ac={curac}, args=["
      elif (curkw == "div"):
        parsed += f"Div(ac={curac}, args=["
      elif (curkw == "toInt"):
        parsed += f"ToInt(ac={curac}, args=["
      elif (curkw == "toFloat"):
        parsed += f"ToFloat(ac={curac}, args=["
      elif (curkw == "let"):
        parsed += f"Let(ac={curac}, args=["
      elif (curkw == "val"):
        parsed += f"Val(ac={curac}, args=["
      elif (curkw == "input"):
        parsed += f"Input(ac={curac}, args=["
      elif (curkw == "array"):
        parsed += f"Array(ac={curac}, args=["
      elif (curkw == "elem"):
        parsed += f"Elem(ac={curac}, args=["
      elif (curkw == "set"):
        parsed += f"SetElem(ac={curac}, args=["

      pos += 2
      opened += 1
      if (len(opargs) > 0):
        opargs[-1] += 1
      opargs.append(0)
    else:
      if (body[pos]["actual"] == "closebr"):
        assert (opened >= 0), "Trying to close the function but it never opened"
        parsed += "])"
        pos += 1
        opened -= 1
        opargs.pop()
      elif (body[pos]["actual"] == "int"):
        if (len(opargs) > 0):
          if (opargs[-1] > 0):
            parsed += ", "
        parsed += f"Int(value={body[pos]['value']})"
        pos += 1
        opargs[-1] += 1
      elif (body[pos]["actual"] == "ident"):
        if (len(opargs) > 0):
          if (opargs[-1] > 0):
            parsed += ", "
        parsed += f"Ident(name=\"{body[pos]['value']}\")"
        pos += 1
        opargs[-1] += 1
      elif (body[pos]["actual"] == "float"):
        if (len(opargs) > 0):
          if (opargs[-1] > 0):
            parsed += ", "
        parsed += f"Float(value={body[pos]['value']})"
        pos += 1
        opargs[-1] += 1
      elif (body[pos]["actual"] == "string"):
        if (len(opargs) > 0):
          if (opargs[-1] > 0):
            parsed += ", "
        parsed += f"String(value=\"{body[pos]['value']}\")"
        pos += 1
        opargs[-1] += 1
      else:
        assert False, f"PARSER => ERROR => Unexpected `{body[pos]}` at position {pos}"
      if (len(opargs) == 0):
        parsed += "\n"
  return parsed
