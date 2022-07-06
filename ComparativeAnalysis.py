# Analysis of two or more data measurements
import pandas as pd
import itertools

class ComparativeAnalysis:
    """Analysis of two or more data measurements.
    """
    def __init__(self, experiment_list):
        """_summary_
        """
        ######################################################
        # PUT TESTING TO CHECK MORE THAN ONE ELEMENT IN LIST #
        ######################################################
        
        # edit ending times to match between all experiments
        self.list = experiment_list
        # find the shortest experiment time
        #time_thresh = min([len(datum.data) for datum in self.list]) #CHANGE '.DATA' LATER
        time_thresh = min([len(datum) for datum in self.list])
        # crop all other measurements to fit the shortest
        for datum in self.list:
            datum = datum.head(time_thresh)
        
    # Descriptive analysis
    def compare_electrodes(self):
        """_summary_
        """
        # create empty dataframe with multindex
        multi = self.list[0].index
        compare_elec_df = pd.DataFrame(index=multi)
        title_template = 'Measurement {} vs. Measurement {}'
        
        # pairwise comparison of all dataframes
        for df1, df2 in itertools.combinations(range(len(self.list)), 2):
            # create column title
            col_title = title_template.format(df1+1, df2+1)
            # add column data
            compare_elec_df[col_title] = self.list[df1].eq(self.list[df2])
        
        self.electrode_comparison = compare_elec_df
    
    # Correlation