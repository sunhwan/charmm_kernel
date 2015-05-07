from IPython.kernel.zmq.kernelapp import IPKernelApp
from .kernel import CharmmKernel
IPKernelApp.launch_instance(kernel_class=CharmmKernel)
