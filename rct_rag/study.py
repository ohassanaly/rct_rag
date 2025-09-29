from config import *
import json
import re
from typing import Dict

class Study():
    def __init__(self, name:str, summary:dict, sections:dict, acronyms: dict) -> None:
        """ 
        name : the acronym of the study
        summary : the extracted summary table
        """
        self.name = name
        self.summary = summary
        self.acronyms = {k.lower(): v.lower() for k, v in acronyms.items()}
        
        section_mapping = {}
        for category, sections in sections.items():
            for section in sections:
                section_mapping[section] = category
        self.sections = section_mapping
    
    @staticmethod
    def normalize(text: str) -> str:
        """
        Normalize text by removing extra spaces, extra dashes and converting to lowercase.
        """
        text = re.sub(r'\s+', ' ', text.strip().lower())
        text = re.sub(r'-\s', ' ', text.strip().lower())
        return text
    
    def regroup_sections(self)-> None:
        """
        Group sections split into multiple pages
        Categorizes study sections based on predefined section titles and groups them accordingly.
        """

        grouped_summary : Dict = {}

        for section, text in self.summary.items():

            normalized_section = Study.normalize(section)
            normalized_text = Study.normalize(text)

            if normalized_section in list(self.sections.keys()) :
                grouped_summary[self.sections[normalized_section]] = normalized_text

            elif normalized_section == "" :
                last_section = list(grouped_summary.keys())[-1]
                grouped_summary[last_section] = grouped_summary[last_section] + normalized_text
            
        self.summary = grouped_summary

        return   

    def replace_acronyms(self) -> None :
        #case if the given study has no acronym found
        if self.acronyms == {} :
            return
        #general case
        for section, text in self.summary.items():
            words = text.split()
            replaced_words = [self.acronyms.get(word, word) for word in words]
            replaced_acronym_text = " ".join(replaced_words)
            self.summary[section] = replaced_acronym_text
        return
    
if __name__ == "__main__":
    with open(pdf_extracted_summary_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
    with open(acronym_path, 'r', encoding="utf-8") as file:
        acronym_dict = json.load(file)

        # #testing the loop for one study
        # study_name = list(data.keys())[0]
        # study_summary = list(data.values())[0]
        # acronym_list = acronym_dict[study_name]
        # study = Study(study_name, study_summary, section_categories, acronym_list)
        # print(study.summary)
        # print("_"*80)
        # print(study.acronyms)
        # study.regroup_sections()
        # study.replace_acronyms()
        # print("_"*80)
        # print(study.summary)

    #processing all the studies
    processed_studies = {}
    for study_name, summary in data.items():
        try :
            acronym_list = acronym_dict[study_name]
        except :
            acronym_list = {}
        study = Study(study_name, summary, section_categories, acronym_list)
        study.regroup_sections()
        study.replace_acronyms()

        processed_studies[study.name] = study.summary
    
    json_str = json.dumps(processed_studies, indent=4)
    with open(process_text_path, "w") as f:
        f.write(json_str)
