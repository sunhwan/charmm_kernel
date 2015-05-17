from IPython.kernel.zmq.kernelbase import Kernel
from IPython.display import HTML
from .CHARMM import CHARMM

class CharmmKernel(Kernel):
    implementation = 'CHARMM'
    implementation_version = '1.0'
    language = 'no-op'
    language_version = '0.1'
    language_info = {'mimetype': 'text/plain', 'name': 'CHARMM'}
    banner = "Echo kernel - as useful as a parrot"

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self._start_charmm()

    def _start_charmm(self):
        self.charmm = CHARMM()

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not self.charmm.is_running:
            self.charmm.kill()
            self._start_charmm()

        if code.startswith('%'):
            html = HTML("""
<script type="text/javascript" src="http://chemapps.stolaf.edu/jmol/jsmol/JSmol.min.js"/>
<script type="text/javascript">

Jmol._isAsync = false;

// last update 2/18/2014 2:10:06 PM

var jmolApplet0; // set up in HTML table, below

// logic is set by indicating order of USE -- default is HTML5 for this test page, though

var s = document.location.search;

// Developers: The _debugCode flag is checked in j2s/core/core.z.js, 
// and, if TRUE, skips loading the core methods, forcing those
// to be read from their individual directories. Set this
// true if you want to do some code debugging by inserting
// System.out.println, document.title, or alert commands
// anywhere in the Java or Jmol code.

Jmol._debugCode = (s.indexOf("debugcode") >= 0);

jmol_isReady = function(applet) {
    document.title = (applet._id + " - Jmol " + Jmol.___JmolVersion)
    Jmol._getElement(applet, "appletdiv").style.border="1px solid blue"
}       

var Info = {
    width: 300,
    height: 300,
    debug: false,
    color: "0xFFFFFF",
    addSelectionOptions: false,
    use: "HTML5",   // JAVA HTML5 WEBGL are all options
    j2sPath: "http://chemapps.stolaf.edu/jmol/jsmol/j2s", // this needs to point to where the j2s directory is.
    jarPath: "http://chemapps.stolaf.edu/jmol/jsmol/java",// this needs to point to where the java directory is.
    jarFile: "JmolAppletSigned.jar",
    isSigned: true,
    script: "set antialiasDisplay false;load files/1kdx.pdb; select *;cartoons off;wireframe -0.1",
    serverURL: "http://chemapps.stolaf.edu/jmol/jsmol/php/jsmol.php",
    readyFunction: jmol_isReady,
    disableJ2SLoadMonitor: true,
    disableInitialConsole: true,
    allowJavaScript: true
    //defaultModel: "$dopamine",
    //console: "none", // default will be jmolApplet0_infodiv, but you can designate another div here or "none"
}

$(document).ready(function() {
  $("#appdiv").html(Jmol.getAppletHtml("jmolApplet0", Info))
})
</script>
<div id="appdiv"></div>
            """)
            #stream_content = {'name': 'stdout', 'text': html.data}
            #self.send_response(self.iopub_socket, 'stream', stream_content)
            stream_content = {'source': 'kernel', 'data': {'text/html': html.data}, 'text': [repr(html)]}
            self.send_response(self.iopub_socket, 'display_data', stream_content)

        else:
            if not silent:
                self.charmm.sendCommand(code)
                #stream_content = {'name': 'stdout', 'text': self.charmm.lastOutput + "\n" + str(self.charmm.is_running)}
                stream_content = {'name': 'stdout', 'text': self.charmm.lastOutput}
                self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }

if __name__ == '__main__':
    #from IPython.kernel.zmq.kernelapp import IPKernelApp
    #IPKernelApp.launch_instance(kernel_class=EchoKernel)
    charmm = CHARMM()
    #charmm.loadParameters('top_all22_prot.inp', 'par_all22_prot.inp')

