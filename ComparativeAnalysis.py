# Analysis of two or more data measurements

class ComparativeAnalysis:
    """Analysis of two or more data measurements.
    """
    def __init__(self, experiment_list):
        """_summary_
        """
        # edit ending times to match between all experiments
        self.list = experiment_list
        # find the shortest experiment time
        time_thresh = min([len(datum.data) for datum in self.list]) #CHANGE '.DATA' LATER
        # crop all other measurements to fit the shortest
        for datum in self.list:
            datum = datum.head(time_thresh)
        
    # Descriptive analysis
    def compare_electrodes(self):
        comparison_bool = []
        for electrode in ...
    
    # Correlation