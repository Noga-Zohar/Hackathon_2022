# Analysis of multiple data measurements/experiments
from cmath import nan
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

class ComparativeAnalysis:
    """Analysis of two or more data measurements.
    
    Returns
    -------
    A comparative data analysis object.
    
    list : a list containing all single experiment objects
            we want to compare.
    electrode_comparison : a bool dataframe containing all
                            pairwise comparisons of highest band power.
    corr_comparison : 
    
    """
    
    def __init__(self, experiment_list):
        # check that list has more than one value
        try:
            self.list = experiment_list
            
            if len(self.list) <= 1:
                del self
                raise InputError('Must be more than 1 experiment for a comparative analysis.')
            else:
                # edit ending times to match between all experiments
            
                # find the shortest experiment time
                time_thresh = min([len(datum.data) for datum in self.list])
                
                self.comp_list = [x.band_significance(values=False) for x in self.list]
                self.corr_list = [x.data for x in self.list]
                
                # crop all other measurements to fit the shortest
                for datum in self.comp_list:
                    datum = datum.head(time_thresh)
                for datum in self.corr_list:
                    datum = datum.head(time_thresh)
                
                self.path = None  # for assigning path later on
            
        except InputError as err:
            print(err.err_msg)

    def new_dir(self, path):
        """
        :param path: enter designated path for analysis output
        :return: None
        :Assign: self.path = path for output
        """
        self.path = path

    # descriptive analysis
    def compare_electrodes(self):
        """Compare highest band powers for pairwise
        comparisons of single experiments.
        """
        # create empty dataframe with multindex
        multi = self.comp_list[0].index
        compare_elec_df = pd.DataFrame(index=multi)
        title_template = 'Measurement{} vs. Measurement{}'
        
        # pairwise comparisons of all dataframes
        for df1, df2 in itertools.combinations(range(len(self.comp_list)), 2):
            # create column title
            col_title = title_template.format(df1+1, df2+1)
            # add column data
            compare_elec_df[col_title] = self.comp_list[df1].eq(self.comp_list[df2])
        
        # write comparison dataframe to csv file
        compare_path = self.path/'compare_electrodes.csv'
        compare_elec_df.to_csv(compare_path)
        
        # return comparison dataframe
        self.electrode_comparison = compare_elec_df
    
    # correlation
    def correlate_data(self):
        """Calculate correlation coefficient per each band of each electrode,
        for pairwise comparisons of single experiments.
        """
        # assuming both dfs have the same electrodes - TEST to see if correct
        
        # create empty dataframe with dropped seconds from multindex
        multi = self.corr_list[0].index
        corr_df = pd.DataFrame(index=multi).droplevel(level=0)
        corr_df.index = set(corr_df.index)
        
        # get base values for dataframe
        title_template = 'Meas{}/Meas{} Corr'
        electrode_values = set(self.corr_list[0].index.get_level_values(1))
        band_values = set(self.corr_list[0].index.get_level_values(2))
        
        # iterate over all pairwise comparisons
        for df1, df2 in itertools.combinations(range(len(self.corr_list)), 2):
            # create column for each iteration
            col_title = title_template.format(df1+1, df2+1)
            corr_df[col_title] = np.nan
            
            # iterate over all possible electrodes
            for electrode in electrode_values:
                # get first dataframe
                df1_copy = self.corr_list[df1].copy()
                elec_filter1 = df1_copy[np.in1d(df1_copy.index.get_level_values(1), [electrode])]
                # get second dataframe
                df2_copy = self.corr_list[df2].copy()
                elec_filter2 = df2_copy[np.in1d(df2_copy.index.get_level_values(1), [electrode])]
                
                # iterate over all possible bands
                for band in band_values:
                    # get first dataframe 
                    band_filter1 = elec_filter1[np.in1d(elec_filter1.index.get_level_values(2), [band])]
                    # get second dataframe
                    band_filter2 = elec_filter2[np.in1d(elec_filter2.index.get_level_values(2), [band])]
                    
                    # correlation
                    reset1 = band_filter1.reset_index()
                    reset2 = band_filter1.reset_index()
                    corr = reset1.power.corr(reset2.power)
                    corr_df.loc[(electrode, band), col_title] = corr
        
        # write correlation dataframe to csv file
        corr_path = self.path/'correlate_data.csv'
        corr_df.to_csv(corr_path)
        
        # return correlation dataframe
        self.corr_comparison = corr_df
        
class InputError(BaseException):
    """Error for incorrect input.
    """
    def __init__(self, err_msg):
        self.err_msg = err_msg