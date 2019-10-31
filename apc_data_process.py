import numpy as np
import os

class APCDataProcessMixin:

    def load_data(self, sort_by_date=True):
        """
        Load the raw npy files from disk. These have already been extracted
        from the csv file. This preprocessing makes the data reading much
        faster.
        """
        self.data = {}
        self.data['OPEN_DATE_TIME'] = np.load(os.path.join(self.clean_data_dir, 
            'OPEN_DATE_TIME.npy'))
        self.data['CLOSE_DATE_TIME'] = np.load(os.path.join(self.clean_data_dir, 
            'CLOSE_DATE_TIME.npy'))
        self.data['VEH_LAT'] = np.load(os.path.join(self.clean_data_dir,
            'VEH_LAT.npy'))
        self.data['VEH_LONG'] = np.load(os.path.join(self.clean_data_dir,
            'VEH_LONG.npy'))
        self.data['ONS'] = np.load(os.path.join(self.clean_data_dir, 
            'ONS.npy'))
        self.data['OFFS'] = np.load(os.path.join(self.clean_data_dir,
            'OFFS.npy'))
        self.data['RUN_ID'] = np.load(os.path.join(self.clean_data_dir, 
            'RUN_ID.npy'))
        self.data['ROUTE_ID'] = np.load(os.path.join(self.clean_data_dir, 
            'ROUTE_ID.npy'))

        if sort_by_date:
            # Sort by open time
            idx = np.argsort(self.data['OPEN_DATE_TIME'])
            for k in self.data.keys():
                self.data[k] = self.data[k][idx]


    def clean_data(self):
        """
        Generic function for cleaning data. Currently only cleans out 
        lat=0/long=0. 
        """
        # Mask files with lat = 0 or lon = 0
        mask = np.where(np.logical_or(self.data['VEH_LAT']==0, 
            self.data['VEH_LONG']==0))

        for k in self.data.keys():
            if isinstance(self.data[k][0], float):
                self.data[k][mask] = np.nan


