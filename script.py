#!/usr/bin/python
import argparse
import re

__desc__ = """
This thing takes a file name, reads each line of a file, and tells you if a given line of a file matches a geographically significant number pattern
"""

bDebug = False


re_pattern = re.compile(r"^"
                        r"(?:"
                        r"(?P<NH>00[1-3][^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<ME>00[4-7][^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<VM>00[8-9][^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<RI>03[5-9][^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<CT>04[0-9][^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<NY>(?:0[5-9][0-9]|1[0-2][0-9]|13[0-4]])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<NJ>(?:13[5-9]|14[0-9]|15[0-8])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<PA>(?:159|1[6-9][0-9]|20[0-9]|21[01])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<TX>(?:449|45[0-9]|46[0-7])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<OK>(?:46[89]|47[0-7])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<MA>(?:01[0-9]|02[0-9]|03[0-4])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<MD>(?:21[2-9]|220)[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<DE>(?:221|222)[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<OH>(?:26[89]|2[7-9][0-9]|30[0-2])[^\d]?[\d]{2}[^\d]?[\d]{4})"
                        r")"
                        r"$"
)


def main(number=None, filename=None, outfile='output.tsv',debug=False):
    if number:
        if debug:
            print(number)
        for match in re_pattern.finditer(number):
            print(str(match.lastgroup)+"\t"+match.group(0))
        return
    
    if filename:
        if debug:
            print(filename)
        try:
            f = open('filename','r')
            fw = open(outfile,'w+')
            data = f.read()
            for line in data:
                for match in re_pattern.finditer(line):
                    fw.write(str(match.lastgroup)+'\t'+match.group(0))
            fw.flush()
        except Exception as e:
            print(str(e))
        finally:
            fw.close()
            f.close()
            print(f'output written to {outfile}!')


if __name__=="__main__":
    parser=argparse.ArgumentParser(
        prog='nick_snake_szpikowski',
        description=__desc__
    )
    parser.add_argument('-d', '--debug',action='store_true')
    parser.add_argument('-o', '--outfile')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f','--filename')
    group.add_argument('-n','--number')

    args = parser.parse_args()
    
    if args.number:
        main(number=args.number,debug=args.debug)
    elif args.filename:
        main(filename=args.filename,outfile=args.outfile,debug=args.debug)
    