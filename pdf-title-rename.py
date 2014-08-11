#!/usr/bin/env python

"""
script.py -- A script to perform some job

Usage: script.py [args]
"""

from __future__ import print_function, division

import os
import re
import sys
import argparse
import subprocess
# import numpy as np
# import scipy as sp

# Package imports

# External imports

# Constants


class Foobar(object):

    """
    This class runs the script
    """

    def __init__(self, args):
        self.args = args

    def main(self):
        """Entry point for running the script."""
        print(*self.args)
        return 0


if __name__ == "__main__":
    sys.exit(Foobar(sys.argv[1:]).main())

