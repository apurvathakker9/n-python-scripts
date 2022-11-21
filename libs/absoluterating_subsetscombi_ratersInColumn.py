import os
import pandas as p
import numpy as np
import constants as c


def add_repetitve_columns(final_dataframe):
    for i in range(1, 4):
        final_dataframe['Rater'+str(i)+'_Name'] = []
        final_dataframe['Rater'+str(i)+'_EmailId'] = []
        final_dataframe['Rater'+str(i)+'_UserIntent'] = []
        final_dataframe['Rater'+str(i)+'_Ambiguity'] = []
        final_dataframe['Rater'+str(i)+'_Hardness'] = []
        final_dataframe['Rater'+str(i)+'_Comfort'] = []
        final_dataframe['Rater'+str(i)+'_PageQuality'] = []
        final_dataframe['Rater'+str(i)+'_PageMatch'] = []
        final_dataframe['Rater'+str(i)+'_QueryRatedOn'] = []
        final_dataframe['Rater'+str(i)+'_ResultRatedOn'] = []

    final_dataframe['Auditor_Name'] = []
    final_dataframe['Auditor_EmailId'] = []
    final_dataframe['Auditor_UserIntent'] = []
    final_dataframe['Auditor_Ambiguity'] = []
    final_dataframe['Auditor_Hardness'] = []
    final_dataframe['Auditor_Comfort'] = []
    final_dataframe['Auditor_PageQuality'] = []
    final_dataframe['Auditor_PageMatch'] = []
    final_dataframe['Auditor_QueryRatedOn'] = []
    final_dataframe['Auditor_ResultRatedOn'] = []


final_dataframe = {
    'QuerySet': [],
    'SubsetId': [],
    'Query': [],
    'Url': [],
}

add_repetitve_columns(final_dataframe=final_dataframe)


def spread_csv_sheet(absoluteratings: p.DataFrame):
    allqueries = absoluteratings.iloc[:, 2].unique()
    for query in allqueries:
        results = absoluteratings[absoluteratings['Query']
                                  == query].iloc[:, 3].unique()
        for result in results:
            raters = absoluteratings[(absoluteratings['Query'] == query) & (absoluteratings['URL'] == result) & (absoluteratings['Rater Type']
                                                                                                                 == 'rater') & (absoluteratings['abspagematch'].notnull())]
            final_dataframe['QuerySet'].append(raters.iloc[0, :]['Query Set'])
            final_dataframe['SubsetId'].append(raters.iloc[0, :]['Subset ID'])
            final_dataframe['Query'].append(query)
            final_dataframe['Url'].append(result)

            index = 1
            for ind, rater in raters.iterrows():
                final_dataframe['Rater' +
                                str(index)+'_Name'].append(rater['Rater Name'])
                final_dataframe['Rater' +
                                str(index)+'_EmailId'].append(rater['Rater email'])
                final_dataframe['Rater' +
                                str(index)+'_UserIntent'].append(rater['absuserintent'])
                final_dataframe['Rater' +
                                str(index)+'_Ambiguity'].append(rater['absqueryambiguity'])
                final_dataframe['Rater' +
                                str(index)+'_Hardness'].append(rater['absqueryhardness'])
                final_dataframe['Rater' +
                                str(index)+'_Comfort'].append(rater['absratercomfort'])
                final_dataframe['Rater' +
                                str(index)+'_PageQuality'].append(rater['abspagequality'])
                final_dataframe['Rater' +
                                str(index)+'_PageMatch'].append(rater['abspagematch'][:1])
                final_dataframe['Rater' +
                                str(index)+'_QueryRatedOn'].append(rater['Query Rated On'])
                final_dataframe['Rater' +
                                str(index)+'_ResultRatedOn'].append(rater['Result Rated On'])
                index += 1

            if index == 3:
                final_dataframe['Rater3_Name'].append('')
                final_dataframe['Rater3_EmailId'].append('')
                final_dataframe['Rater3_UserIntent'].append('')
                final_dataframe['Rater3_Ambiguity'].append('')
                final_dataframe['Rater3_Hardness'].append('')
                final_dataframe['Rater3_Comfort'].append('')
                final_dataframe['Rater3_PageQuality'].append('')
                final_dataframe['Rater3_PageMatch'].append('')
                final_dataframe['Rater3_QueryRatedOn'].append('')
                final_dataframe['Rater3_ResultRatedOn'].append('')

            auditors = absoluteratings[(absoluteratings['Query'] == query) & (absoluteratings['URL'] == result) & (absoluteratings['Rater Type']
                                                                                                                   == 'auditor') & absoluteratings['abspagematch'].notnull()]
            if auditors.__len__() == 0:
                final_dataframe['Auditor_Name'].append('')
                final_dataframe['Auditor_EmailId'].append('')
                final_dataframe['Auditor_UserIntent'].append('')
                final_dataframe['Auditor_Ambiguity'].append('')
                final_dataframe['Auditor_Hardness'].append('')
                final_dataframe['Auditor_Comfort'].append('')
                final_dataframe['Auditor_PageQuality'].append('')
                final_dataframe['Auditor_PageMatch'].append('')
                final_dataframe['Auditor_QueryRatedOn'].append('')
                final_dataframe['Auditor_ResultRatedOn'].append('')
            else:
                for ind, auditor in auditors.iterrows():
                    final_dataframe['Auditor_Name'].append(
                        auditor['Rater Name'])
                    final_dataframe['Auditor_EmailId'].append(
                        auditor['Rater email'])
                    final_dataframe['Auditor_UserIntent'].append(
                        auditor['absuserintent'])
                    final_dataframe['Auditor_Ambiguity'].append(
                        auditor['absqueryambiguity'])
                    final_dataframe['Auditor_Hardness'].append(
                        auditor['absqueryhardness'])
                    final_dataframe['Auditor_Comfort'].append(
                        auditor['absratercomfort'])
                    final_dataframe['Auditor_PageQuality'].append(
                        auditor['abspagequality'])
                    final_dataframe['Auditor_PageMatch'].append(
                        auditor['abspagematch'][:1])
                    final_dataframe['Auditor_QueryRatedOn'].append(
                        auditor['Query Rated On'])
                    final_dataframe['Auditor_ResultRatedOn'].append(
                        auditor['Result Rated On'])


def subsets_combi_ratersInColumn(folder_name: str):
    # Demo Path: D:\beans\Neeva\Opeartions\All Ratings Post Audit\Absolute Ratings\discussion_onebox_reddit_stack_quora\discussion_onebox_reddit_stack_quora-Subset1AllRating.csv
    # input('Input File Root Path:')
    base_path = c.BASE_PATH
    file_path = base_path + folder_name

    all_files = os.listdir(file_path)

    for single_file in all_files:
        abs_path = file_path+"/"+single_file
        absoluteratings = p.read_csv(abs_path)
        spread_csv_sheet(absoluteratings=absoluteratings)

    export_dataframe = p.DataFrame(final_dataframe)
    export_dataframe['Diff'] = export_dataframe.apply(lambda row: abs(
        int(row['Rater1_PageMatch'])-int(row['Rater2_PageMatch'])), axis=1)
    return export_dataframe


folder_name = 'discussion_onebox_reddit_stack_quora_v2'
# folder_name = 'test'

# export_dataframe = subsets_combi_ratersInColumn(
#     folder_name=folder_name)
# export_dataframe.to_csv(folder_name+'.csv')
