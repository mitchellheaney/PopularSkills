import pandas as pd
from datetime import datetime, timedelta


def input_time(df):
    
    curr_time = datetime.now()
    updated_times = []
    for idx in df.index:
        posting_ref = df['posted_at'][idx]
        new_time = curr_time - timedelta(hours=int(posting_ref.split(' ')[0]))
        updated_times.append(new_time)
    df['datetime_posted'] = updated_times
    

def remove_duplicates(old, new):   # maybe change
    
    for idx_o in old.index:
        
        title = str(old['title'][idx_o])
        company = str(old['company_name'][idx_o])
        location = str(old['location'][idx_o])
        
        for idx_n in new.index:
            
            if (str(new['title'][idx_n]) == title and 
                str(new['company_name'][idx_n]) == company and 
                str(new['location'][idx_n]) == location):
                    new.drop([idx_n], axis=0, inplace=True)
                


    