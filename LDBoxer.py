'''
Created on 16 mar 2017
Updated on 27 may 2021
@author: Tore Eriksson <tore.eson@gmail.com>
@author: Jeremy Czajkowski
@author: Michael Horvath
@license: GNU General Public License version 3
@version: 2018i
@note: A utility to help you replace LDraw parts with no visible studs or tubes with boxes. 
       Saves rendering time and CPU power.
       Note that this script is volatile! If your model already contains boxed parts, they will be deleted!
       If you add a third "-v" command-line option, the program will display more verbose output useful for debugging.
       I recommend using PyPy to run the script instead of CPython. The speed is much much improved!
       I recommend not using this script on MPD or XMPD models for the time being, until the script properly handles such file types.
       Unless you flatten/inline the MPD or XMPD files first, in which case it is okay but still not ideal.
'''

import os
import sys
import datetime
import time
from macpath import dirname

__appname__ = "LDBoxer"
__version__ = "2018i"

NOTFOUND_MSG = "FileNotFoundError: [Errno 2] No such file or directory: '%s'"
INVALIDACCESS_MSG = "ImportError: Invalid access to %s."

CHKLST_INFILE = []
CHKLST_INTYPE = []
STR_PREFIXES = ['none', 'b\\t', 'b\\b', 'b\\a']

LDRAWPATH = MODELPATH = ''
VERBOSE = False


def ldLineType(ldline):
    result = -1
    s = ldline.strip()
    if len(s)>0:
        if s[0] == '0': result = 0
        elif s[0] == '1': result = 1
        elif s[0] == '2': result = 2
        elif s[0] == '3': result = 3
        elif s[0] == '4': result = 4
        elif s[0] == '5': result = 5
    return result


def ldLineUpdate(ldline, ItemNr, NewVal):
    color1 = ldExtractFromLine(ldline, 2)
    x1 = ldExtractFromLine(ldline, 3)
    y1 = ldExtractFromLine(ldline, 4)
    z1 = ldExtractFromLine(ldline, 5)
    a1 = ldExtractFromLine(ldline, 6)
    b1 = ldExtractFromLine(ldline, 7)
    c1 = ldExtractFromLine(ldline, 8)
    d1 = ldExtractFromLine(ldline, 9)
    e1 = ldExtractFromLine(ldline, 10)
    f1 = ldExtractFromLine(ldline, 11)
    g1 = ldExtractFromLine(ldline, 12)
    h1 = ldExtractFromLine(ldline, 13)
    i1 = ldExtractFromLine(ldline, 14)
    fil = ldExtractFromLine(ldline, 15)
    
    if ItemNr == 2:
        color1 = NewVal
    elif ItemNr == 3:
        x1 = NewVal
    elif ItemNr == 4:
        y1 = NewVal
    elif ItemNr == 5:
        z1 = NewVal
    elif ItemNr == 6:
        a1 = NewVal
    elif ItemNr == 7:
        b1 = NewVal
    elif ItemNr == 8:
        c1 = NewVal
    elif ItemNr == 9:
        d1 = NewVal
    elif ItemNr == 10:
        e1 = NewVal
    elif ItemNr == 11:
        f1 = NewVal
    elif ItemNr == 12:
        g1 = NewVal
    elif ItemNr == 13:
        h1 = NewVal
    elif ItemNr == 14:
        i1 = NewVal
    elif ItemNr == 15:
        fil = NewVal
    
    s = '1 ' + color1 + ' '
    s = s + ldFloatToLDraw(float(x1))+ ' '
    s = s + ldFloatToLDraw(float(y1))+ ' '
    s = s + ldFloatToLDraw(float(z1))+ ' '
    s = s + ldFloatToLDraw(float(a1))+ ' '
    s = s + ldFloatToLDraw(float(b1))+ ' '
    s = s + ldFloatToLDraw(float(c1))+ ' '
    s = s + ldFloatToLDraw(float(d1))+ ' '
    s = s + ldFloatToLDraw(float(e1))+ ' '
    s = s + ldFloatToLDraw(float(f1))+ ' '
    s = s + ldFloatToLDraw(float(g1))+ ' '
    s = s + ldFloatToLDraw(float(h1))+ ' '
    s = s + ldFloatToLDraw(float(i1))+ ' '
    s = s + fil
    return s


def ldExtractFromLine(ldline, post):
    a = ldline.split()
    if post <= len(a):
        return a[post-1]
    return '' 


