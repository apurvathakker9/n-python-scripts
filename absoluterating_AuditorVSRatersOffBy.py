import libs.absoluterating_subsetscombi as absoluterating_subsetscombi
import pandas as p
import numpy as n


folder_name = 'rater_vs_rater'
combined_subsets = absoluterating_subsetscombi.subsheetscombi(
    folder_name=folder_name)

raterwise_data = {}
all_raters = combined_subsets['Rater email'].unique()
all_raters = n.delete(all_raters, n.where(all_raters == ''))

all_columns = combined_subsets.columns
auditor_data = combined_subsets[(
    combined_subsets['Rater Type'] == 'auditor') & (combined_subsets['abspagematch'].notnull())]

for rater in all_raters:
    rater_data = combined_subsets[(
        combined_subsets['Rater Type'] == 'rater') & (combined_subsets['abspagematch'].notnull()) & (combined_subsets['Rater email'] == rater)]

    rater_pm = rater_data['abspagematch'].str[:1]
    if(str(rater_data['abspagematch'].str[:2]).isnumeric()):
        rater_pm = rater_data['abspagematch'].str[:2]

    rater_data['numpagematch'] = rater_pm
    rater_data['auditorrating'] = ''
    rater_data['diff'] = ''
    for ind, r in rater_data.iterrows():
        page_match = r['abspagematch']
        rater_rat = str(page_match)[:1]

        auditor_rating = auditor_data[(
            auditor_data['Query'] == r['Query']) & (auditor_data['URL'] == r['URL'])]
        auditor_rating = auditor_rating['abspagematch'].values

        if not str(page_match[2:3]).isalpha():
            r['numpagematch'] = str(page_match)[:2]
            rater_rat = str(page_match)[:2]

        if len(auditor_rating) > 0:
            aud_rat = auditor_rating[0][:1]

            if not (auditor_rating[0][2:3]).isalpha():
                aud_rat = auditor_rating[0][:2]

            r['auditorrating'] = aud_rat
            r['diff'] = abs(
                int(rater_rat)-int(aud_rat))

    raterwise_data[rater] = rater_data

with p.ExcelWriter('auditor_vs_rater.xlsx') as writer:
    auditor_data.to_excel(writer, sheet_name="Auditor", index=False)
    for rater in all_raters:
        index_at = rater.index('@')
        raterwise_data[rater].to_excel(
            writer, sheet_name=rater[:index_at], index=False)
