#!/usr/bin/python
import argparse
import re

from _version import __desc__
from _version import __version__

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
                        r"(?P<OH>(?:26[89]|2[7-9][0-9]|30[0-2])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<VA>(?:22[3-9]|23[01])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<NC>(?:232)[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<WV>(?:23[2-6])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<SC>(?:24[789]|25[01])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<GA>(?:25[2-9]|260)[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<FL>(?:26[1-7])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<IN>(?:30[3-9]|31[0-7])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<IL>(?:31[89]|3[2-5][0-9]|36[01])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<MI>(?:36[2-9]|37[0-9]|38[0-6])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<WI>(?:38[789]|39[0-9])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<KY>(?:40[0-7])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<TN>(?:40[89]|41[0-5])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<AL>(?:41[0-6]|42[0-4])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<MS>(?:42[5-8])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<AR>(?:429|43[0-2])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<LA>(?:43[3-9])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<MN>(?:46[89]|47[0-7])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<IA>(?:47[89]|48[0-5])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<MO>(?:48[6-9]|49[0-9]|500)[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<ND>(?:50[12])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<SD>(?:50[34])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<NE>(?:50[5-8])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<KS>(?:509|51[0-5])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<MT>(?:51[67])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<ID>(?:51[89])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<WY>(?:520)[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<CO>(?:52[1-4])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<NM>(?:525|585)[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<AZ>(?:52[67])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<UT>(?:52[89])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<NV>(?:530|680)[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<WA>(?:53[1-9])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<OR>(?:54[0-4])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<CA>(?:54[5-9]|5[5-6][0-9]|57[0-3])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<AK>(?:574)[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<HI>(?:57[56])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<DoC>(?:57[7-9])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<VirginIslands>(?:580)[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<PR>(?:58[0-4])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<Guam_AmSamoa_Philipns>(?:586)[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<Not_Issued>(?:58[7-9]|23[7-9]|24[0-6]|59[0-9]|6[0-5][0-9]|66[0-5]|66[7-9]|67[0-9]|68[1-9]|69[0-9]|7[56][0-9]|77[0-2])[^\d]?[\d]{2}[^\d]?[\d]{4})|"
                        r"(?P<Railroad_Board>(?:7[01][0-9]|72[0-8]|23[7-9]|24[0-6])[^\d]?[\d]{2}[^\d]?[\d]{4})"
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
        prog=f'nick_snake_szpikowski v{__version__}',
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
    