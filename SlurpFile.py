#!/usr/bin/python3.6

import bz2
import gzip
import hashlib
import json
import numpy 
import secrets
import sys

#import os
#import shutil

from colorama   import Fore,          Back,  Style 
from contextlib import contextmanager              
from datetime   import datetime                    
from pathlib    import Path                        
from tabulate   import tabulate       as     pt    
from termcolor  import colored,       cprint       
from time       import time                        

###########
#  def's  #
###########



@contextmanager
def runtime(description):
  print(f"{'-i-'}", flush=True, end=' ')
  pConM(f"{description:>16}", 4)
  start_time = time()
  try:
    yield
  finally:
    end_time = time()
    run_time = end_time - start_time
    pConM( f"-i-above function took ", 1, " ")
    pConM( f" {run_time:>16} ", 24, " ")
    pConM( f" seconds to run.", 1)


def pCON(str='', Fgnd='blue', endc='\n'):  
    """ """#vim_folder_<<<
    if sys.stdout.isatty():
        print(Style.BRIGHT, end="")
        if 'blue' in Fgnd.lower():
            print(Fore.BLUE + Back.BLACK + f"{str}", flush=True, end=endc)
        elif 'cyan' in Fgnd.lower():
            print(Fore.CYAN + Back.BLACK + f"{str}", flush=True, end=endc)
        elif 'green' in Fgnd.lower():
            print(Fore.GREEN + Back.BLACK + f"{str}", flush=True, end=endc)
        elif 'magenta' in Fgnd.lower():
            print(Fore.MAGENTA + Back.BLACK + f"{str}", flush=True, end=endc)
        elif 'red' in Fgnd.lower():
            print(Fore.RED + Back.BLACK + f"{str}", flush=True, end=endc)
        elif 'yellow' in Fgnd.lower():
            print(Fore.YELLOW + Back.BLACK + f"{str}", flush=True, end=endc)
        elif 'white' in Fgnd.lower():
            print(Fore.WHITE + Back.BLACK + f"{str}", flush=True, end=endc)
        else:
            print(Fore.WHITE + Back.BLACK + f"{str}", flush=True, end=endc)
        print(Style.RESET_ALL, end="")
    else:
        print(f"{str}", flush=True, end=endc)


#vim_folder_>>>

def LoadJson(fin):
  """ to load from (possibly zipped) text json file """
  str0 = SlurpFileZipOkay(fin)
  lA3 = json.loads(str0)
  return lA3


def Dump2Json(fon2, obj):
  """  """  #vim_folder_<<<
  fon2Obj = Path(fon2)
  lSu = fon2Obj.suffix
  fon3 = fon2Obj.resolve()
  fon3s = str(fon3)
  if "bz2" in lSu.lower():
    with bz2.open(fon3, 'wt') as fo:
      json.dump(obj, fo)
  elif "gz" in lSu.lower():
    with gzip.open(fon3, 'wt') as fo:
      json.dump(obj, fo)
  else:
    with open(fon3, mode='wt') as fo:
      json.dump(obj, fo)
  print(f"-i-writing into ", flush=True, end=" ")
  pConM(f"{fon3s:>16}", 4)

#vim_folder_>>>


def SlurpFileZipOkay(fileN):
  """ """# <<<
  fileNObj = Path(fileN)
  if fileNObj.is_file():
    pass
  else:
    pConM('-W-', 2, ' ')
    print(f" cannot see file ", flush=True, end=" ")
    pConM(fileN, 18, '\n\n')
    return 0
  absFileN = fileNObj.resolve()
  print(f"-i- reading file ", flush=True, end=" ")
  pConM(str=absFileN, Fgnd=4, endc='\n\n')
  bin1 = absFileN.read_bytes()
  FileExt = absFileN.suffix
  if 'gz' in FileExt:
    str1 = gzip.decompress(bin1).decode("utf-8")
  elif 'bz2' in FileExt:
    str1 = bz2.decompress(bin1).decode("utf-8")
  else:
    str1 = bin1.decode("utf-8")
  return str1
# >>>

#    str1 = absFileN.read_text()


def YWStr():
    td = datetime.today()
    return td.strftime("%yww%Vd%u%H")

def GetRndHex(length=16):
  kyb4=bytes(GetRndStr(), encoding='utf-8' )
  md4 = hashlib.sha3_512(kyb4).hexdigest()
  return md4[0:length]

def GetRndStr(nbits=10):
    bbits = int(nbits / 0.30103)
    rnd = secrets.randbits(bbits)
    rnd2 = '{:0{width}d}'.format(rnd, width=nbits)
    return rnd2

def YWRand():
    yw = YWStr()
    rnd = GetRndStr()
    return yw + "." + rnd


def YWRHex():
    yw = YWStr()
    rnd = GetRndHex(8)
    return yw + "." + rnd

def pConM(str='', Fgnd=1, endc='\n'):  
#vim_folder_<<<
    if sys.stdout.isatty():
        dictC = {
            0: {
                "fg": "white",
                "att": ['bold']
            },
            1: {
                "fg": "green",
                "att": []
            },
            2: {
                "fg": "red",
                "att": []
            },
            3: {
                "fg": "yellow",
                "att": []
            },
            4: {
                "fg": "blue",
                "att": ['bold']
            },
            5: {
                "fg": "magenta",
                "att": []
            },
            6: {
                "fg": "white",
                "att": ['reverse']
            },
            7: {
                "fg": "cyan",
                "att": []
            },
        }
        dictAt = {
            0: [],
            1: ["underline"],
            2: ["bold"],
            3: ["bold", "underline"]
        }
        Fgnd2 = Fgnd / len(dictC)
        Fgnd2 %= len(dictAt)
        Fgnd2 = int(Fgnd2)
        Fgnd %= len(dictC)
        if Fgnd in dictC:
            dictC0 = dictC[Fgnd]
            list0 = dictC0["att"]
            list0 += dictAt[Fgnd2]
            cprint(str, dictC0["fg"], 'on_grey', attrs=list0, end=endc)
        else:
            cprint(str, 'white', 'on_grey', ['underline'], end=endc)
    else:
        print(f"{str}", flush=True, end=endc)


#vim_folder_>>>

def p2Dim(ndA, ColorCode=4, tf='pretty'):
  # <<<
  """TODO: Docstring for p2Dim.
  """
  # dTabFmt = dict(f1='fancy_grid', f2='github', f3='grid', f4='pipe', f5='plain', f6='presto', f7='pretty', f8='simple')
  if isinstance(ndA, numpy.ndarray):
    if ndA.ndim == 2:
      pConM(pt(ndA, tablefmt=tf), ColorCode)
    else:
      pConM(ndA, ColorCode)
      pass
  elif isinstance(ndA, list):
    boolLoL = any(isinstance(el, list) for el in ndA)
    if boolLoL:
      pConM(pt(ndA, tablefmt=tf), ColorCode)
    else:
      pConM([ndA], ColorCode)
    pass
  else:
    pConM(ndA, ColorCode)
    pass


# >>>



#grey
#red
#green
#yellow
#blue
#magenta
#cyan
#white



#bold
#dark
#underline
#blink
#reverse
#concealed


