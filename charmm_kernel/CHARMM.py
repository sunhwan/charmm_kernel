import sys, os, re
import subprocess as sp

_charmm_exec = '/Users/sunhwan/local/charmm/c38b2'
_charmm_data = '/Users/sunhwan/local/charmm/toppar'
_s = re.compile('\s+')

class CHARMM:
    def __init__(self, output=None, exe=_charmm_exec):
        self._pid = sp.Popen(exe, stdin=sp.PIPE, stdout=sp.PIPE, close_fds=True, universal_newlines=True)
        (self._in, self._out) = (self._pid.stdin, self._pid.stdout)
        self._in.write("* title\n*\n\n")
        self._in.write("UNBUFIO\n")
        self._in.write("label _INIT\n")
        self._in.flush()
        self.lastOutput = None
        self.output = output
        self.getCharmmOutput('_INIT')
        self.params = {}

    def __del__(self):
        try:
            self._in.write("STOP\n")
            self._pid.wait()
        except:
            pass

    def loadParameters(self, top=None, par=None):
        top = "%s/%s" % (_charmm_data, top)
        par = "%s/%s" % (_charmm_data, par)
        self.sendCommand("""
read  rtf card name %s
read para card name %s""" % (top, par))

    def readpsf(self, psf):
        self.sendCommand("read  psf card name %s" % psf)

    def getCharmmOutput(self, exp="_DONE"):
        self.lastOutput = ""
        energy = False
        while 1:
            line = self._out.readline()
            if not line: return
            if line.strip().endswith(exp):
                return
            self.lastOutput += line

            # ENERGY
            if line.startswith('ENER ENR:') or line.startswith('INTE ENR:'):
                energy = True
                self.energy = {}
                energy_header = []
                i = 0
            if not line.strip():
                energy = False
            if energy:
                entries = _s.split(line.strip())
                if entries[1].endswith(':'):
                    energy_header.extend(map(lambda x: x[:4].lower(), entries[2:]))
                if entries[0].endswith('>') or entries[1].endswith('>'):
                    entries = entries[2:] if entries[1].endswith('>') else entries[1:]
                    for entry in entries:
                        try:
                            self.energy[energy_header[i]] = float(entry)
                            i += 1
                        except:
                            while entry:
                                n = re.match(r'-?\d+\.(\d+)?(?=-)?', entry).group()
                                entry = entry[len(n):]
                                self.energy[energy_header[i]] = float(n)
                                i += 1
            # PARAMETER
            if line.startswith(' Parameter:'):
                entries = line.strip().split()
                k,v = entries[1].lower(), entries[3][1:-1]
                if v.isdigit():
                    self.params[k] = int(v)
                else:
                    try:
                        self.params[k] = float(v)
                    except:
                        self.params[k] = v

    def sendCommand(self, cmd):
        if not self.lastOutput: 
            self.getCharmmOutput()

        for line in cmd.splitlines():
            self._in.write("%s\n" % line)

        self.lastOutput = None
        self._in.write("label _DONE\n")
        self._in.flush()
        self.getCharmmOutput()
        if self.output: self.output.write(self.lastOutput)
        #print self.lastOutput

    def kill(self):
        self.__del__()