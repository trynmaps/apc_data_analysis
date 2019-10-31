import csv
import os
import datetime
import warnings
import numpy as np
import matplotlib.pyplot as plt

root_dir = os.path.join('/Users/edwardyoung/Google Drive/CodeForSF/OpenTransit/',
    'OT Raw Data (not in shared drive)')
clean_data_dir = os.path.join('/Users/edwardyoung/Google Drive/CodeForSF/',
    'OpenTransit/clean_data')


def format_and_save_apc_production_data(apc_file):
    """
    """
    data_dict = format_apc_production_csv(apc_file)
    for k in data_dict.keys():
        np.save(os.path.join(clean_data_dir, f'{k}'), data_dict[k])


def format_apc_production_csv(apc_file):
    """
    Extracts the data from a APC production CSV file and saves them as numpy
    files.
    """
    data_types = {
        'ACTUAL_SEQUENCE': "int", 
        'ACT_TRIP_START_TIME' : "datetime", 
        'APC_DATE_TIME' : "datetime",
        'BLOCK_ID' : "int",
        # 'BOOKING_ID' : "int", 
        'BOOKING_ID' : "str", 
        'BOOKING_NUM' : 'int', 
        'BOOKING_START_DATE' : 'datetime',
        'BS_ID' : 'int', 
        'CLOSE_DATE_TIME': 'datetime', 
        'CURRENT_ROUTE_ID': 'int', 
        'DATENUMBER' : 'int',
        'DATE_TYPE_VS': 'int', 
        'DIRECTION_CODE_ID': 'int', 
        'DWELL_TIME' : 'int',
        'EFFECTIVE_DATE_KEY_FK' : 'int', 
        'EXT_TRIP_ID' : 'int', 
        'GARAGE_ID': 'int',
        'HEADSIGN_ROUTE': 'int', 
        'IMPORT_ERROR' : 'int', 
        'IMPORT_TRIP_ERROR' : 'int',
        'INSERT_DATE_TIME' : 'datetime', 
        'MAX_LOAD' : 'int',
        'NON_REV_DISTANCE': 'int',
        'NON_REV_SECONDS': 'int', 
        'NUM_STAT' : 'int' ,
        'OFFS' : 'int',
        'ONS'  : 'int', 
        'OPEN_DATE_TIME' : 'datetime',
        'OPERATOR_ID' : 'int', 
        'POSITION_SOURCE' : 'int', 
        'PRIMARY_KEY' : 'int',
        'QUALITY_INDICATOR' : 'int', 
        'RAW_MAX_LOAD' : 'int', 
        'RAW_OFF' : 'int', 
        'RAW_ON' : 'int',
        'REV_DISTANCE' : 'float', 
        'REV_SECONDS' : 'int', 
        'ROUTE_ID' : 'int', 
        'RUN_ID' : 'int', 
        'SCHED_TIME' : 'datetime',
        'SEG_ARR_TIME' : 'datetime',
        'SEG_DEP_TIME' : 'datetime', 
        'START_TRIP_TIME' : 'datetime', 
        'TIME_ID' : 'int',
        'TP_ID' : 'int', 
        'TRANSIT_DATE_TIME' : 'datetime', 
        'VARIATION' : 'str', 
        'VEHICLE_ID' : 'int', 
        'VEH_LAT' : 'float',
        'VEH_LONG' : 'float'
    }

    with open(os.path.join(root_dir, apc_file), newline='') as csvfile:
        spamreader = csv.DictReader(csvfile)
        keys = spamreader.fieldnames  # Load dictionary keys

        # Extract data keys
        data_dict = {}
        for k in keys:
            data_dict[k] = []

        # Fill the data dictionary with values
        counter = 0
        for row in spamreader:
            if counter % 10000 == 0:
                print(f'Loaded {counter} lines')
            for k in keys:
                if k in data_types.keys():
                    data_dict[k].append(convert_type(row[k], data_types[k]))
            counter += 1

    return data_dict

def convert_type(dat, output_type):
    """
    Converts input data into the desired type. 
    """
    if output_type == "int":
        return int(dat)
    elif output_type == "datetime":
        return datetime.datetime.strptime(dat.split('.')[0], 
            '%Y-%m-%d %H:%M:%S')
    elif output_type == "float":
        return float(dat)
    elif output_type == "str":
        return str(dat)
    else:
        warnings.warn("Not an accepted datatype")

def plot_lat_lon(run_id, start_date, end_date):
    # Load the data
    odt = np.load(os.path.join(clean_data_dir, 'OPEN_DATE_TIME.npy'))
    lats = np.load(os.path.join(clean_data_dir,'VEH_LAT.npy'))
    lons = np.load(os.path.join(clean_data_dir,'VEH_LONG.npy'))
    ons = np.load(os.path.join(clean_data_dir, 'ONS.npy'))
    offs = np.load(os.path.join(clean_data_dir, 'OFFS.npy'))
    run_ids = np.load(os.path.join(clean_data_dir, 'RUN_ID.npy'))

    lats[lats==0] = np.nan
    lons[lons==0] = np.nan
    

    # Sort data
    ars = np.argsort(odt)
    run_ids = run_ids[ars]
    odt = odt[ars]
    lats = lats[ars]
    lons = lons[ars]
    ons = ons[ars]
    offs = offs[ars]

    time_idx = np.logical_and(odt > start_date, odt < end_date)

    print(f'There are {len(time_idx)} elements')

    run_ids = run_ids[time_idx]
    odt = odt[time_idx]
    lats = lats[time_idx]
    lons = lons[time_idx]
    ons = ons[time_idx]
    offs = offs[time_idx]

    # Choose run_id
    idx = np.where(run_ids == run_id)[0]

    fig, ax = plt.subplots(4, sharex=True, figsize=(5,8))
    ax[0].plot(odt[idx], lats[idx])
    ax[1].plot(odt[idx], lons[idx])
    ax[2].plot(odt[idx], ons[idx])
    ax[2].plot(odt[idx], offs[idx])
    ax[3].plot(odt[idx], np.cumsum(ons[idx])-np.cumsum(offs[idx]))
    plt.tight_layout()

    plt.figure()
    plt.plot(lats[idx],lons[idx], '.')


if __name__ == "__main__":
    apc_file = 'Not Confirmed - ProductionDW_APC_20170101_to_20170601.csv'
    # data_dict = format_apc_production_csv(apc_file)
    format_and_save_apc_production_data(apc_file)