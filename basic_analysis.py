import numpy as np
import pandas as pd
import datetime
import pandas_bokeh
from muse_eeg import MuseEEG


class BasicAnalysis():
    ''' 
    documentation NOT FINISHED
    '''   
    def __init__(self, data: pd.DataFrame, relevant_band : str = None, relevant_electrode: str = None, bands: list = ["Delta","Theta","Alpha","Beta","Gamma"], electrodes : list = ["TP9","AF7","AF8","TP10"]): ##NOT FINISHED!!!
        if not isinstance(data,pd.DataFrame):
            raise TypeError(f"The object you were trying to pass as the data is {type(data)}, but it should have been a museEEG data type")
        elif data.empty:
            raise ValueError(f"The data frame you're trying to push is empty")
        self.duration = len(data)
        data['sec']=range(len(data))
        ff = pd.wide_to_long(data, stubnames=["Alpha","Beta","Gamma","Delta","Theta"],i='sec',j="electrode",sep='_',suffix=r'\w+')
        ff=ff.reset_index()
        lf = pd.melt(ff, id_vars=["sec","electrode"],value_vars=["Alpha","Beta","Gamma","Delta","Theta"], var_name="band",value_name = "power")
        self.data = lf.set_index(["sec","electrode","band"])
        self.data['power'] = self.data['power'].abs()
        self.data = self.data.sort_values(by=[('sec')])
        
        self.verify_data(electrodes, bands)
        if relevant_band!=None:
            self.verify_band(relevant_band)
        if relevant_electrode!=None:
            self.verify_electrode(relevant_electrode)
        
        self.rel_band = relevant_band
        self.rel_electrode = relevant_electrode
        self.bands = bands
        self.electrodes = electrodes
    
    def verify_data(self,electrodes,bands):
        #make sure data is muse eeg data and has all the appropriate col else give error          
        if set(electrodes) != set(self.data.index.get_level_values('electrode')):
            raise ValueError(f"The museEEG data you've entered doesn't match the bands names we expected, which are {bands}")
        if set(bands) != set(self.data.index.get_level_values('band')):
            raise ValueError(f"The museEEG data you've entered doesn't match the bands names we expected, which are {bands}")              

    def verify_band(self, relevant_band):
        #make sure relevant band is of the given type else raise error. if no band given return none
        if not isinstance(relevant_band, str):
            raise TypeError(f"We expected a string! Please pass a str band")
        elif relevant_band in set(self.data.index.get_level_values('band')) == False:
            raise ValueError(f"The band you specified, {relevant_band}, doesn't exist within the data")
    
    def verify_electrode(self, relevant_electrode):
        #make sure relevant electrode is of the given type else rause error. if no electrode given return none
        if not isinstance(relevant_electrode, str):
            raise TypeError(f"We expected a string! Please pass a str electrode")
        elif relevant_electrode in set(self.data.index.get_level_values('electrode')) == False:
            raise ValueError(f"The band you specified, {relevant_electrode}, doesn't exist within the data")
               
    def time_info(self):
        #return the duration of the recording and the time-end time stamps
        print(f"This muse EEG recording lasted {self.duration} seconds, meaning {str(datetime.timedelta(seconds=self.duration))}")
        return self.duration
    
    def statistics_powers(self, x="band"):     
        grouped = self.data.groupby(['sec',x])
        mean_grouped = grouped.mean().rename(columns={'power': 'mean'})
        std_grouped = grouped.std().rename(columns={'power': 'std'})
        max_grouped = grouped.max().rename(columns={'power': 'max'})
        df_stats = mean_grouped.join(std_grouped).join(max_grouped)
        _ = df_stats['mean'].plot_bokeh()
        return _, df_stats
    
    def highest_band_powers(self,x:int = 2): 
        #return a df with band-electrode power values that were more than 2 standard deviations above the average for that band-electrode
        grouped = self.data.groupby(['electrode','band'])
        mean_grouped = grouped.mean().rename(columns={'power': 'mean'})
        std_grouped = grouped.std().rename(columns={'power': 'std'})
        df_stats = mean_grouped.join(std_grouped)
        df_threshold = df_stats['mean'] + x*df_stats['std']
        result_df = pd.Series()
        for electrode in self.electrodes:
            for band in self.bands:
                passed = self.data.loc[:,electrode,band][self.data.loc[:,electrode,band]>=df_threshold.loc[electrode,band]].dropna(axis=0)
                if passed.empty == False:
                    result_df = result_df.append(pd.Series(index=passed.index,data=(electrode+'_'+band)))
        result_df = pd.Series(result_df.index.values, index=result_df) 
        return result_df

    def band_significance(self, values = True):
        #return a df with the band and electrode that had the most significant value for each second
        df = self.data[self.data.groupby(['sec']).transform(lambda x: x == x.max()).astype(bool)].dropna(axis=0)
        if values == False:
            df = df.reset_index().set_index(['sec'])
            df=df.drop(columns='power')
        return df
    
    def specific_band_most_significant(self):
        #return the time and duration during which the specific band was most significant in the specific electrode
        #if it never happened return that
        if (self.rel_band == None) and (self.rel_electrode == None):
            raise ValueError(f"Both band and electrode values are missing. Please input a band and/or electrode")
        df = self.band_significance()
        if self.rel_band == None:
            sliced_df = df.loc[:,self.rel_electrode,:]
            count = len(sliced_df.index)
            print(f"For {count} seconds this electrode had the most significant power, meaning for {count*100/self.duration} of the recording") 
        elif self.rel_electrode == None:
            sliced_df = df.loc[:,:,self.rel_band]
            count = len(sliced_df.index)
            print(f"For {count} seconds this band had the most significant power, meaning for {count*100/self.duration} of the recording")
        else:
            sliced_df = df.loc[:,self.rel_electrode,self.rel_band]
            count = len(sliced_df.index)
            print(f"For {count} seconds this electrode,band combo had the most significant power, meaning for {count*100/self.duration} of the recording")
        return sliced_df
    
"""
df = pd.read_csv("data.csv")
df=df[['TimeStamp', 'Delta_TP9', 'Delta_AF7', 'Delta_AF8', 'Delta_TP10', 'Theta_TP9', 'Theta_AF7', 'Theta_AF8', 'Theta_TP10', 'Alpha_TP9', 'Alpha_AF7', 'Alpha_AF8', 'Alpha_TP10', 'Beta_TP9', 'Beta_AF7', 'Beta_AF8', 'Beta_TP10', 'Gamma_TP9', 'Gamma_AF7','Gamma_AF8', 'Gamma_TP10']]
temp = BasicAnalysis(df)
print(temp.data)"""

x = MuseEEG()
x.read_data()
x.ave_sec()


temp = x.data_per_sec

temp = BasicAnalysis(x.data_per_sec,"Alpha")
df = temp.statistics_powers()
print(df)




