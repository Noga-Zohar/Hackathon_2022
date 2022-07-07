# Analysis of multiple data measurements/experiments
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import numpy as np

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
    
    def __init__(self, experiment_list, path):
        ######################################################
        # PUT TESTING TO CHECK MORE THAN ONE ELEMENT IN LIST #
        ######################################################
        
        # edit ending times to match between all experiments
        self.list = experiment_list
        self.path = None  # for assigning path later on
        # find the shortest experiment time
        #time_thresh = min([len(datum.data) for datum in self.list]) #CHANGE '.DATA' LATER
        time_thresh = min([len(datum) for datum in self.list]) # DELETE LATER
        
        # crop all other measurements to fit the shortest
        for datum in self.list:
            datum = datum.head(time_thresh)

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
        multi = self.list[0].index
        compare_elec_df = pd.DataFrame(index=multi)
        title_template = 'Measurement{} vs. Measurement{}'
        
        # pairwise comparisons of all dataframes
        for df1, df2 in itertools.combinations(range(len(self.list)), 2):
            # create column title
            col_title = title_template.format(df1+1, df2+1)
            # add column data
            compare_elec_df[col_title] = self.list[df1].eq(self.list[df2])
        
        # return comparison dataframe
        self.electrode_comparison = compare_elec_df
    
    # correlation
    def correlate_data(self):
        """Calculate correlation coefficient per each band of each electrode,
        for pairwise comparisons of single experiments.
        """
        # assuming both dfs have the same electrodes - TEST to see if correct
        
        # create empty dataframe with dropped seconds from multindex
        multi = self.list[0].index
        corr_df = pd.DataFrame(index=multi).droplevel(level=0)
        corr_df.index = set(corr_df.index)
        
        # get base values for dataframe
        title_template = 'Meas{}/Meas{} Corr'
        electrode_values = set(self.list[0].index.get_level_values(1))
        band_values = set(self.list[0].index.get_level_values(2))
        
        # iterate over all pairwise comparisons
        for df1, df2 in itertools.combinations(range(len(self.list)), 2):
            # create column for each iteration
            col_title = title_template.format(df1+1, df2+1)
            corr_df[col_title] = np.nan
            
            # iterate over all possible electrodes
            for electrode in electrode_values:
                # get first dataframe
                df1_copy = self.list[df1].copy()
                elec_filter1 = df1_copy[np.in1d(df1_copy.index.get_level_values(1), [electrode])]
                # get second dataframe
                df2_copy = self.list[df2].copy()
                elec_filter2 = df2_copy[np.in1d(df2_copy.index.get_level_values(1), [electrode])]
                
                # iterate over all possible bands
                for band in band_values:
                    # get first dataframe 
                    band_filter1 = elec_filter1[np.in1d(elec_filter1.index.get_level_values(2), [band])]
                    # get second dataframe
                    band_filter2 = elec_filter2[np.in1d(elec_filter2.index.get_level_values(2), [band])]
                    
                    # correlation
                    print(band_filter1, band_filter2)
                    corr = band_filter1.corr(band_filter2)
                    #corr_df.loc[(electrode, band), col_title] = corr
        # DELETE LATER
        self.corr = corr
        self.b1 = band_filter1
        self.b2 = band_filter2
        
        # return correlation dataframe
        self.corr_comparison = corr_df