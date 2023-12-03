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
      if (body[pos].get("value") == "println"):
        parsed += f"PrintLn(ac=-1, args=["
      elif (body[pos].get("value") == "add"):
        parsed += f"Add(ac=-1, args=["
      elif (body[pos].get("value") == "sub"):
        parsed += f"Sub(ac=-1, args=["
      elif (body[pos].get("value") == "mul"):
        parsed += f"Mul(ac=-1, args=["
      elif (body[pos].get("value") == "div"):
        parsed += f"Div(ac=-1, args=["
      elif (body[pos].get("value") == "toInt"):
        parsed += f"ToInt(ac=1, args=["
      elif (body[pos].get("value") == "toFloat"):
        parsed += f"ToFloat(ac=1, args=["
      elif (body[pos].get("value") == "let"):
        parsed += f"Let(ac=2, args=["
      elif (body[pos].get("value") == "val"):
        parsed += f"Val(ac=1, args=["
      elif (body[pos].get("value") == "input"):
        parsed += f"Input(ac=0, args=["

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
