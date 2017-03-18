'''
Created on 16 mar 2017

@author: Jeremy Czajkowski
@author: Tore Eriksson <tore.eriksson@mbox325.swipnet.se>
@license: GNU General Public License version 3
@version: 2017a
@note: A utility to help you replace LDraw parts with no visible studs or tubes with boxes. 
       Saves rendering time and CPU power.
'''

import os
import sys

__appname__ = "LDBoxer"
__version__ = "2017a"

NOTFOUND_MSG = "FileNotFoundError: [Errno 2] No such file or directory: '%s'"
INVALIDACCESS_MSG = "ImportError: Invalid access to %s."

MODELCONTENT = CHKLST_INFILE = []
REPLACEDTOTAL_COUNT = 0

LDRAWPATH = MODELPATH = ""


def isBox(fil):
    return True if fil[1:2].upper() == "B\\" else False


def ldLineType(ldline):
    result = -1;
    s = ldline.strip()
    if len(s)>0 :
        if s[1]=='0' : result = 0
        if s[1]=='1' : result = 1
        if s[1]=='2' : result = 2
        if s[1]=='3' : result = 3
        if s[1]=='4' : result = 4
        if s[1]=='5' : result = 5
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
    s = s + FloatToLDraw(i1)+ ' ' + fil
    return s

def ldExtractFromLine (ldline, post):

    t = []
    i = 0
    
    s = ldline.strip()
    iT = 1;
    while s <> '':
        s = s.strip() + ' '
        i = 1
        while s[i] <> ' ': i += 1
#         t[iT] = Copy(s, 1, i-1)
#         function Copy(const S: string; From: integer = 1; Count: integer = MaxInt): string;
        t[iT] = s[1:(i-1)+1]
        iT += 1
        s = s[i:len(s)+i]
    
    result = ''
    if post < iT: result = t[post]
    return result
    

def FloatToLDraw(inval):
    if (inval > -0.0001) and (inval < 0.0001): inval = 0
    return '%.5f' % (round(inval*10000)/10000)    


def cmdReplace():
    replacedCount = 0
    for i in range(CHKLST_INFILE.__len__()):
        ldline = CHKLST_INFILE[i]
        if ldLineType(ldline) == 1 :
            fil = ldExtractFromLine(ldline, 15)
            if isBox(fil) == False : fil = strPrefix + fil
            fname = os.path.join(LDRAWPATH ,'Parts' ,fil)
            if os.path.exists(fname):
                ldline == ldLineUpdate(ldline, 15, fil)
                CHKLST_INFILE[i] == ldline
                replacedCount += 1;
                REPLACEDTOTAL_COUNT += 1;
    if replacedCount>0 :
        CHKLST_INFILE.append("0 // Boxed {0} parts ({1}).".format(replacedCount ,strPrefix))

