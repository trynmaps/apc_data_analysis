import numpy as np
import matplotlib.pyplot as plt
import os
from apc_plot import APCPlotMixin
from apc_data_process import APCDataProcessMixin

class APCDataAnalysis(APCPlotMixin, APCDataProcessMixin):

    def __init__(self, load_data=True, clean_data=True):
        """
        General initializer
        """
        # annoying hard coded paths
        self.root_dir = os.path.join('/Users/edwardyoung/Google Drive/',
            'CodeForSF/OpenTransit/OT Raw Data (not in shared drive)')
        self.clean_data_dir = os.path.join('/Users/edwardyoung/Google Drive/',
            'CodeForSF/OpenTransit/clean_data')

        if load_data:
            self.load_data()

        if clean_data:
            self.clean_data()