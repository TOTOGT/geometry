#!/usr/bin/env python3
"""
SHIPS lsdiag parser -- derived from the format document, validated on real bytes.

Every constant below was read off the distribution's own "SHIPS Predictor Files,
last updated 2 Oct 2023" PDF and then checked against
data/ships_sample_EP011982.txt, which is the first case of
lsdiage_1982_2022_sat_ts_5day.txt. Four things a reasonable sketch gets wrong,
each of which fails silently:

  1. THE LABEL IS AT THE END OF THE LINE, not the start. The document says it:
     "Each line of the file ends with a line descriptor, and each set of records
     starts with HEAD and ends with LAST." A parser keying on line[:4] finds
     nothing at all and reports an empty dataset rather than an error.

  2. FIELDS ARE 5 CHARACTERS WIDE, not 4, and there are 23 of them
     (-12, -6, 0, 6, ... 120 h at 6-hour steps). 7-day files run to 168 h.

  3. ROWS HAVE BLANK LEADING FIELDS, not shifted values. HIST, U200, E000 and
     others start at t = 0 with the -12 and -6 columns left blank. Splitting on
     whitespace silently shifts those rows two places left and misaligns every
     value against its time.

  4. RSST, DSST and DSTA CARRY A TRAILING NUMBER after the label -- the age in
     days of the SST analysis. Taking the last whitespace token as the label
     reads those three rows as a variable called "1".

And the one that decides the experiment:

  CSST is the CLIMATOLOGICAL SST. RSST is weekly Reynolds, DSST is daily
  Reynolds, DSTA is daily Reynolds averaged over five points (centre and
  +50 km N/E/S/W). For a test asking whether the ENVIRONMENT determines the
  storm's state, the control must be observed, not climatological: a
  climatological field is a function of position and calendar date, so a loop
  in it is partly a re-encoding of the track. Use DSTA. CSST is the confound
  that holonomy-test.py block [5] exists to catch.

Missing / not-available is 9999 everywhere, including land cases for DELV and
INCV. Values are integers scaled by 10 for degrees C and degrees N/W.
"""

NVALS, WIDTH, MISSING = 23, 5, 9999

def parse_cases(path, nvals=NVALS):
    """Yield one dict per storm case: HEAD fields plus {label: [values]}."""
    block = []
    with open(path, encoding='utf-8-sig') as f:
        for line in f:
            line = line.rstrip('\n')
            label = line[nvals*WIDTH:nvals*WIDTH+5].strip()
            if label == 'HEAD':
                if block: yield _case(block, nvals)
                block = [line]
            elif block:
                block.append(line)
                if label == 'LAST':
                    yield _case(block, nvals); block = []
    if block: yield _case(block, nvals)

def _case(block, nvals):
    head = block[0][:nvals*WIDTH].split()
    case = {'name': head[0] if head else '', 'yymmdd': head[1] if len(head) > 1 else '',
            'hour': head[2] if len(head) > 2 else '',
            'atcf': head[-1] if head else '', 'rows': {}}
    for line in block[1:]:
        label = line[nvals*WIDTH:nvals*WIDTH+5].strip()
        if not label or label in ('HEAD', 'LAST'): continue
        vals = []
        for i in range(nvals):
            fld = line[i*WIDTH:(i+1)*WIDTH]
            if not fld.strip(): vals.append(None); continue
            try: v = int(fld)
            except ValueError: vals.append(None); continue
            vals.append(None if v == MISSING else v)
        case['rows'][label] = vals
    return case

if __name__ == '__main__':
    import sys
    src = sys.argv[1] if len(sys.argv) > 1 else 'data/ships_sample_EP011982.txt'
    ok, bad = [], []
    for c in parse_cases(src):
        r = c['rows']
        print('case %-6s %s %sZ  %s   rows: %d' %
              (c['name'], c['yymmdd'], c['hour'], c['atcf'], len(r)))
        if 'TIME' in r:
            ok.append(r['TIME'][:4] == [-12, -6, 0, 6])
        if 'LAT' in r and 'CSST' in r and 'DSTA' in r:
            i = 2
            print('   t=0:  lat %.1f N   CSST %.1f C   DSTA %.1f C   vmax %s kt' %
                  (r['LAT'][i]/10, r['CSST'][i]/10, r['DSTA'][i]/10, r['VMAX'][i]))
            ok.append(r['CSST'][i] != r['DSTA'][i])
        if 'VMAX' in r:
            ok.append(r['VMAX'][0] is None)          # 9999 became None
        if 'HIST' in r:
            ok.append(r['HIST'][0] is None and r['HIST'][2] is not None)
    print('\n%d/%d structural checks passed' % (sum(ok), len(ok)))
