import numpy as np
import pandas as pd
from typing import Union
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from muse_eeg import MuseEEG


class BasicAnalysis():
    ''' 
    Performs basic analysis (e.g., simple descriptive statistics and visualization, duration calculation and higlighting of speific events)
    on a single Muse EEG recording (specifically the absolute power columns).
    The class can answer specialized queried regarding the significance of specific wave bands and electrodes.
    This class transforms the data into long form data and its methods operate only on long form data.
    The intended data for this class is averaged per second (see class MuseEEG), but it can operate on non-averaged data as well.

    Methods:
    time_info - prints the duration of the recording in secs and HH:MM:SS format
    statistics_power - returns df of simple descriptive statistics (mean, std, max) for each wave band power in every second averaged over electrodes
                        as well as a graph of mean power vs. time. Can also be applied to electrodes instead of waves
    highest_band_power - returns df of wave bands' power recording that exceeded an inputted threshold calculated uniquely for each wave band*electrode combo
    band_significance - returns the most powerful band*electrode combo for each second
    specific_band_most_significant - returns the seconds during which a specific band and\or electrode appeared in band_significance, as well as calculating the commonality of that 

    Attributes:
    self.data - a long form version of the data (index of sec:electrode:band, sorted by sec)
    self.duration - the duration of the recording in seconds
    self.path - a path to save results in
    '''

    def __init__(self, data: pd.DataFrame, relevant_band : str = None, relevant_electrode: str = None, bands: list = ["Delta","Theta","Alpha","Beta","Gamma"], electrodes : list = ["TP9","AF7","AF8","TP10"],):
        """Initializes a BasicAnalysis object, and creates a long-form data attribute
            Parameters
            ----------
            data : pd.DataFrame
                A MuseEEG recording, ideally averaged per second.
            relevant_band, relevant_electrode: str, optional
                specified band and/or electrode of unique interest
            bands, electrodes: list, optional
                a list of all the bands and electrodes appearing in the data
        """
        #check if data is a non-empty dataframe, else raise errors
        if not isinstance(data,pd.DataFrame):
            raise TypeError(f"The object you were trying to pass as the data is {type(data)}, but it should have been a museEEG data type")
        elif data.empty:
            raise ValueError(f"The data frame you're trying to push is empty")

        self.duration = len(data) #while data isn't in long-form, extract duration (assuminf data is averaged per second)
        
        #transform data into long form
        data['sec']=range(len(data)) #add running sec column to data
        ff = pd.wide_to_long(data, stubnames=["Alpha","Beta","Gamma","Delta","Theta"],i='sec',j="electrode",sep='_',suffix=r'\w+') #add sec and electrode as indexes
        ff=ff.reset_index() #return sec and electrode to column status
        lf = pd.melt(ff, id_vars=["sec","electrode"],value_vars=["Alpha","Beta","Gamma","Delta","Theta"], var_name="band",value_name = "power") #create band column with value column being 'power'
        self.data = lf.set_index(["sec","electrode","band"]) #set new index
        self.data = self.data.sort_values(by=[('sec')])# sort by second
        
        self.data['power'] = self.data['power'].abs() #make sure values are in absolute values
        self.path = None  # for assigning path later on
        
        self.verify_data(electrodes, bands) #verify the electrodes and bands lists are relevant to data
        if relevant_band!=None: #if a band was inputted verify input
            self.verify_band(relevant_band)
        if relevant_electrode!=None: #verify input for electrode
            self.verify_electrode(relevant_electrode)
        
        self.rel_band = relevant_band
        self.rel_electrode = relevant_electrode
        self.bands = bands
        self.electrodes = electrodes
    
    def new_dir(self, path):
        """
        :param path: enter designated path for analysis output
        :return: None
        :Assign: self.path = path for output
        """
        self.path = path

    def verify_data(self,electrodes,bands):
        #verify that electrodes and bands given list data are the same as the ones in actual data          
        if set(electrodes) != set(self.data.index.get_level_values('electrode')):
            raise ValueError(f"The museEEG data you've entered doesn't match the bands names we expected, which are {bands}")
        if set(bands) != set(self.data.index.get_level_values('band')):
            raise ValueError(f"The museEEG data you've entered doesn't match the bands names we expected, which are {bands}")              

    def verify_band(self, relevant_band):
        #verify inputted band is a string and exists in the data
        if not isinstance(relevant_band, str):
            raise TypeError(f"We expected a string! Please pass a str band")
        elif relevant_band in set(self.data.index.get_level_values('band')) == False:
            raise ValueError(f"The band you specified, {relevant_band}, doesn't exist within the data")
    
    def verify_electrode(self, relevant_electrode):
        #verify inputted electrode is a string and exists in the data
        if not isinstance(relevant_electrode, str):
            raise TypeError(f"We expected a string! Please pass a str electrode")
        elif relevant_electrode in set(self.data.index.get_level_values('electrode')) == False:
            raise ValueError(f"The band you specified, {relevant_electrode}, doesn't exist within the data")
               
    def time_info(self):
        #return the duration of the recording in seconds and HH:MM:SS format
        print(f"This muse EEG recording lasted {self.duration} seconds, meaning {str(datetime.timedelta(seconds=self.duration))}")
        return self.duration
    
    def statistics_powers(self, rel_idx: str ="band"):
        """Calculates simple descriptive statistics (mean, std, max) for the power of each band for every second averaging over electrodes.
        Can also do so for the electrodes. 
        Parameters
            ----------
            rel_idx : str, optional
                either "band" (default) or "electrode" to indicate the relevant condition
        Returns
            ----------
            df_stats: pd.DataFrame
                df with the columns mean, std and max for each second
            means_plot: sns.lineplot
                a lineplot of the mean power of each band/electrode [bell] vs. time [sec]
        """     
        if (rel_idx!="band") & (rel_idx!="electrode"): #check if rel_idx input is band or electrode otherwise return error
            raise ValueError("The relevant index argument must be 'band' or 'electrode'")
        grouped = self.data.groupby(['sec',rel_idx]) #group data by sec and either band/electrode (over the other variable)
        mean_grouped = grouped.mean().rename(columns={'power': 'mean'}) #create mean series with power column
        std_grouped = grouped.std().rename(columns={'power': 'std'}) #std series
        max_grouped = grouped.max().rename(columns={'power': 'max'}) #max series
        df_stats = mean_grouped.join(std_grouped).join(max_grouped) #join the three serieses into a df
        means_plot = sns.lineplot(data = df_stats.reset_index(),x='sec',y='mean',hue=rel_idx) #create graph of means vs. time
        _ = means_plot.legend(bbox_to_anchor=(1, 1)) #correct legend location
        plt.savefig('graph_means_'+rel_idx+'.png')
        plt.show() #pop up graph
        df_stats.to_csv("statistics_powers_"+rel_idx+".csv")
        return df_stats, _
    
    def highest_band_powers(self,x:Union[int, float] = 2): 
        """Finds instances where the power of a band-electrode combination (e.g. a recording of a band from a certain combination) esceeded
        a certain threshold calculated from the mean and std relevant to the specific band-electrode combination throughout the entire recording.
        Can be used to examine peak amplitudes or removed outliers. 
        Parameters
            ----------
            x : str, optional
                a coefficient in the creation of the threshold (mean+x*std), defaulted as 2
        Returns
            ----------
            result_df: pd.DataFrame
                df with the index of the "band-electrode" names, data of the second in which the passing of the threshold occured
        """
        if not isinstance(x, (int, float)): #verify x is an integer or float
            raise TypeError("The threshold coefficient must be an integer or float")
        grouped = self.data.groupby(['electrode','band']) #remove the element of time
        mean_grouped = grouped.mean().rename(columns={'power': 'mean'}) #mean power for each electrode-band combo for the entire recording
        std_grouped = grouped.std().rename(columns={'power': 'std'}) #same for std
        df_stats = mean_grouped.join(std_grouped) #df of these means and stds (index of electrode and band)
        df_threshold = df_stats['mean'] + x*df_stats['std'] #create a df of threshold (index of electrode and band)
        result_df = pd.Series() #initialize an empty Series - results_df (we'll add occurences passing the threshold to it)
        for electrode in self.electrodes:
            for band in self.bands: #loop over each combo occurenece
                #create a temp df unique to each electrode-band combo of times where the threshold was passed
                passed = self.data.loc[:,electrode,band][self.data.loc[:,electrode,band]>=df_threshold.loc[electrode,band]].dropna(axis=0) 
                if passed.empty == False: #if such occurences exist add them to result_df with the data being the combined name
                    result_df = result_df.append(pd.Series(index=passed.index,data=(electrode+'_'+band)))
        result_df = pd.Series(result_df.index.values, index=result_df) #switch data and index of result_df so that the data is the seconds
        result_df.to_csv("above_threshold_power.csv")
        return result_df

    def band_significance(self, values: bool = True):
        """Finds the most powerful electrode-band combo for each second of recording.
        Parameters
            ----------
            values : bool, optional
                if True returns a df with the actual values and sec-electrode-band as index
                if False returns a df without the values and with band as a column insted of index
        Returns
            ----------
            occurence_df: pd.DataFrame
                df with the index depenedent on the values argument input
        """        
        
        if not isinstance(values, bool): #verifies values argument is a boolean
            raise TypeError("The values argument must be a boolean!")
        #finds the index of the maximal values per second; 
        # df is the original data frame in those indices (with dropped nan so that only the max values remain)
        occurence_df = self.data[self.data.groupby(['sec']).transform(lambda x: x == x.max()).astype(bool)].dropna(axis=0) 
        if values == False: #a unique case where the data is the band rather than the values
            occurence_df = occurence_df.reset_index().set_index(['sec','electrode'])
            occurence_df=occurence_df.drop(columns='power') #delete the values col
        occurence_df.to_csv("most_powerful_point.csv")
        return occurence_df
    
    def specific_band_most_significant(self):
        """Finds the occurences where a specifically inputted band and\or electrode appeared as the most powerful band and\or electrode of second.
        Relies on the method band_significance
        Returns
            ----------
            df: pd.DataFrame
                df with the index being the time of such an occurence
        """ 

        if (self.rel_band == None) and (self.rel_electrode == None): #verifies a band and/or electrode were specified
            raise ValueError(f"Both band and electrode values are missing. Please input a band and/or electrode")
        df = self.band_significance() #calls for the complete df of the most powerful elcetrode-band combos for each second
        if self.rel_band == None: #if obly electrode name was inputted
            sliced_df = df.loc[:,self.rel_electrode,:] #extract times where that electrode appeared in df
            count = len(sliced_df.index) #count the number of occurences
            #print the number of occurences and calculate the percentage of time this was true
            print(f"For {count} seconds this electrode had the most significant power, meaning for {count*100/self.duration} of the recording") 
        elif self.rel_electrode == None: #same for the case where only band name was inputted
            sliced_df = df.loc[:,:,self.rel_band]
            count = len(sliced_df.index)
            print(f"For {count} seconds this band had the most significant power, meaning for {count*100/self.duration} of the recording")
        else: #if both band and electrode were inputted only the combo of the two will return
            sliced_df = df.loc[:,self.rel_electrode,self.rel_band]
            count = len(sliced_df.index)
            print(f"For {count} seconds this electrode,band combo had the most significant power, meaning for {count*100/self.duration} of the recording")
        sliced_df.to_csv("relevant_peaks.csv")
        return sliced_df
