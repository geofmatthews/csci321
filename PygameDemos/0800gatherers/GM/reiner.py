
import os, re, glob, sys
from pprint import pprint

class SpecMaker():
    def __init__(self, suffix='bmp'):
        
        namePattern = '(.*?)'
        headings = ['e','ne','n','nw','w','sw','s','se']
        spaceheadings = [' '+h for h in headings]
        headingPattern = '(' + '|'.join(spaceheadings) + ')'
        digitPattern = '(\d\d\d\d)'
        extensionPattern = '(.' + suffix + ')$'

        nameHeadingDigitPattern = namePattern + headingPattern \
                                  + digitPattern + extensionPattern
        nameDigitPattern = namePattern + digitPattern \
                           + extensionPattern
        nameHeadingPattern = namePattern + headingPattern \
                             + extensionPattern

        self.suffix = suffix

        self.nameHeadingDigitPattern = re.compile(nameHeadingDigitPattern)
        self.nameDigitPattern = re.compile(nameDigitPattern)
        self.nameHeadingPattern = re.compile(nameHeadingPattern)
        self.spec = 0

    def GetSpec(self,
                folders = 0,
                datafolder = 'data'):

        startfolder = os.getcwd()
        os.chdir(datafolder)
        if not folders:
            folders = [f for f in os.listdir('.') if os.path.isdir(f)]
        bigdict = {}
        print folders
        for folder in folders:
            cdict = {}
            for root, dirs, files in os.walk(folder):
                for f in files:
                    #print f
                    nameHeadingDigit = self.nameHeadingDigitPattern.match(f)
                    nameDigit = self.nameDigitPattern.match(f)
                    nameHeading = self.nameHeadingPattern.match(f)
                    if nameHeadingDigit:
                        name = nameHeadingDigit.group(1)
                        heading = nameHeadingDigit.group(2)
                        frame = nameHeadingDigit.group(3)
                        if not name in cdict:
                            cdict[name] = {'fileroot': os.path.join(datafolder,root,name),
                                           'frames': set([frame]),
                                           'headings': set([heading]),
                                           'suffix':self.suffix}
                        else:
                            cdict[name]['frames'].add(frame)
                            cdict[name]['headings'].add(heading)
                    elif nameDigit:
                        name = nameDigit.group(1)
                        frame = nameDigit.group(2)
                        if not name in cdict:
                            cdict[name] = {'fileroot': os.path.join(datafolder,root,name),
                                           'frames':set([frame]),
                                           'headings':set(['']),
                                           'suffix':self.suffix}
                        else:
                            cdict[name]['frames'].add(frame)
                    elif nameHeading:
                        name = nameHeading.group(1)
                        heading = nameHeading.group(2)
                        if not name in cdict:
                            cdict[name] = {'fileroot': os.path.join(datafolder,root,name),
                                           'frames':set(['']),
                                           'headings':set([heading]),
                                           'suffix':self.suffix}
                        else:
                            cdict[name]['headings'].add(heading)
            for name in cdict:
                #Turn sets into sorted lists:
                x = list(cdict[name]['frames'])
                x.sort()
                cdict[name]['frames'] = x
                x = list(cdict[name]['headings'])
                x.sort()
                cdict[name]['headings'] = x
            bigdict[folder] = cdict
        self.spec = bigdict
        os.chdir(startfolder)

    def SaveSpec(self,
                 folders = 0,
                 datafolder = 'data',
                 outputfile = 'default.rei'):
        if not self.spec:
            self.GetSpec(folders, datafolder)
        try:
            print 'Writing:  ' + datafolder + outputfile
            f = open(outputfile, 'w')
            pprint(self.spec, stream=f)
            f.close()
        except:
            print 'Unable to spec %s in %s' % (self.folders, self.datafolder)


if __name__ == "__main__":
    from pprint import pprint
    datafolder = os.path.join('..','data')
    s = SpecMaker(suffix='png')
    s.GetSpec(datafolder=datafolder)
    pprint(s.spec['T_crow'])
    if 0:
        s.SaveSpec(datafolder = datafolder)
        f = open(os.path.join(datafolder, 'default.rei'), 'r')
        print f.read()
        f.close()
    
    
        
                            
                            
