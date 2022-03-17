import sys
import os
os.chdir("codecarbon")
sys.path.append(".")

from codecarbon import EmissionsTracker,OfflineEmissionsTracker

import time
from datetime import datetime
import argparse
# import logging
# logging.basicConfig(level=logging.WARNING,handlers=[logging.FileHandler('info_4cc.log')])


def main(no_of_hours_to_run=1,update_interval=1,measure_power_secs=10,offline=True,country_iso_code=None):
    start_time = datetime.strptime(time.ctime(time.time()),"%a %b %d %H:%M:%S %Y")
    current_time = datetime.strptime(time.ctime(time.time()),"%a %b %d %H:%M:%S %Y")
    print(current_time-start_time)
    if offline:
        save_folder = os.path.join("..","Offline Emissions")
        if not os.path.exists(save_folder):
            os.mkdir(save_folder)
        tracker  = OfflineEmissionsTracker(output_dir=save_folder,country_iso_code=country_iso_code,measure_power_secs=measure_power_secs)
    else:
        save_folder = os.path.join("..","Online Emissions")
        if not os.path.exists(save_folder):
            os.mkdir(save_folder)
        tracker = EmissionsTracker(output_dir=save_folder,measure_power_secs=measure_power_secs)
    
    while(int(str(current_time-start_time).split(":")[0]) <= int(no_of_hours_to_run)):
        tracker.start()
        start_batch_time = datetime.strptime(time.ctime(time.time()),"%a %b %d %H:%M:%S %Y")
        current_batch_time = datetime.strptime(time.ctime(time.time()),"%a %b %d %H:%M:%S %Y")
        while(int(str(current_batch_time-start_batch_time).split(":")[1]) < int(update_interval)):
            current_batch_time = datetime.strptime(time.ctime(time.time()),"%a %b %d %H:%M:%S %Y")
        tracker.flush()
        current_time = datetime.strptime(time.ctime(time.time()),"%a %b %d %H:%M:%S %Y")
    tracker.stop()

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m","--mode",type=bool,help="wether to track in offline mode, need to provide ISO of country (default=False)",default=False)
    parser.add_argument("-t","--tracking_hours",type=int,help="No of hours to track (default=1)",default=1)
    parser.add_argument("-s","--saving_interval_mins",type=int,help="No of minutes after which the emissions should be saved (default=1)",default=1)
    parser.add_argument("-i","--iso",type=str,help="ISO code of country if mode is True (default='IND')",default="IND")
    parser.add_argument("-p","--measure_power_secs",type=int,help="interval in seconds to read data from devices (default=5)",default=5)
    
    
    args = parser.parse_args()
    main(
        no_of_hours_to_run=args.tracking_hours,
        update_interval=args.saving_interval_mins,
        measure_power_secs=args.measure_power_secs,
        offline=args.mode,
        country_iso_code=args.iso  
    )
    
    

