import numpy as np
import pandas as pd
import datetime

class BasicAnalysis(self: museEEG, relevant_band : str = None, relevant_electrode: str = None, bands = ["Delta","Theta","Alpha","Beta","Gamma"], electrodes = ["TP9","AF7","AF8","TP10"]):
    ''' 
    documentation NOT FINISHED
    '''
    def __init__(): ##NOT FINISHED!!!
        self.data = verify_data(data)
        self.band = verify_band(relevant_band)
        self.electrode = verify_electrode(relevant_electrode)
    
    def verify_data(data,bands,electrodes):
        #make sure data is muse eeg data and has all the appropriate col else give error
        if not isinstance(data, museEEG):
            raise TypeError(f"The object you were trying to pass as the data is {type(data)}, but it should have been a museEEG data type")
        all_names = bands.append(electrodes)
        for name in all_names:
            if data.loc[name] == False:
                raise ValueError(f"The museEEG data you've entered doesn't match the bands and electrodes names we expected, which are {all_names}")
        return data
    
    def verify_band(self, band):
        #make sure relevant band is of the given type else raise error. if no band given return none
        if (band == []) or (band == None):
            return None
        elif not isinstance(band, str):
            raise TypeError(f"We expected a string! Please pass a str band")
        elif self.loc[band] == False:
            raise ValueError(f"The band you specified, {band}, doesn't exist within the data")
        else:
            return [band] 
    
    def verify_electrode(self, electrode):
        #make sure relevant electrode is of the given type else rause error. if no electrode given return none
        if (electrode == []) or (electrode == None):
            return None
        elif not isinstance(electrode, str):
            raise TypeError(f"We expected a string! Please pass a str electrode")
        elif self.loc[electrode] == False:
            raise ValueError(f"The band you specified, {electrode}, doesn't exist within the data")
        else:
            return [electrode] 
    
    def time_info(self):
        #return the duration of the recording and the time-end time stamps
        duration = len(self.index())
        return f"""This muse EEG recording lasted {duration} seconds, meaning {str(datetime.timedelta(seconds=duration))}"""
    
    def statistics_powers(self, x="band"):     
        self['power'] = self['power'].abs()
        grouped = self.groupby(['time',x])
        mean_grouped = grouped.mean().rename(columns={'power': 'mean'})
        std_grouped = grouped.std().rename(columns={'power': 'std'})
        max_grouped = grouped.max().rename(columns={'power': 'max'})
        df_stats = mean_grouped.join(std_grouped).join(max_grouped)
        return df_stats
    
    def statistics_powers_electrode(self):     
        return statistics_power(self,'electrode')
    
    def highest_band_powers(self,electrodes,bands,x:int = 2): #NOT FINISHED
        #return a df with band-electrode power values that were more than 2 standard deviations above the average for that band-electrode
        self['power'] = self['power'].abs()
        grouped = self.groupby(['electrode','band'])
        mean_grouped = grouped.mean().rename(columns={'power': 'mean'})
        std_grouped = grouped.std().rename(columns={'power': 'std'})
        df_stats = mean_grouped.join(std_grouped)
        df_threshold = df_stats['mean'] + x*df_stats['std']
        result_df = pd.Series()
        for electrode in electrodes:
            for band in bands:
                passed = self.loc[:,electrode,band][self.loc[:,electrode,band]>=df_threshold.loc[electrode,band]].dropna(axis=0)
                if passed.empty == False:
                    result_df = result_df.append(pd.Series(index=passed.index,data=(electrode+'_'+band)))
        result_df = pd.Series(result_df.index.values, index=result_df) 
        return result_df

    def band_significance(self,bands,electrodes, values = True):
        #return a df with the band and electrode that had the most significant value for each second
        self['power'] = self['power'].abs()
        df = self[self.groupby(level=0).transform(lambda x: x == x.max()).astype(bool)].dropna(axis=0)
        df = df.reset_index().set_index(['time'])
        if values == False:
            df=df.drop(columns='power')
        return df
    
    def specific_band_most_significant(self,relevant_band,relevant_electrode):
        #return the time and duration during which the specific band was most significant in the specific electrode
        #if it never happened return that
        if relevant_band == None & relevant_electrode == None:
            raise ValueError(f"Both band and electrode values are missing. Please input a band and/or electrode")
        df = band_significance(self)
        if relevant_band == None:
            sliced_df = df.loc[:,relevant_electrode,:]
            count = len(sliced_df.index)
            print(f"For {count} seconds this electrode had the most significant power, meaning for {count*100/len(self.index)} of the recording") 
        elif relevant_electrode == None:
            sliced_df = df.loc[:,:,relevant_band]
            count = len(sliced_df.index)
            print(f"For {count} seconds this band had the most significant power, meaning for {count*100/len(self.index)} of the recording")
        else:
            sliced_df = df.loc[:,relevant_electrode,relevant_band]
            count = len(sliced_df.index)
            print(f"For {count} seconds this electrode,band combo had the most significant power, meaning for {count*100/len(self.index)} of the recording") 
        return sliced_df
    

