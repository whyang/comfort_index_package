"""
Created on Jan. 31, 2020

@author: whyang
"""
# -*- coding: utf-8 -*-
import datetime
import pandas as pd

#######################################################################################
# declare emulated CI(Comfort Index) of the Running Biji                              #
#######################################################################################
###
# standalone version of the emulation for CI
#
class ciEmulatedStandalone:
    def __init__(self): 
        pass

    ###
    # declare functions
    #
    # query the CI based on the specific set of the parameters combination
    
    def queryCI(self, p1, p2, p3, p4, p5, p6, p7, temp, grade, rank, x1, x2, x3, x4):
        # set initial value of the used variables
        CI = ''
        _rule = f1 = f2 = fci = 0

        # iterative loop of checking up on the three rules
        # check up on the rule 1
        if (p1 <= grade[4]) | (p2 <= grade[4]) | (p3 <= grade[4]) | (p4 <= grade[4]) | (p5 <= grade[4]) | (p6 <= grade[4]) | (p7 <= grade[4]):
            _rule = 1
            CI = rank[4]
        else:
            # check up on the rule 2
            if (

                    ((p1 <= grade[3]) & (p2 <= grade[3])) | ((p1 <= grade[3]) & (p3 <= grade[3])) | ((p1 <= grade[3]) & (p4 <= grade[3])) | ((p1 <= grade[3]) & (p5 <= grade[3])) | ((p1 <= grade[3]) & (p6 <= grade[3])) | ((p1 <= grade[3]) & (p7 <= grade[3]))
                    | ((p2 <= grade[3]) & (p3 <= grade[3])) | ((p2 <= grade[3]) & (p4 <= grade[3])) | ((p2 <= grade[3]) & (p5 <= grade[3])) | ((p2 <= grade[3]) & (p6 <= grade[3])) | ((p2 <= grade[3]) & (p7 <= grade[3]))
                    | ((p3 <= grade[3]) & (p4 <= grade[3])) | ((p3 <= grade[3]) & (p5 <= grade[3])) | ((p3 <= grade[3]) & (p6 <= grade[3])) | ((p3 <= grade[3]) & (p7 <= grade[3]))
                    | ((p4 <= grade[3]) & (p5 <= grade[3])) | ((p4 <= grade[3]) & (p6 <= grade[3])) | ((p4 <= grade[3]) & (p7 <= grade[3]))
                    | ((p5 <= grade[3]) & (p6 <= grade[3])) | ((p5 <= grade[3]) & (p7 <= grade[3]))
                    | ((p6 <= grade[3]) & (p7 <= grade[3]))) :
                        _rule = 2
                        CI = rank[3]
            else:
                # check up on the rule 3

                # get f1
                minimum = lambda m, n: m if m <= n else n
                f1 = minimum(p1, p2)

                # get f2
                f2 = minimum(p3*p4*p7, p5*p6*p7)

                if temp > 40:
                    f2 = 0.0001
                else:
                    if temp >12:
                        f2 = p3 * p4 * p7
                    else:
                        if temp >= 0:
                            f2 = p5 * p6 * p7
                        else:
                            f2 = 0.0001

                # get fci
                fci = f1 * f2

                # indicate the qualified rule number
                _rule = 3
                if (fci > x1):
                    CI = rank[0]
                else:
                    if (fci > x2):
                        CI = rank[1]
                    else:
                        if (fci > x3):
                            CI = rank[2]
                        else:
                            if (fci > x4):
                                CI = rank[3]
                            else:
                                CI = rank[4]
        # end of the iterative loop of checking up on the three rules

        # present the checking result
        '''
        print('p1 = ', p1)
        print('p2 = ', p2)
        print('p3 = ', p3)
        print('p4 = ', p4)
        print('p5 = ', p5)
        print('p6 = ', p6)
        print('p7 = ', p7)
        print('temp = ', temp)
        print('x1 = ', x1)
        print('x2 = ', x2)
        print('x3 = ', x3)
        print('x4 = ', x4)
        print('p3*p4*p7 = ', p3*p4*p7)
        print('p5*p6*p7 = ', p5*p6*p7)
        print('f1 = ', f1)
        print('f2 = ', f2)
        print('fci = ', fci)
        print('**** rule = ', _rule)
        print('**** CI = ', CI)
        '''

        return CI, _rule
    ##
    # end of queryCI(..)
    #

    # query the CIs based on the all sets of the parameters combination
    def queryallCI(self, cipath, temp_period, grade, rank, x1, x2, x3, x4):
        ##
        # seperate to five parts to gather the emulated results depending on the element of the parameter p1
        #
        df = ['df0', 'df1', 'df2', 'df3', 'df4'] # dataframe's name corresponding to each part
        name = datetime.datetime.now().strftime("%Y%m%d") # get the date of today
        df_filename = ['AQI=優_'+name, 'AQI=好_'+name, 'AQI=普通_'+name, 'AQI=不良_'+name, 'AQI=劣_'+name] # filename of each party
        i = 0
        # iterative loop based on the p1
        for p1 in grade:
            filename = 'ci_emulated_'+df_filename[i]+'.csv'
            print('**** p1 = ', p1)
            # given the column names of the table
            df[i] = pd.DataFrame(columns=('p1(AQI)', 'p2(PM2.5)', 'p3(HI)', 'p4(UVI)', 'p5(WCI)', 'p6(WR)', 'p7(RF)',
                                         'temperature', 'CI(Rank)','qualified_rule'))
            # iterative loop
            for p2 in grade:
                for p3 in grade:
                    for p4 in grade:
                        for p5 in grade:
                            for p6 in grade:
                                for p7 in grade:
                                    for temp in temp_period:
                                        _CI, _rule = self.queryCI(p1, p2, p3, p4, p5, p6, p7, temp, grade, rank, x1, x2, x3, x4)
                                        # construct the content of a row in the table
                                        s = pd.Series({'p1(AQI)':p1,
                                                      'p2(PM2.5)':p2,
                                                      'p3(HI)':p3,
                                                      'p4(UVI)':p4,
                                                      'p5(WCI)':p5,
                                                      'p6(WR)':p6,
                                                      'p7(RF)':p7,
                                                      'temperature':temp,
                                                      'CI(Rank)':_CI,
                                                      'qualified_rule':_rule})
                                        df[i] = df[i].append(s, ignore_index=True)

            # end of iterative loop
            # drop out to store as a file
            #
            df[i].to_csv(cipath+filename, index=False, encoding='cp950')
            i += 1

            # end of iterative loop based on the p1

        return True
        # end of queryallCI(..)

#
# end of ciEmulatedStandalone
###

#######################################################################################
# end of file                                                                         #
#######################################################################################
