import pandas as pd
from data_process import DataProcess

class Importer:
    
    def __init__(self):
        pass
    

    def import_data(self, api_key, aws_key_id, aws_secret, bucketname):
        
        dp = DataProcess()
        collected_data = dp.collect(api_key)
        jobs_df = dp.clean_api_data(pd.DataFrame(collected_data))
        
        # Connect to AWS cloud and obtain all time data
        jobs_df = dp.retrieve_cloud_dataset(jobs_df, aws_key_id, aws_secret, bucketname)
        
        return jobs_df