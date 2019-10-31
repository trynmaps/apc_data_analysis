import numpy as np
import matplotlib.pyplot as plt

class APCPlotMixin:

    def plot_lat_lon(self, start_date, end_date, run_id=None, route_id=None):
        """
        Args:
        -----
        start_date (datetime) : The beginning of time to plot
        end_date (datetime) : The end of time to plot

        Opt Args:
        ---------
        run_id (int) : The ID of the run.
        route_id (int) : The route number. What do these 2 things really mean??
        """
        # Find indicies of data points between start and end dates
        idx = np.logical_and(self.data['OPEN_DATE_TIME'] > start_date, 
            self.data['OPEN_DATE_TIME'] < end_date)
        if run_id is not None:
            idx = np.logical_and(idx, self.data['RUN_ID'] == run_id)
        if route_id is not None:
            idx = np.logical_and(idx, self.data['ROUTE_ID'] == route_id)


        print(f'There are {np.sum(idx)} elements')

        fig, ax = plt.subplots(4, sharex=True, figsize=(5,8))
        ax[0].plot(self.data['OPEN_DATE_TIME'][idx], self.data['VEH_LAT'][idx])
        ax[1].plot(self.data['OPEN_DATE_TIME'][idx], self.data['VEH_LONG'][idx])
        ax[2].plot(self.data['OPEN_DATE_TIME'][idx], self.data['ONS'][idx], 
            label='On')
        ax[2].plot(self.data['OPEN_DATE_TIME'][idx], self.data['OFFS'][idx], 
            label='Off')
        ax[3].plot(self.data['OPEN_DATE_TIME'][idx], 
            np.cumsum(self.data['ONS'][idx])-np.cumsum(self.data['OFFS'][idx]))

        ax[2].legend(loc='upper right')
        ax[0].set_ylabel('Lat')
        ax[1].set_ylabel('Lon')
        ax[2].set_ylabel('On/Off #')
        ax[3].set_ylabel('Total #')
        ax[3].set_xlabel('Time')

        for tick in ax[3].get_xticklabels():
            tick.set_rotation(90)

        plt.tight_layout()

        plt.figure()
        plt.plot(self.data['VEH_LAT'][idx],self.data['VEH_LONG'][idx], '.')
        plt.xlabel('Lat')
        plt.ylabel('Long')