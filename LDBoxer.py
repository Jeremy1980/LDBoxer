'''
Created on 16 mar 2017
Updated on 24 jan 2018
@author: Tore Eriksson <tore.eriksson@mbox325.swipnet.se>
@author: Jeremy Czajkowski
@author: Michael Horvath
@license: GNU General Public License version 3
@version: 2018c
@note: A utility to help you replace LDraw parts with no visible studs or tubes with boxes. 
       Saves rendering time and CPU power.
       This script will fail on four letter file extansions, such as "xmpd".
'''

import os
import sys
from macpath import dirname

__appname__ = "LDBoxer"
__version__ = "2018c"

NOTFOUND_MSG = "FileNotFoundError: [Errno 2] No such file or directory: '%s'"
INVALIDACCESS_MSG = "ImportError: Invalid access to %s."

CHKLST_INFILE = []
CHKLST_INCHEK = []
REPLACEDTOTAL_COUNT = 0
STR_PREFIXES = ['B\\', 'B\\T', 'B\\B']

LDRAWPATH = MODELPATH = ''


def ldLineType(ldline):
    result = -1
    s = ldline.strip()
    if len(s)>0 :
        if s[0]=='0' : result = 0
        if s[0]=='1' : result = 1
        if s[0]=='2' : result = 2
        if s[0]=='3' : result = 3
        if s[0]=='4' : result = 4
        if s[0]=='5' : result = 5
    return result


def ldLineUpdate(ldline, ItemNr, NewVal):
    color1 = ldExtractFromLine(ldline, 2)
    x1 = float(ldExtractFromLine(ldline, 3))
    y1 = float(ldExtractFromLine(ldline, 4))
    z1 = float(ldExtractFromLine(ldline, 5))
    a1 = float(ldExtractFromLine(ldline, 6))
    b1 = float(ldExtractFromLine(ldline, 7))
    c1 = float(ldExtractFromLine(ldline, 8))
    d1 = float(ldExtractFromLine(ldline, 9))
    e1 = float(ldExtractFromLine(ldline, 10))
    f1 = float(ldExtractFromLine(ldline, 11))
    g1 = float(ldExtractFromLine(ldline, 12))
    h1 = float(ldExtractFromLine(ldline, 13))
    i1 = float(ldExtractFromLine(ldline, 14))
    fil = ldExtractFromLine(ldline, 15)
    
    if ItemNr == 2:
        color1 = NewVal
    if ItemNr == 3:
        x1 = float(NewVal)
    if ItemNr == 4:
        y1 = float(NewVal)
    if ItemNr == 5:
        z1 = float(NewVal)
    if ItemNr == 6:
        a1 = float(NewVal)
    if ItemNr == 7:
        b1 = float(NewVal)
    if ItemNr == 8:
        c1 = float(NewVal)
    if ItemNr == 9:
        d1 = float(NewVal)
    if ItemNr == 10:
        e1 = float(NewVal)
    if ItemNr == 11:
        f1 = float(NewVal)
    if ItemNr == 12:
        g1 = float(NewVal)
    if ItemNr == 13:
        h1 = float(NewVal)
    if ItemNr == 14:
        i1 = float(NewVal)
    if ItemNr == 15:
        fil = NewVal
    
    s = '1 ' + color1 + ' '
    s = s + FloatToLDraw(x1)+ ' '
    s = s + FloatToLDraw(y1)+ ' '
    s = s + FloatToLDraw(z1)+ ' '
    s = s + FloatToLDraw(a1)+ ' '
    s = s + FloatToLDraw(b1)+ ' '
    s = s + FloatToLDraw(c1)+ ' '
    s = s + FloatToLDraw(d1)+ ' '
    s = s + FloatToLDraw(e1)+ ' '
    s = s + FloatToLDraw(f1)+ ' '
    s = s + FloatToLDraw(g1)+ ' '
    s = s + FloatToLDraw(h1)+ ' '
    s = s + FloatToLDraw(i1)+ ' '
    s = s + fil
    return s


