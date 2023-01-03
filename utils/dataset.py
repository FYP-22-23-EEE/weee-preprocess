import os
import datetime 
import numpy as np
import pandas as pd

class StudyInfoEncoder:
    """Encodes study info into a dataframe.
    """
    
    def __init__(self, source):
        """Initializes the StudyInfoEncoder class.

        Args:
            source (str): path to the study info csv file
        """
        self.activities = ['Start_Sit', 'Start_Stand', 'Start_Cycle1', 'Start_Cycle2', 'Start_Run1', 'Start_Run2']
        self.encodings = { v:i for i, v in  enumerate(self.activities)}
        self.info = pd.read_csv(source, parse_dates=list(self.encodings.keys()))
    
    def fit_activity_column(self, df, participant_id, 
                            timestamp_column='timestamp', 
                            activity_column='activity', 
                            activity_column_index=-1):
        """Fits the activity column to the dataframe.

        Args:
            df (pd.DataFrame): dataframe to fit the activity column to
            participant_id (int): participant id
            timestamp_column (str, optional): defaults to 'timestamp'
            activity_column (str, optional): defaults to 'activity'
            activity_column_index (int, optional): defaults to last column

        Returns:
            pd.DataFrame: dataframe with the activity column
        """
        _info = self.info[self.info['Participant'] == f"P{participant_id:02d}"]
        df.insert(activity_column_index, activity_column, np.nan)
        df[activity_column] = df[activity_column].astype('Int8')
        for activity in self.activities:
            df.loc[df[timestamp_column] >= _info[activity].iloc[0], activity_column] = self.encodings[activity]
        return df

class DatasetVersion1:
    
    def __init__(self, path):
        self.path = path
    
    def get(self, participant_id, device, sensor, raw=False):
        """Get dataset as pandas DataFrame

        Args:
            participant_id (int): participant ID [1-17]
            device (str): device name [E4, EARBUDS, MUSE, VO2, ZEPHYR]
            sensor (str): sensor name
                            E4 - [EDA]
                            MUSE - [EEG]
            raw (bool, optional): raw data or not. Defaults to False.

        Returns:
            pandas.DataFrame: dataset
        """
        if not 1 <= participant_id <= 17:
            raise ValueError('Participant ID must be between 1 and 17')
        path = os.path.join(self.path, f'P{participant_id:02d}')
        if device == 'E4' and sensor == 'EDA':
            return self.__e4_eda(path, raw)
        if device == 'MUSE' and sensor == 'EEG':
            return self.__muse_eeg(path, raw)
    
    def __e4_eda(self, path, raw):
        sampling_rate = 4
        path = os.path.abspath(os.path.join(path, "E4", "EDA.csv"))
        data = pd.read_csv(path, header=None)
        if raw:
            return data # raw data
        start_time = datetime.datetime.fromtimestamp(float(data.iloc[0, 0]), tz=datetime.timezone.utc)
        start_time = start_time.replace(tzinfo=None)
        time_gap = int(1000/sampling_rate) # ms
        data = pd.DataFrame({
            'timestamp': pd.date_range(start=start_time, periods=len(data.iloc[1:]), freq=f"{time_gap}ms"),
            'eda_raw': data.iloc[1:].values.reshape(-1),
        })
        return data
    
    def __muse_eeg(self, path, raw):
        path = os.path.abspath(os.path.join(path, "MUSE", "eeg.csv"))
        df = pd.read_csv(path, header=None,)
        if raw:
            return df
        # convert first column is unix epoch time to datetime
        df = pd.DataFrame({
            'timestamp': pd.to_datetime(df[0], unit='s', utc=True),
            'alpha': df[1], 'beta': df[2], 'delta': df[3], 'gamma': df[4], 'theta': df[5]
        })
        # remove timezone info 
        df['timestamp'] = df['timestamp'].dt.tz_convert(None)
        return df