def ldFloatToLDraw(inval):
#    if (inval > -0.0001) and (inval < 0.0001): inval = 0
#    return '%.5f' % (round(inval*10000)/10000)
    return ('%s' % inval).rstrip('0').rstrip('.')


if __name__ == '__main__':
    if sys.argv.__len__() < 3 or sys.argv.__len__() > 4:
        print("Invalid arguments")
        sys.exit(2)
    elif sys.argv.__len__() == 4:
        if sys.argv[3] == "-v":
            VERBOSE = True
        else:
            print("Invalid arguments")
            sys.exit(2)

    LDRAWPATH = sys.argv[1]
    MODELPATH = sys.argv[2]
    
    if not os.path.isdir(LDRAWPATH):
        print(NOTFOUND_MSG % LDRAWPATH)
        sys.exit(2)
        
    if not os.path.isfile(MODELPATH):
        print(NOTFOUND_MSG % MODELPATH)
        sys.exit(2)
    
    try:
        with open(MODELPATH, "r") as f:
            for line in f:
                CHKLST_INFILE.append(line)
                CHKLST_INTYPE.append(0)
            f.close()
    except:
        CHKLST_INFILE = []
        CHKLST_INTYPE = []
        print(INVALIDACCESS_MSG % MODELPATH)
        sys.exit(2)
    
    else:
        print(__appname__, __version__, "processing", MODELPATH)
        
        i = ii = iii = frg = 0
        x1 = y1 = z1 = a1 = c1 = g1 = i1 = x2 = y2 = z2 = x3 = y3 = z3 = 0.0
        s = ldline = fil = ""
        SkipThis = False
        StrLstCover = []
        StrListInfil = []
        
        # STEP 1/5: Compile a list of locations (20x20LDU)
        # Tops and Bottoms that are hiding (=covering) details from next part
        # Save the list in StrListCover
        
        start_time = time.time()
        currentDT = datetime.datetime.now().strftime("%b %d, %Y %H:%M:%S")
        print("")
        print("Processing step 1/5. Current date and time: " + str(currentDT) + ".")
        imax = CHKLST_INFILE.__len__()
        for i in range(imax):
            ldline = CHKLST_INFILE[i]
            CHKLST_INTYPE[i] = 0
            if ldLineType(ldline) != 1: continue
            
            frg = int(ldExtractFromLine(ldline, 2))
            if (frg > 31) and (frg < 48): continue
            
            if float(ldExtractFromLine(ldline, 7)) != 0.0: continue
            if float(ldExtractFromLine(ldline, 9)) != 0.0: continue
            if float(ldExtractFromLine(ldline, 10)) != 1.0: continue
            if float(ldExtractFromLine(ldline, 11)) != 0.0: continue
            if float(ldExtractFromLine(ldline, 13)) != 0.0: continue
            
            fil = ldExtractFromLine(ldline, 15)
            if len(fil) < 5: continue # just to be foolproof...
            
            #  2010-03-20 also check if already boxed parts cover positions
            #  by removing B\, B\T, or B\B from examined file reference
            
            if fil[0:3].upper() == STR_PREFIXES[1]:
                fil = fil[3:]
            elif fil[0:3].upper() == STR_PREFIXES[2]:
                fil = fil[3:]
            elif fil[0:3].upper() == STR_PREFIXES[3]:
                fil = fil[3:]
            
            ldline = ldLineUpdate(ldline, 15, fil)
            CHKLST_INFILE[i] = ldline
            
            if VERBOSE == True:
                elapsed_time = time.time() - start_time
                currentDT = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                print("  Step 1/5. Line " + str(i) + "/" + str(imax) + ". File \"" + fil + "\". Time " + str(currentDT) + ".")
            
            if len(fil) < 5: continue # just to be foolproof...
            fil = fil[0:(len(fil)-4)]
            filnfo = os.path.join(LDRAWPATH, 'parts', 'b', fil + '.nfo')
            if not os.path.exists(filnfo): continue
            
            x1 = float(ldExtractFromLine(ldline, 3))
            y1 = float(ldExtractFromLine(ldline, 4))
            z1 = float(ldExtractFromLine(ldline, 5))
            a1 = float(ldExtractFromLine(ldline, 6))
            c1 = float(ldExtractFromLine(ldline, 8))
            g1 = float(ldExtractFromLine(ldline, 12))
            i1 = float(ldExtractFromLine(ldline, 14))
            
            NFOCONTENT = []
            try:
                with open(filnfo, "r") as f:
                    for line in f:
                        NFOCONTENT.append(line)
                    f.close()
            except:
                NFOCONTENT = []
                print(INVALIDACCESS_MSG % filnfo)
            
            StrListInfil = []
            StrListInfil.extend(NFOCONTENT)
            iimax = StrListInfil.__len__()
            for ii in range(iimax):
                ldline = StrListInfil[ii]
                s = ldExtractFromLine(ldline, 1)
                if s == 'Top' or s=='Stud': s = 'T '
                elif s == 'Bottom': s = 'B '
                x2 = float(ldExtractFromLine(ldline, 2))
                y2 = float(ldExtractFromLine(ldline, 3))
                z2 = float(ldExtractFromLine(ldline, 4))
                x3 = x1 + x2 * a1 + z2 * c1
                y3 = y1 + y2
                z3 = z1 + x2 * g1 + z2 * i1
                s = s + ldFloatToLDraw(x3) + ' '
                s = s + ldFloatToLDraw(y3) + ' '
                s = s + ldFloatToLDraw(z3)
                StrLstCover.append(s)
                
        
        #  END of STEP 1/5
        
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
        
        
        #  STEP 2/5 & 3/5: Determine which parts the top and/or bottom details can be removed from
        
        for iiii in range(1, 3):
            print("Processing step " + str(1+iiii) + "/5. Pass " + str(iiii) + ".")
            imax = CHKLST_INFILE.__len__()
            for i in range(imax):
                ldline = CHKLST_INFILE[i]
                if ldLineType(ldline) != 1: continue
                frg = int(ldExtractFromLine(ldline, 2))
                if (frg > 31) and (frg < 48): continue
                if float(ldExtractFromLine(ldline, 7)) != 0.0: continue
                if float(ldExtractFromLine(ldline, 9)) != 0.0: continue
                if float(ldExtractFromLine(ldline, 10)) != 1.0: continue
                if float(ldExtractFromLine(ldline, 11)) != 0.0: continue
                if float(ldExtractFromLine(ldline, 13)) != 0.0: continue
                
                fil = ldExtractFromLine(ldline, 15)
                if VERBOSE == True:
                    elapsed_time = time.time() - start_time
                    currentDT = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                    print("  Step " + str(1+iiii) + "/5. Line " + str(i) + "/" + str(imax) + ". File \"" + fil + "\". Time " + str(currentDT) + ".")
                
                if len(fil) < 5: continue
                fil = fil[0:(len(fil)-4)]
                filnfo = os.path.join(LDRAWPATH, 'parts', 'b', fil + '.nfo')
                if not os.path.exists(filnfo): continue
                
                x1 = float(ldExtractFromLine(ldline, 3))
                y1 = float(ldExtractFromLine(ldline, 4))
                z1 = float(ldExtractFromLine(ldline, 5))
                a1 = float(ldExtractFromLine(ldline, 6))
                c1 = float(ldExtractFromLine(ldline, 8))
                g1 = float(ldExtractFromLine(ldline, 12))
                i1 = float(ldExtractFromLine(ldline, 14))
                
                NFOCONTENT = []
                try:
                    with open(filnfo, "r") as f:
                        for line in f:
                            NFOCONTENT.append(line)
                        f.close()
                except:
                    NFOCONTENT = []
                    print(INVALIDACCESS_MSG % filnfo)
                
                StrListInfil = []
                StrListInfil.extend(NFOCONTENT)
                SkipThis = False
                iimax = StrListInfil.__len__()
                for ii in range(iimax):
                    ldline = StrListInfil[ii]
                    
                    s = ldExtractFromLine(ldline, 1)
                    if iiii == 1:
                        if s =='Top': continue
                        elif s =='Bottom': continue
                        elif s =='Stud': s = 'B '      # Scan for matching B
                    elif iiii == 2:
                        if s == 'Top': continue
                        elif s == 'Stud': continue
                        elif s == 'Bottom': s = 'T '   # Scan for matching T
                    
                    x2 = float(ldExtractFromLine(ldline, 2))
                    y2 = float(ldExtractFromLine(ldline, 3))
                    z2 = float(ldExtractFromLine(ldline, 4))
                    x3 = x1 + x2 * a1 + z2 * c1
                    y3 = y1 + y2
                    z3 = z1 + x2 * g1 + z2 * i1
                    s = s + ldFloatToLDraw(x3) + ' '
                    s = s + ldFloatToLDraw(y3) + ' '
                    s = s + ldFloatToLDraw(z3)
                    
                    SkipThis = True
                    for iii in range(StrLstCover.__len__()):
                        if s == StrLstCover[iii]:
                            SkipThis = False
                            break
                    if SkipThis == True: break
                if SkipThis == True: continue
                if iiii == 1:
                    CHKLST_INTYPE[i] = 1
                elif iiii == 2:
                    if CHKLST_INTYPE[i] == 1:
                        CHKLST_INTYPE[i] = 3
                    else:
                        CHKLST_INTYPE[i] = 2
        
        #  END of STEP 2/5 & 3/5
        
        #  STEP 4/5: Generate output
        
        print("Processing step 4/5. Generating output.")
        replacedCount1 = 0
        replacedCount2 = 0
        replacedCount3 = 0
        replacedCountTotal = 0
        partCountTotal = 0
        imax = CHKLST_INFILE.__len__()
        for i in range(imax):
            ldline = CHKLST_INFILE[i]
            ldtype = CHKLST_INTYPE[i]
            if ldLineType(ldline) != 1: continue
            partCountTotal += 1
            if ldtype == 0: continue
            elif ldtype == 1:
                replacedCount1 += 1
            elif ldtype == 2:
                replacedCount2 += 1
            elif ldtype == 3:
                replacedCount3 += 1
            replacedCountTotal += 1
            newPrefix = STR_PREFIXES[ldtype]
            
            # Super verbose text for debugging.
            #print(ldline, ldtype, newPrefix)
            
            fil = newPrefix + ldExtractFromLine(ldline, 15)
            if VERBOSE == True:
                elapsed_time = time.time() - start_time
                currentDT = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                print("  Step 4/5. Line " + str(i) + "/" + str(imax) + ". File \"" + fil + "\". Time " + str(currentDT) + ".")

            fname = os.path.join(LDRAWPATH, 'Parts', fil)
            if not os.path.exists(fname): continue
            ldline = ldLineUpdate(ldline, 15, fil)
            CHKLST_INFILE[i] = ldline
        
        #  END of STEP 4/5
        
        #  STEP 5/5: Finalize and write output.
        
        print("Processing step 5/5. Finalizing and writing output.")
        
        elapsed_time = time.time() - start_time
        currentDT = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        boxPercent = round(float(replacedCountTotal)/float(partCountTotal) * 100, 1)
        
        endMessage1 = "Boxed {0} parts ({1}).".format(replacedCount1, STR_PREFIXES[1])
        endMessage2 = "Boxed {0} parts ({1}).".format(replacedCount2, STR_PREFIXES[2])
        endMessage3 = "Boxed {0} parts ({1}).".format(replacedCount3, STR_PREFIXES[3])
        endMessage4 = "Boxed Total {0}/{1} ({2}%) parts by {3} v{4}.".format(replacedCountTotal, partCountTotal, boxPercent, __appname__, __version__)
        endMessage5 = "Elapsed time: " + str(currentDT) + "."

        CHKLST_INFILE.append("0 // " + endMessage1)
        CHKLST_INFILE.append("0 // " + endMessage2)
        CHKLST_INFILE.append("0 // " + endMessage3)
        CHKLST_INFILE.append("0 // " + endMessage4)
        CHKLST_INFILE.append("0 // " + endMessage5)
        CHKLST_INFILE.append("0")
        CHKLST_INTYPE.append(0)
        CHKLST_INTYPE.append(0)
        CHKLST_INTYPE.append(0)
        CHKLST_INTYPE.append(0)
        CHKLST_INTYPE.append(0)
        CHKLST_INTYPE.append(0)
        print("  " + endMessage1)
        print("  " + endMessage2)
        print("  " + endMessage3)
        print("  " + endMessage4)
        print("  " + endMessage5)
        
        if replacedCountTotal > 0:
            try:
                dirname = os.path.dirname(MODELPATH)
                basename = "boxed_" + os.path.basename(MODELPATH)
                parentpath = os.path.abspath(os.path.join(MODELPATH, os.pardir))
                with open(os.path.join(dirname,basename), "w") as f:
                    for line in CHKLST_INFILE:
                        output = line.strip("\n").strip("\r") + "\n"
                        f.write(output)
                    f.close()
            except Exception as ex:
                print(ex.message)
            else:
                print("  Saved \"{0}\" in \"{1}\".".format(basename, parentpath))
