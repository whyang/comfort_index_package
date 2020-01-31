"""
Created on Jan. 31, 2020
@author: whyang

present the emulated CI(Comfort Index) of the running biji

"""

###
# USAGE (example of command)
# python ci_emulated_package_20200131.py --query one -p1 1 -p2 1 -p3 1 -p4 1 -p5 1 -p6 1 -p7 1 -t 20
# python ci_emulated_package_20200131.py --query all -p1 1 -p2 1 -p3 1 -p4 1 -p5 1 -p6 1 -p7 1 -t 20
##

# -*- coding: utf-8 -*-
import os
import argparse
from comfortindexpackage.ciEmulated import ciEmulatedStandalone # the emulated comfort index (CI) (standalone version)

###
# function of entry point
#
def doCIEmulation():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-q", "--query", required=True, help="query one CI or all of the CIs based on the set of parameters combination")
    ap.add_argument("-p1", "--parameter1", required=True, help="p1: AQI")
    ap.add_argument("-p2", "--parameter2", required=True, help="p2: PM 2.5")
    ap.add_argument("-p3", "--parameter3", required=True, help="p3: HI")
    ap.add_argument("-p4", "--parameter4", required=True, help="p4 UVI")
    ap.add_argument("-p5", "--parameter5", required=True, help="p5: WCI")
    ap.add_argument("-p6", "--parameter6", required=True, help="p6: WR")
    ap.add_argument("-p7", "--parameter7", required=True, help="p7: RF")
    ap.add_argument("-t", "--temperature", required=True, help="temp: temperature")
    args = vars(ap.parse_args())
            
    ##
    # query specific parameter combination for the emulated CI
    # set the value of the each parameter
    grade = [1, 0.9, 0.8, 0.4, 0.2] # g1, g2, g3, g4 and g5 w.r.t. 優, 好, 普通, 不良 and 劣
    rank = ['優', '好', '普通', '不良', '劣']
    temp_period = [41, 13, 0, -1]
    x1 = pow(grade[1], 4)
    x2 = pow(grade[2], 4)
    x3 = pow(grade[3], 4)
    x4 = pow(grade[4], 4)
               
    if args['query'] == 'all':
        # folder to store all of the CI tables
        cipath = '.\\CI_table\\'  # directory of the table of the emulated CIs
        if not os.path.isdir(cipath):
            os.mkdir(cipath)    
        # query all parameters combination for the emulated CI
        ciEmul = ciEmulatedStandalone()
        ciEmul.queryallCI(cipath, temp_period, grade, rank, x1, x2, x3, x4)
        print('**** finished')
    elif args['query'] == 'one':
        p1 = float(args['parameter1'])
        p2 = float(args['parameter2'])
        p3 = float(args['parameter3'])
        p4 = float(args['parameter4'])
        p5 = float(args['parameter5'])
        p6 = float(args['parameter6'])
        p7 = float(args['parameter7'])
        temp = float(args['temperature'])        
        # call queryCI() to get the result
        ciEmul = ciEmulatedStandalone()
        _CI, _rule = ciEmul.queryCI(p1, p2, p3, p4, p5, p6, p7, temp, grade, rank, x1, x2, x3, x4)
        # present the query result
        print(_CI)
        print(_rule)
        print('**** finished')
    else:
        print('**** error: input argument')

    print('== end of query ==')

###
# main program
#
if __name__ == '__main__':
    doCIEmulation()

#######################################################################################
# end of file                                                                         #
#######################################################################################