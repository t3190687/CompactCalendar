#!/usr/bin/python3.6
import argparse
import os
import sys
import xlsxwriter as xw
from datetime import (date, timedelta)
from SlurpFile import( pConM, GetRndStr,  YWRHex, )


def CreateWSheet(wsheet, dateO, dictFmt):
  """ """# <<<
  wsheet.set_zoom(120)
  wsheet.set_footer('&C&16&A')
  wsheet.set_row(0, 15)
  wsheet.set_row(1, 16)
  wsheet.set_column(0, 0, 8)
  wsheet.set_column(1, 1, 0.5)
  wsheet.set_column(2, 8, 6)
  wsheet.merge_range(0, 2, 0, 8, "")
  wsheet.write_datetime(0, 2, dateO, dictFmt.get('ft0'))
  wsheet.merge_range(1, 2, 1, 8, "Compact Calendar", dictFmt.get('ftCCal'))

  SWSheetRow_i = 2
  wsheet.set_row(SWSheetRow_i, 25)
  wsheet.write_datetime(SWSheetRow_i, 8, dateO, dictFmt.get('ftd'))
  for i0 in range(2, 8):
    wsheet.write_formula(SWSheetRow_i, i0, '=INDIRECT("RC[+1]",0)-1', dictFmt.get('ftd'))

  SWSheetRow_i += 1
  while SWSheetRow_i < 25:
    wsheet.set_row(SWSheetRow_i, 28)
    i2 = SWSheetRow_i + 1
    i2s = str(i2)
    formulaStr = f"{{=IF(SUM(1*(DAY(C{i2s}:I{i2s})=1))>0,I{i2s}, \"\")}}"
    wsheet.write_formula(SWSheetRow_i, 0, formulaStr, dictFmt.get('ftm'))
    fstr2 = '=INDIRECT("R[-1]C[+6]", 0)+1'
    wsheet.write_formula(SWSheetRow_i, 2, fstr2, dictFmt.get('ftd'))
    for i1 in range(3, 9):
      fstr3 = '=INDIRECT("RC[-1]", 0)+1'
      wsheet.write_formula(SWSheetRow_i, i1, fstr3, dictFmt.get('ftd'))
    SWSheetRow_i += 1

  wsheet.conditional_format('C3:I25', {'type': 'formula', 'criteria': 'IF(DAY(C3)=1, 1, 0)', 'format': dictFmt.get('ft_1stday')})
  wsheet.conditional_format('C3:I25', {'type': 'formula', 'criteria': 'DAY(C3)>DAY(C4)', 'format': dictFmt.get('ft_uline')})
  wsheet.conditional_format('A3:A25', {'type': 'formula', 'criteria': 'IF(MOD(MONTH(I3), 3)=1, 1, 0)', 'format': dictFmt.get('ftMon1')})

# >>>



#####################
#  code main block  #
#####################

def main():
  td = date.today()
  yrStr = td.strftime("%Y")
  Lyear = []
  parser = argparse.ArgumentParser(description='To generate compact calendar in xlsx files ')
  parser.add_argument('--year', '-y', nargs='+', default=yrStr, help='the years for we to print the calendars ')
  args = parser.parse_args()
  print(f"args is ", flush=True)
  print(args, flush=True)
  LYear = []
  yr3 = vars(args).get('year')
  if isinstance(yr3, list):
    LYear = yr3
  else:
    LYear.append(yr3)

  fname2 = YWRHex() + '.xlsx'

  with xw.Workbook(fname2) as wk:
    """ """  # <<<
    pConM(f"{'-i-writing into ':>16}{fname2}", Fgnd=4)
    ft0 = wk.add_format({'num_format': 'dd mmm yyyy'})
    ftd = wk.add_format({'num_format': 'dd', 'font_size': 20, 'align': 'center', 'text_wrap': True, 'font_name': 'Courier New'})
    ftm = wk.add_format({'num_format': 'mmm', 'font_outline': True, 'font_size': 20, 'align': 'center', 'font_name': 'Garamond'})
    ftCCal = wk.add_format({
        'align': 'center',
        'bg_color': '#5757ff',
        'bold': True,
        'border': 0,
        'color': '#f4f4ff',
        'font': 'Garamond',
        'size': 14,
        'text_wrap': True
    })
    #      'font': 'Courier New',

    ft_1stday = wk.add_format({'bold': True, 'bg_color': '#ff9966'})
    ft_uline = wk.add_format({'bottom': 6, 'bottom_color': '#9900cc', 'color': '#5f021f'})
    ftMon1 = wk.add_format({'bg_color': '#90f9b7'})
    dFt = {'ft0': ft0}
    dFt.update(ftCCal=ftCCal)
    dFt.update(ftd=ftd)
    dFt.update(ftm=ftm)
    dFt.update(ft_1stday=ft_1stday)
    dFt.update(ft_uline=ft_uline)
    dFt.update(ftMon1=ftMon1)
    for yr in LYear:
      yr0 = int(yr)
      for mi in range(1, 13):
        tf1 = date(year=yr0, month=mi, day=1)
        dow = tf1.weekday()
        td0 = timedelta(dow + 2)
        tf2 = tf1 - td0
        ywStr2 = tf1.strftime("%yMn%m")
        ws = wk.add_worksheet(ywStr2)
        CreateWSheet(ws, tf2, dFt)



# >>>

#  os.system("/usr/bin/libreoffice --calc --view " + fname2 + " & ")


if __name__ == "__main__":
  main()
