from serpapi import GoogleSearch
import pandas as pd
from helper import input_time, remove_duplicates
import boto3
import botocore
from e_analysis import EAnalysis
import streamlit as st

 
class DataProcess():
    
    def __init__(self):
        pass
    
    
    def collect(self, api_key):

        params = {
            "api_key": api_key,
            "engine": "google_jobs",
            "google_domain": "google.com",
            "q": "Data Analyst",
            "hl": "en",
            "gl": "us",
            "chips": "date_posted:today",
            "location": "United States",
        }
        
        # TODO Check results are obtained


        # obtain only the job results list of dicts fro the api
        search = GoogleSearch(params)
        results = search.get_dict()
        jobs_df = results['jobs_results']
        return jobs_df
    
    
    def clean_api_data(self, df):
        
        jobs_df = pd.concat([pd.DataFrame(df),
                            pd.json_normalize(df['detected_extensions'])],
                            axis=1).drop('detected_extensions', 1)
        jobs_df = jobs_df.drop('extensions', 1)
        input_time(jobs_df)
        
        return jobs_df
    
    
    def retrieve_cloud_dataset(self, jobs_df, aws_key_id, aws_secret, bucketname):
    
        new_df = pd.DataFrame()
        
        s3 = boto3.resource(
            service_name='s3',
            region_name='ap-southeast-2',
            aws_access_key_id=aws_key_id,
            aws_secret_access_key=aws_secret
        )
        
        ea = EAnalysis(jobs_df)
        ea.get_top_skills()
        
        try:
            
            s3.Object(bucketname, 'jobs_df.csv').load()       # check if there is originally a dataset in bucket
            
        except botocore.exceptions.ClientError as e:   
            if e.response['Error']['Code'] == "404":     # if no dataset in bucket, make it TODO maybe dont include this
                jobs_df.to_csv('jobs_df.csv')
                s3.Bucket(bucketname).upload_file(Filename='jobs_df.csv', Key='jobs_df.csv')
                return jobs_df
            
        else:                   # concatenate new data with original
            
            bucket = s3.Bucket(bucketname)
            bucket.download_file('jobs_df.csv', 'existing.csv')
            
            existing_df = pd.read_csv('existing.csv', index_col=0)
            
            remove_duplicates(existing_df, jobs_df)

            updated_df = pd.concat([existing_df, jobs_df], ignore_index=True)
            new_df = updated_df
            updated_df.to_csv('jobs_df.csv')

            s3.Bucket(bucketname).upload_file(Filename='jobs_df.csv', Key='jobs_df.csv')
        
        return new_df