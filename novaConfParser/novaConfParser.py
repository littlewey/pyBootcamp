import sys
argVars = sys.argv[1:]
argFormatErrorFlag = True

helpInfo = """

Usage:
  novaConfParser.py [--input <path-to-input-file>] [--par <par>]
Options:
  --help       Show this help screen.
Examples:
  python3 novaConfParser.py --input /nova/nova.conf --par my_ip

"""

# parse parseArgVars
def parseArgVars(argVars, flag):
  # init for filePath, par
  filePath, par = str(), str()
  if len(argVars) == 4:
    if "--input" and "--par" in [argVars[0], argVars[2]]:
      # if in order: --input x --par y
      filePath, par = argVars[1], argVars[3]
      # argFormatErrorFlag is valid now
      flag = False
      # switch order if needed, in order: --par x --input y
      if argVars[0] != "--input":
        filePath, par = par, filePath
  return flag, filePath , par

def parse(par,inputList):
  valueForThePar = "oops: there is no " + par + " found."
  for line in inputList:
    line = line.strip().split("=")
    line = [item.strip() for item in line]
    if par == line[0]:
      valueForThePar = line[1]
  return valueForThePar

def readInputFile(path):
  with open(path) as file:
    fileStr = file.read()
  return fileStr.split("\n")

# main process
def main(argVars, argFormatErrorFlag):
  # parse arguments and validate them
  argFormatErrorFlag, filePath, par = parseArgVars(argVars, argFormatErrorFlag)
  # in case argFormatErrorFlag is True, end and print the help info
  if argFormatErrorFlag:
    print (helpInfo)
    # End function without raise errors
    return None
  # Read file as a list
  inputList = readInputFile(filePath)
  # Build final output with parse()
  output = parse(par,inputList)
  # do the output
  print (output)

# run main function
main(argVars, argFormatErrorFlag)
