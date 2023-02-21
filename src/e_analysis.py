

class EAnalysis:
    
    def __init__(self, df):
        self.df = df
    
    
    def keyword_dict(self):
        
        keywords_programming = [
            ' sql ', ' python ', ' r ', ' c ', ' c# ', ' javascript ', ' js ',  ' java ', ' scala ', ' sas ', ' matlab ', 
            ' c++ ', ' c/c++ ', ' perl ', ' go ', ' typescript ', ' bash ', ' html ', ' css ', ' php ', ' powershell ', ' rust ', 
            ' kotlin ', ' ruby ',  ' dart ', ' assembly ', ' swift ', ' vba ', ' lua ', ' groovy ', ' delphi ', ' objective-c ', 
            ' haskell ', ' elixir ', ' julia ', ' clojure ', ' solidity ', ' lisp ', ' f# ', ' fortran ', ' erlang ', ' apl ', 
            ' cobol ', ' ocaml ', ' crystal ', ' javascript/typescript ', ' golang ', ' nosql ', ' mongodb ', ' t-sql ', ' no-sql ',
            ' visual_basic ', ' pascal ', ' mongo ', ' pl/sql ',  ' sass ', ' vb.net ', ' mssql ', 
        ] 

        keywords_skills = [
            ' excel ', ' tableau ', ' word ', ' powerpoint ', ' looker ', ' powerbi ', ' power bi ', ' outlook ', ' azure ', ' jira ', ' twilio ', 
            ' shell ', ' linux ', ' sas ', ' sharepoint ', ' mysql ', ' visio ', ' git ', ' powerpoint ', ' postgresql ', ' seaborn ',
            ' pandas ', ' np ', ' aws ', ' gdpr ', ' spreadsheet ', ' alteryx ', ' github ', ' postgres ', ' ssis ', ' numpy ', ' power_bi ',
            ' microstrategy ', ' cognos ', ' dax ', ' matplotlib ', ' dplyr ', ' tidyr ', ' ggplot ', ' plotly ', ' esquisse ', ' docker ',
            ' jira ', ' hadoop ', ' airflow ', ' redis ', ' graphql ', ' sap ', ' tensorflow ', ' node ', ' jquery ', ' pyspark ', 
            ' pytorch ', ' gitlab ', ' selenium ', ' splunk ', ' bitbucket ', ' terminal ', ' ubuntu '
        ]
        
        return (keywords_programming, keywords_skills)


    def get_top_skills(self):
        
        lst = self.tokenize(self.keyword_dict()[0], self.keyword_dict()[1])
        self.df['skills_found'] = lst
       
    
    def tokenize(self, *word_bank):
        
        skills = []
        
        for idx in self.df.index:
            key_entries = []
            
            token = self.df['description'][idx].lower()
            token = token.replace(",", "")
            
            for bank in word_bank:
                for prog_skill in bank:
                    
                    if prog_skill in token and prog_skill not in key_entries:
                        key_entries.append(prog_skill)
            
            skills.append(key_entries)
            
        return list(skills)