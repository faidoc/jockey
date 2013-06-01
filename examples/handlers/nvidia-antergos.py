# (c) 2008 Canonical Ltd.
# Author: Martin Pitt <martin.pitt@ubuntu.com>
# License: GPL v2 or later

import logging

from jockey.handlers import KernelModuleHandler
from jockey.xorg_driver import XorgDriverHandler
from jockey.oslib import OSLib

# dummy stub for xgettext
def _(x): return x

class NvidiaDriver(XorgDriverHandler):
    def __init__(self, backend):
        self._free = False
        # use "None" as driver_package, since we have several;
        # LocalKernelModulesDriverDB overwrites it later with the correct
        # package from the modalias lists
        XorgDriverHandler.__init__(self, backend, 'nouveau', None,
            'nvidia', 'nv', {'NoLogo': 'True'},
            add_modules=[], disable_modules=[],
            remove_modules=[],
            name=_('NVIDIA accelerated graphics driver'),
            description=_('3D-accelerated proprietary graphics driver for '
                'NVIDIA cards.'),
            rationale=_('This driver is required to fully utilise '
                'the 3D potential of NVIDIA graphics cards, as well as provide '
                '2D acceleration of newer cards.\n\n'
                'If you wish to enable desktop effects, this driver is '
                'required.\n\n'
                'If this driver is not enabled, you will not be able to '
                'enable desktop effects and will not be able to run software '
                'that requires 3D acceleration, such as some games.'))
        
        self.package = 'nvidia'
        self._do_rebind = False
        
    def id(self):
        '''Return an unique identifier of the handler.'''

        if self.package:
            i = 'xorg:' + self.package

        return i

    def enabled(self):
        return KernelModuleHandler.enabled(self)

    def enables_composite(self):
        '''Return whether this driver supports the composite extension.'''

        # When using an upstream installation, or -new/-legacy etc., we already
        # have composite
        if KernelModuleHandler.module_loaded('nvidia'):
            logging.debug('enables_composite(): already using nvidia driver from nondefault package')
            return False

        # neither vesa nor nv support composite, so safe to say yes here
        return True