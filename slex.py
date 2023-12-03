import json

def lex(src):
  src = list(src + "\0")
  pos = 0

  buf = ""
  tokens = {
    "body": []
  }

  DIGITS = "".join(map(chr, range(48, 58)))
  VARLETTERS = "".join(map(chr, list(range(65, 91)) + list(range(97, 123))))
  WHITESPACES = " \n\b\v"

  while (src[pos] != "\0"):
    # print(src[pos], pos)
    if (src[pos] == "~"):
      while (src[pos] != "\n"):
        pos += 1
      pos += 1
    if (src[pos] in DIGITS + "-"):
      if (src[pos] == "-"):
        buf += src[pos]
        pos += 1
      while (src[pos] in DIGITS + "."):
        buf += src[pos]
        pos += 1
      if (buf.count(".") == 0):
        tokens["body"].append({"kw": False, "actual": "int", "value": int(buf)})
      elif (buf.count(".") == 1):
        tokens["body"].append({"kw": False, "actual": "float", "value": float(buf)})
      else:
        assert False, f"Can't parse {buf} as a floating point number"
      buf = ""
    elif (src[pos] in VARLETTERS):
      while (src[pos] in (VARLETTERS + DIGITS)):
        buf += src[pos]
        pos += 1
      if (buf in ["println", "add", "sub", "mul", "div", "array", "elem", "set"]):
        tokens["body"].append({"kw": True, "value": buf, "ac": -1})
      elif (buf in ["input"]):
        tokens["body"].append({"kw": True, "value": buf, "ac": 0})
      elif (buf in ["toInt", "toFloat", "val"]):
        tokens["body"].append({"kw": True, "value": buf, "ac": 1})
      elif (buf in ["let"]):
        tokens["body"].append({"kw": True, "value": buf, "ac": 2})
      else:
        tokens["body"].append({"kw": False, "actual": "ident", "value": buf})
      buf = ""
    elif (src[pos] == "\t"):
      assert False, "LEXER => ERROR => You can't use spaces in indentation"
    elif (src[pos] in WHITESPACES):
      pos += 1
    elif (src[pos] == "\""):
      pos += 1
      while (src[pos] != "\""):
        if (src[pos] == "\n"):
          assert False, "LEXER => ERROR => Unterminated string literal"
        buf += src[pos]
        pos += 1
      tokens["body"].append({"kw": False, "actual": "string", "value": buf})
      buf = ""
      pos += 1
    else:
      while (src[pos] not in (DIGITS + VARLETTERS + WHITESPACES + "\0")):
        buf += src[pos]
        pos += 1
      if (buf == "["):
        tokens["body"].append({"kw": False, "actual": "openbr", "value": None})
      elif (buf == "]"):
        tokens["body"].append({"kw": False, "actual": "closebr", "value": None})
      # elif (all([i == "]" for i in buf])):
      #   for i in range(len(buf)):
      #     tokens["body"].append({"kw": False, "actual": "closebr", "value": None})
      elif (buf[0] == "[") and (len(buf) > 1):
        tokens["body"].append({"kw": False, "actual": "openbr", "value": None})
        pos -= len(buf) - 1
      elif (buf[0] == "]") and (len(buf) > 1):
        tokens["body"].append({"kw": False, "actual": "closebr", "value": None})
        pos -= len(buf) - 1
      # elif (buf[0] == "[") and (all([i == "]" for i in buf[1:]])):
      #   tokens["body"].append({"kw": False, "actual": "openbr", "value": None})
      #   for i in range(len(buf)-1):
      #     tokens["body"].append({"kw": False, "actual": "closebr", "value": None})
      buf = ""

  tokens["body"].append({"EOF": True})
  return tokens

def jsonOut(fln, jsonDict):
  with open(fln, "w") as fl:
    fl.write(json.dumps(jsonDict, indent = 2))
  return 1
