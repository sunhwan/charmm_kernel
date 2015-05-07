from IPython.kernel.zmq.kernelbase import Kernel
from .CHARMM import CHARMM

class CharmmKernel(Kernel):
    implementation = 'CHARMM'
    implementation_version = '1.0'
    language = 'no-op'
    language_version = '0.1'
    language_info = {'mimetype': 'text/plain'}
    banner = "Echo kernel - as useful as a parrot"

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self._start_charmm()

    def _start_charmm(self):
        self.charmm = CHARMM()

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:
            self.charmm.sendCommand(code)
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