def ldExtractFromLine (ldline, post):
    a = ldline.split()
    if post <= len(a):
        return a[post-1]
    return '' 


def FloatToLDraw(inval):
    if (inval > -0.0001) and (inval < 0.0001): inval = 0
    return '%.5f' % (round(inval*10000)/10000)


if __name__ == '__main__':
    if sys.argv.__len__() != 3:
        print "Invalid arguments"
        sys.exit(2)
        
    LDRAWPATH = sys.argv[1]    # mjh, don't change this index
    MODELPATH = sys.argv[2]    # mjh, don't change this index
    
    if not os.path.isdir(LDRAWPATH):
        print NOTFOUND_MSG % LDRAWPATH
        sys.exit(2)
        
    if not os.path.isfile(MODELPATH):
        print NOTFOUND_MSG % MODELPATH
        sys.exit(2)
    
    try:
        with open(MODELPATH ,"r") as f:
            for line in f:
                CHKLST_INFILE.append(line)
                CHKLST_INCHEK.append(False)
            f.close()
    except:
        CHKLST_INFILE = []
        CHKLST_INCHEK = []
        print INVALIDACCESS_MSG % MODELPATH
        sys.exit(2)
    
    else:
        print __appname__ ,__version__ ,"processing" ,MODELPATH
        
        i = ii = iii = frg = 0
        x1 = y1 = z1 = a1 = c1 = g1 = i1 = x2 = y2 = z2 = x3 = y3 = z3 = 0.0
        s = ldline = fil = ""
        SkipThis = False
        StrLstCover = []
        StrListInfil = []
        
        # cmdFittingsClick STEP 1: Compile a list of locations (20x20LDU)
        # Tops and Bottoms that are hiding (=covering) details from next part
        # Save the list in StrListCover

        for i in range(CHKLST_INFILE.__len__()):
            ldline = CHKLST_INFILE[i]
            if ldLineType(ldline) <> 1: continue
            
            frg = int(ldExtractFromLine(ldline, 2))
            if (frg>31) and (frg<48): continue
            
            if float(ldExtractFromLine(ldline, 7)) <> 0.0 : continue
            if float(ldExtractFromLine(ldline, 9)) <> 0.0 : continue
            if float(ldExtractFromLine(ldline, 10)) <> 1.0 : continue
            if float(ldExtractFromLine(ldline, 11)) <> 0.0 : continue
            if float(ldExtractFromLine(ldline, 13)) <> 0.0 : continue
            
            fil = ldExtractFromLine(ldline ,15)
            if len(fil)<5: continue # just to be foolproof...
            
            #  2010-03-20 also check if already boxed parts cover positions
            #  by removing B\, B\T, or B\B from examined file reference
            
            if fil[0:3].upper() == "B\\T":
                fil = fil[3:]
            elif fil[0:3].upper() == "B\\B":
                fil = fil[3:]
            elif fil[0:2].upper() == "B\\":
                fil = fil[2:]
            
            if len(fil)<5 : continue # just to be foolproof...
            
            fil = fil[0:(len(fil)-4)]
            
            fil = os.path.join(LDRAWPATH ,'Parts' ,'B' ,fil + '.nfo')
            
            print "Searching for" ,fil
            if not os.path.exists(fil) : continue
            
            x1 = float(ldExtractFromLine(ldline ,3))
            y1 = float(ldExtractFromLine(ldline ,4))
            z1 = float(ldExtractFromLine(ldline ,5))
            a1 = float(ldExtractFromLine(ldline ,6))
            c1 = float(ldExtractFromLine(ldline ,8))
            g1 = float(ldExtractFromLine(ldline ,12))
            i1 = float(ldExtractFromLine(ldline ,14))
            
            NFOCONTENT = []
            try:
                with open(fil ,"r") as f:
                    for line in f:
                        NFOCONTENT.append(line)
                    f.close()
            except:
                NFOCONTENT = []
                print INVALIDACCESS_MSG % fil
            
            StrListInfil = []
            StrListInfil.extend(NFOCONTENT)
            for ii in range(StrListInfil.__len__()):
                ldline = StrListInfil[ii]
                s = ldExtractFromLine(ldline, 1)
                x2 = float(ldExtractFromLine(ldline, 2))
                y2 = float(ldExtractFromLine(ldline, 3))
                z2 = float(ldExtractFromLine(ldline, 4))
                if s=='Top' or s=='Stud' : s = 'T '
                elif s=='Bottom' : s = 'B '
                x3 = x1 + x2*a1 + z2*c1
                y3 = y1 + y2
                z3 = z1 + x2*g1 + z2*i1
                s = s + FloatToLDraw(x3) + ' '
                s = s + FloatToLDraw(y3) + ' '
                s = s + FloatToLDraw(z3)
                StrLstCover.append(s)
                
        
        #  END of cmdFittingsClick STEP 1
        #  The model file in chklstInfile has been scanned for locations
        #  meeting all the given criterias
        #  For example:
        #  This following line meets the criteria:
        #  1 15  240 -48 160  1 0 0  0 1 0  0 0 1  3005.dat
        #  The two lines from the file Parts\B\3005.nfo is used:
        #  Stud 0 0 0
        #  Bottom 0 24 0
        #  The output stored in StrListCover is the following two lines:
        #  T 240 -48 160
        #  B 240 -24 160
        
        
        #  cmdFittingsClick STEP 2: Replace all parts that top and/or bottom details can be removed from
        
        for iiii in range(0, 3):
            for i in range(CHKLST_INFILE.__len__()) :
                CHKLST_INCHEK[i] = False
                ldline = CHKLST_INFILE[i]
                if ldLineType(ldline) <> 1 : continue
                frg = int(ldExtractFromLine(ldline, 2))
                if (frg>31) and (frg<48) : continue
                if float(ldExtractFromLine(ldline, 7)) <> 0.0 : continue
                if float(ldExtractFromLine(ldline, 9)) <> 0.0 : continue
                if float(ldExtractFromLine(ldline, 10)) <> 1.0 : continue
                if float(ldExtractFromLine(ldline, 11)) <> 0.0 : continue
                if float(ldExtractFromLine(ldline, 13)) <> 0.0 : continue
                
                fil = ldExtractFromLine(ldline, 15)
                if len(fil)<5 : continue
                if fil[0:3].upper() == "B\\T":
                    fil = fil[3:]
                elif fil[0:3].upper() == "B\\B":
                    fil = fil[3:]
                elif fil[0:2].upper() == "B\\":
                    fil = fil[2:]
                if len(fil)<5 : continue
                fil = fil[0:(len(fil)-4)]
                fil = os.path.join(LDRAWPATH ,'Parts' ,'B' ,fil + '.dat')
                if not os.path.exists(fil) : continue
                fil = fil[0:(len(fil)-4)]
                fil = fil + '.nfo'
                if not os.path.exists(fil) : continue
                
                x1 = float(ldExtractFromLine(ldline, 3))
                y1 = float(ldExtractFromLine(ldline, 4))
                z1 = float(ldExtractFromLine(ldline, 5))
                a1 = float(ldExtractFromLine(ldline, 6))
                c1 = float(ldExtractFromLine(ldline, 8))
                g1 = float(ldExtractFromLine(ldline, 12))
                i1 = float(ldExtractFromLine(ldline, 14))
                
                NFOCONTENT = []
                try:
                    with open(fil ,"r") as f:
                        for line in f:
                            NFOCONTENT.append(line)
                        f.close()
                except:
                    NFOCONTENT = []
                    print INVALIDACCESS_MSG % fil
                
                StrListInfil = []
                StrListInfil.extend(NFOCONTENT)
                SkipThis = False
                for ii in range (StrListInfil.__len__()) :
                    ldline = StrListInfil[ii]
                    
                    s = ldExtractFromLine(ldline, 1)
                    if iiii == 0:
                        if s =='Top' : continue
                        #elif s == 'Stud': continue
                        elif s =='Stud' : s = 'B '      # Scan for matching B
                        #elif s == 'Bottom': continue
                        elif s =='Bottom' : s = 'T '    # Scan for matching T
                    elif iiii == 1:
                        if s =='Top' : continue
                        #elif s == 'Stud': continue
                        elif s =='Stud' : s = 'B '      # Scan for matching B
                        elif s =='Bottom' : continue
                        #elif s == 'Bottom': s = 'T '    # Scan for matching T
                    elif iiii == 2:
                        if s=='Top' : continue
                        elif s=='Stud' : continue
                        #elif s=='Stud' : s = 'B '    # Scan for matching B
                        #elif s=='Bottom' : continue
                        if s=='Bottom' : s = 'T '  # Scan for matching T
                    
                    x2 = float(ldExtractFromLine(ldline, 2))
                    y2 = float(ldExtractFromLine(ldline, 3))
                    z2 = float(ldExtractFromLine(ldline, 4))
                    x3 = x1 + x2*a1 + z2*c1
                    y3 = y1 + y2
                    z3 = z1 + x2*g1 + z2*i1
                    s = s + FloatToLDraw(x3) + ' '
                    s = s + FloatToLDraw(y3) + ' '
                    s = s + FloatToLDraw(z3)
                    SkipThis = True
                    for iii in range (StrLstCover.__len__()) :
                        if s==StrLstCover[iii] :
                            SkipThis = False
                            break
                    if SkipThis==True : break
                if SkipThis==True : continue
                CHKLST_INCHEK[i] = True
            
            replacedCount = 0
            for i in range(CHKLST_INFILE.__len__()):
                ldline = CHKLST_INFILE[i]
                newPrefix = STR_PREFIXES[iiii]
                oldPrefix = ''
                #print ldline, CHKLST_INCHEK[i], newPrefix
                if CHKLST_INCHEK[i]==False : continue
                if ldLineType(ldline) <> 1 : continue
                fil = ldExtractFromLine(ldline, 15)
                if fil[0:3].upper() == 'B\\T':
                    fil = fil[3:]
                    oldPrefix = 'B\\T'
                elif fil[0:3].upper() == 'B\\B':
                    fil = fil[3:]
                    oldPrefix = 'B\\B'
                elif fil[0:2].upper() == 'B\\':
                    fil = fil[2:]
                    oldPrefix = 'B\\'
                if oldPrefix == 'B\\':
                    fil = 'B\\' + fil
                else:
                    fil = newPrefix + fil
                fname = os.path.join(LDRAWPATH ,'Parts' ,fil)
                if not os.path.exists(fname) : continue
                ldline = ldLineUpdate(ldline, 15, fil)
                CHKLST_INFILE[i] = ldline
                replacedCount += 1
                global REPLACEDTOTAL_COUNT
                REPLACEDTOTAL_COUNT += 1
            if replacedCount>0 :
                CHKLST_INFILE.append("0 // Boxed {0} parts ({1})".format(replacedCount ,newPrefix))
                CHKLST_INCHEK.append(False)
        
        #  END of cmdFittingsClick STEP 2
        
        print
        print "Boxed %d parts" % REPLACEDTOTAL_COUNT
        
        for i in range(CHKLST_INFILE.__len__()) :
            CHKLST_INCHEK[i] = False
        
        if REPLACEDTOTAL_COUNT>0 :       
            
            #  0 !LDOXER LEVEL info should also be automatically updated!
            CHKLST_INFILE.append("0 // Boxed Total {0} parts by {1} v{2}".format(REPLACEDTOTAL_COUNT ,__appname__ ,__version__))
            CHKLST_INFILE.append("0")
            CHKLST_INCHEK.append(False)
            CHKLST_INCHEK.append(False)
            
            try:
                dirname = os.path.dirname(MODELPATH)
                basename = "boxed_" + os.path.basename(MODELPATH)
                with open(os.path.join(dirname,basename) ,"wb") as f:
                    for line in CHKLST_INFILE:
                        line = line.strip('\r').strip('\n')
                        f.write(line + "\r\n")
                    f.close()
            except Exception, ex:
                print ex.message
            else:
                print "Saved {0} in {1}".format(basename ,dirname)     