if __name__ == '__main__':
    if sys.argv.__len__() != 3:
        print "Invalid arguments"
        sys.exit(2)
        
    LDRAWPATH = sys.argv[1]
    MODELPATH = sys.argv[2]
    
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
                MODELCONTENT.append(line)
            f.close()
    except:
        CHKLST_INFILE = []
        print INVALIDACCESS_MSG % MODELPATH
    else:
        print __appname__ ,__version__ ,"processing" ,MODELPATH
        
        i = ii = iii = frg = 0
        x1 = y1 = z1 = a1 = c1 = g1 = i1 = x2 = y2 = z2 = x3 = y3 = z3 = 0.0
        s = ldline = fil = ""
        SkipThis = False
        StrLstCover = StrListInfil = []
              
        """
         cmdFittingsClick STEP 1: Compile a list of locations (20x20LDU)
         Tops and Bottoms that are hiding (=covering) details from next part
         Save the list in StrListCover        
        """
        for i in range(CHKLST_INFILE.__len__()):
            ldline = CHKLST_INFILE[i]
            if ldLineType(ldline) <> 1: continue
            
            frg = int(ldExtractFromLine(ldline, 2));
            if (frg>31) and (frg<48): continue
            
            if ldExtractFromLine(ldline, 7) <> '0' : continue
            if ldExtractFromLine(ldline, 9) <> '0' : continue
            if ldExtractFromLine(ldline, 10) <> '1' : continue
            if ldExtractFromLine(ldline, 11) <> '0' : continue
            if ldExtractFromLine(ldline, 13) <> '0' : continue
            
            fil = ldExtractFromLine(ldline ,15);
            if len(fil)<5: continue # just to be foolproof...
    
            """
             2010-03-20 also check if already boxed parts cover positions
             by removing B\, B\t, or B\B from examined file reference
            """
            if fil[1:3].upper() == "B\\T":
                fil = fil[4:(len(fil)-3)+4]
            
            if s[1:3].upper() == "B\\B":
                fil = fil[4:(len(fil)-3)+4]
            
            if fil[1:2].upper() == "B\\":
                fil = fil[3:(len(fil)-2)+3]
            
            if len(fil)<5 : 
                continue    
            
            fil = fil[1:(len(fil)-4)+1]
            
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
            
            StrListInfil = []
            StrListInfil.extend(MODELCONTENT)
            for ii in range(StrListInfil.__len__()):
                ldline = StrListInfil[ii]
                s = ldExtractFromLine(ldline, 1)
                x2 = float(ldExtractFromLine(ldline, 2))
                y2 = float(ldExtractFromLine(ldline, 3))
                z2 = float(ldExtractFromLine(ldline, 4))
                
                if s=='Top' or s=='Stud' : s = 'T '
                if s=='Bottom' : s = 'B '

                x3 = x1 + x2*a1 + z2*c1
                y3 = y1 + y2
                z3 = z1 + x2*g1 + z2*i1
                s = s + FloatToLDraw(x3) + ' '
                s = s + FloatToLDraw(y3) + ' '
                s = s + FloatToLDraw(z3)
                StrLstCover.append(s) 
                
        """
         END of cmdFittingsClick STEP 1
         The model file in chklstInfile has been scanned for locations
          meeting all the given criterias
         For example:
         This following line meets the criteria:
         1 15  240 -48 160  1 0 0  0 1 0  0 0 1  3005.dat
         The two lines from the file Parts\B\3005.nfo is used:
         Stud 0 0 0
         Bottom 0 24 0
         The output stored in StrListCover is the following two lines:
         T 240 -48 160
         B 240 -24 160
        """
        
        
        """
         cmdFittingsClick STEP 2: Replace all parts that can be fully boxed
          Checkbox all parts that has all stud and bottom locations covered
          according to StrListCover
        """
        for i in range(CHKLST_INFILE.__len__()):
            ldline = CHKLST_INFILE[i]
            if ldLineType(ldline) <> 1 : continue;
            frg = int(ldExtractFromLine(ldline, 2))
            if (frg>31) and (frg<48) : continue
            if ldExtractFromLine(ldline, 7) <> '0' : continue
            if ldExtractFromLine(ldline, 9) <> '0' : continue
            if ldExtractFromLine(ldline, 10) <> '1' : continue
            if ldExtractFromLine(ldline, 11) <> '0' : continue
            if ldExtractFromLine(ldline, 13) <> '0' : continue
            fil = ldExtractFromLine(ldline, 15)
            if len(fil)<5 : continue
            
            fil = fil[1:(len(fil)-4)+1]
            
            fil = os.path.join(LDRAWPATH ,'Parts' ,'B' ,fil + '.dat')
            if not os.path.exists(fil):  continue
            
            fil = fil[1:(len(fil)-4)+1]
            fil = fil + '.nfo';
            if not os.path.exists(fil): continue
            x1 = float(ldExtractFromLine(ldline, 3))
            y1 = float(ldExtractFromLine(ldline, 4))
            z1 = float(ldExtractFromLine(ldline, 5))
            a1 = float(ldExtractFromLine(ldline, 6))
            c1 = float(ldExtractFromLine(ldline, 8))
            g1 = float(ldExtractFromLine(ldline, 12))
            i1 = float(ldExtractFromLine(ldline, 14))
            
            StrListInfil = []
            StrListInfil.extend(fil)
            for ii in range(StrListInfil.__len__()):
                ldline = StrListInfil[ii]
                s = ldExtractFromLine(ldline, 1)
                x2 = float(ldExtractFromLine(ldline, 2))
                y2 = float(ldExtractFromLine(ldline, 3))
                z2 = float(ldExtractFromLine(ldline, 4))
                if s =='Top' : continue
                if s =='Stud' : s = 'B '      # Scan for matching B
                if s =='Bottom' : s = 'T '    # Scan for matching T
                x3 = x1 + x2*a1 + z2*c1
                y3 = y1 + y2
                z3 = z1 + x2*g1 + z2*i1
                s = s + FloatToLDraw(x3) + ' '
                s = s + FloatToLDraw(y3) + ' '
                s = s + FloatToLDraw(z3)
                SkipThis == True
                for iii in range(StrLstCover.__len__()):
                    if s==StrLstCover[iii] : SkipThis = False
                if SkipThis : break
            if SkipThis : continue
    
        strPrefix = "B\\"
        cmdReplace()
        """
          END of cmdFittingsClick STEP 2
        """    
      
      
        """
          cmdFittingsClick STEP 3: Replace all parts that studs can be removed from
          (STEPs 3 & 4 should be easily baked into STEP 2...) 
        """
        for i in range(CHKLST_INFILE.__len__()):
            ldline = CHKLST_INFILE[i]
            if ldLineType(ldline) <> 1: continue;
            frg = int(ldExtractFromLine(ldline, 2));
            if (frg>31) and (frg<48) : 
                continue;
            if ldExtractFromLine(ldline, 7) <> '0' : continue
            if ldExtractFromLine(ldline, 9) <> '0' : continue
            if ldExtractFromLine(ldline, 10) <> '1' : continue
            if ldExtractFromLine(ldline, 11) <> '0' : continue
            if ldExtractFromLine(ldline, 13) <> '0' : continue
            fil = ldExtractFromLine(ldline, 15);
            if len(fil)<5 : continue
            fil = fil[1:(len(fil)-4)+1]
            fil = os.path.join(LDRAWPATH ,'Parts' ,'B' ,fil + '.dat')
            if not os.path.exists(fil) : 
                continue
            fil = fil[1:(len(fil)-4)+1]
            fil = fil + '.nfo'
            if not os.path.exists(fil) : 
                continue
            x1 = float(ldExtractFromLine(ldline, 3))
            y1 = float(ldExtractFromLine(ldline, 4))
            z1 = float(ldExtractFromLine(ldline, 5))
            a1 = float(ldExtractFromLine(ldline, 6))
            c1 = float(ldExtractFromLine(ldline, 8))
            g1 = float(ldExtractFromLine(ldline, 12))
            i1 = float(ldExtractFromLine(ldline, 14))
            StrListInfil = []
            StrListInfil.extend(fil)
            SkipThis = False
            for ii in range (StrListInfil.__len__()) :
                ldline = StrListInfil[ii]
                s = ldExtractFromLine(ldline, 1)
                x2 = float(ldExtractFromLine(ldline, 2))
                y2 = float(ldExtractFromLine(ldline, 3))
                z2 = float(ldExtractFromLine(ldline, 4))
                if s =='Top' : continue
                if s =='Stud' : s = 'B '      # Scan for matching B
                if s =='Bottom' : continue
                x3 = x1 + x2*a1 + z2*c1
                y3 = y1 + y2
                z3 = z1 + x2*g1 + z2*i1
                s = s + FloatToLDraw(x3) + ' '
                s = s + FloatToLDraw(y3) + ' '
                s = s + FloatToLDraw(z3)
                SkipThis = True;
                for iii in range (StrLstCover.__len__()) :
                    if s==StrLstCover[iii] : SkipThis = False
                if SkipThis : break
            if SkipThis : continue
        strPrefix = 'B\\T'
        cmdReplace()
        """
          END of cmdFittingsClick STEP 3
        """ 
      
      
        """
         cmdFittingsClick STEP 4: Replace all parts that bottom details
          can be removed from
         (STEPs 3 & 4 should be easily baked into STEP 2...)
        """
        for i in range (CHKLST_INFILE.__len__()) :
            ldline = CHKLST_INFILE[i];
            if ldLineType(ldline) <> 1 : continue;
            frg = int(ldExtractFromLine(ldline, 2));
            if (frg>31) and (frg<48) : continue;
            if ldExtractFromLine(ldline, 7) <> '0' : continue;
            if ldExtractFromLine(ldline, 9) <> '0' : continue;
            if ldExtractFromLine(ldline, 10) <> '1' : continue;
            if ldExtractFromLine(ldline, 11) <> '0' : continue;
            if ldExtractFromLine(ldline, 13) <> '0' : continue;
            fil = ldExtractFromLine(ldline, 15);
            if len(fil)<5 : continue
            fil = fil[1:(len(fil)-4)+1]
    
            fil = os.path.join(LDRAWPATH ,'Parts' ,'B' ,fil + '.dat')
            if not os.path.exists(fil) : continue
            fil = fil[1:(len(fil)-4)+1]
            fil = fil + '.nfo'
          
            if not os.path.exists(fil) : continue
          
            x1 = float(ldExtractFromLine(ldline, 3))
            y1 = float(ldExtractFromLine(ldline, 4))
            z1 = float(ldExtractFromLine(ldline, 5))
            a1 = float(ldExtractFromLine(ldline, 6))
            c1 = float(ldExtractFromLine(ldline, 8))
            g1 = float(ldExtractFromLine(ldline, 12))
            i1 = float(ldExtractFromLine(ldline, 14))
            StrListInfil = []
            StrListInfil.exttend(fil)
            SkipThis = False
            for ii in range (StrListInfil.__len__()) :
                ldline = StrListInfil[ii];
                s = ldExtractFromLine(ldline, 1)
                x2 = float(ldExtractFromLine(ldline, 2))
                y2 = float(ldExtractFromLine(ldline, 3))
                z2 = float(ldExtractFromLine(ldline, 4))
                if s=='Top' : continue
                if s=='Stud' : continue
                if s=='Stud' : s = 'B '    # Scan for matching B
                if s=='Bottom' : s = 'T '  # Scan for matching T
                x3 = x1 + x2*a1 + z2*c1
                y3 = y1 + y2
                z3 = z1 + x2*g1 + z2*i1
                s = s + FloatToLDraw(x3) + ' '
                s = s + FloatToLDraw(y3) + ' '
                s = s + FloatToLDraw(z3)
                SkipThis = True
                for iii in range (StrLstCover.__len__()) :
                    if s==StrLstCover[iii] : SkipThis = False
                if SkipThis : break
            if SkipThis : continue
        strPrefix = 'B\\B'
        cmdReplace()
        """
          END of cmdFittingsClick STEP 4
        """  
        
        print
        print "Boxed %d parts" % REPLACEDTOTAL_COUNT
        
        if REPLACEDTOTAL_COUNT>0 :
        # 0 !LDOXER LEVEL info should also be automatically updated!
            CHKLST_INFILE.append("0 // Boxed Total {0} parts by {1} v{2}.".format(REPLACEDTOTAL_COUNT ,__name__ ,__version__))
            CHKLST_INFILE.append("0")
        
    
    
