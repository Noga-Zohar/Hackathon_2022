# Analysis of two or more data measurements

class ComparativeAnalysis:
    """Analysis of two or more data measurements.
    """
    def __init__(self, experiment_list):
        """_summary_
        """
        self.list = experiment_list
    
    # Edit
    def same_ending_time(self):
        # find the shortest measurement
        time_thresh = min([len(datum.data) for datum in self.list])
        # crop all other measurements to fit the shortest
        for datum in self.list:
            datum = datum.head(time_thresh)
        
    # Descriptive analysis
    
    
    # Correlation