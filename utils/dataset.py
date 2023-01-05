import os
import datetime
import numpy as np
import pandas as pd
import glob


class StudyInfoEncoder:
    """Encodes study info into a dataframe.
    """

    def __init__(self, source):
        """Initializes the StudyInfoEncoder class.

        Args:
            source (str): path to the study info csv file
        """
        self.activities = ['Start_Sit', 'Start_Stand',
                           'Start_Cycle1', 'Start_Cycle2', 'Start_Run1', 'Start_Run2']
        self.encodings = {v: i for i, v in enumerate(self.activities)}
        self.info = pd.read_csv(
            source, parse_dates=list(self.encodings.keys()))

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
            df.loc[df[timestamp_column] >= _info[activity].iloc[0],
                   activity_column] = self.encodings[activity]
        return df


class DatasetVersion1:

    def __init__(self, path="data/v1"):
        self.path = os.path.abspath(path)

    def e4_eda(self, participant_id, raw=False):
        sampling_rate = 4
        path = os.path.abspath(os.path.join(self.path, f'P{participant_id:02d}', "E4", "EDA.csv"))
        data = pd.read_csv(path, header=None)
        if raw:
            return data  # raw data
        start_time = datetime.datetime.fromtimestamp(
            float(data.iloc[0, 0]), tz=datetime.timezone.utc)
        start_time = start_time.replace(tzinfo=None)
        time_gap = int(1000/sampling_rate)  # ms
        data = pd.DataFrame({
            'timestamp': pd.date_range(start=start_time, periods=len(data.iloc[1:]), freq=f"{time_gap}ms"),
            'eda_raw': data.iloc[1:].values.reshape(-1),
        })
        return data

    def earbud_acc(self, participant_id, raw=False):
        path = os.path.abspath(os.path.join(
            self.path, f'P{participant_id:02d}', "EARBUDS"))
        left = glob.glob(os.path.join(path, "*imu-left.csv"))
        right = glob.glob(os.path.join(path, "*imu-right.csv"))

        def read_one_side(path, raw):
            df = pd.read_csv(path, low_memory=False)
            if raw:
                return df
            if participant_id == 1:
                start_time = datetime.datetime.strptime(
                    df.iloc[0, 0], '%Y-%m-%d %H:%M:%S'
                ).replace(tzinfo=datetime.timezone.utc)
                start_time_unix = start_time.timestamp() * 1000
            else:
                start_time_unix = float(df.iloc[0, 0])
            df.iloc[0, 0] = 0
            df['timestamp'] = df['timestamp'].astype(
                float) + start_time_unix
            df['timestamp'] = pd.to_datetime(
                df['timestamp'], unit='ms', utc=True)
            df = pd.DataFrame({
                'timestamp': df['timestamp'],
                'ax': df['ax'], 'ay': df['ay'], 'az': df['az'],
            })
            return df
        
        if len(left) > 0:
            left_df = read_one_side(left[0], raw)
        if len(right) > 0:
            right_df = read_one_side(right[0], raw)
            
        return left_df, right_df

    def muse_eeg(self, participant_id, raw=False):
        path = os.path.abspath(os.path.join(self.path, f'P{participant_id:02d}', "MUSE", "eeg.csv"))
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
