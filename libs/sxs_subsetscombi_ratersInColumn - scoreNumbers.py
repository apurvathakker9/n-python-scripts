import os
import pandas as p
import numpy as np
from constants import SXS_BASE_PATH


def print_final_dataframe():
    print('Queryset ', final_dataframe['QuerySet'].__len__())
    print('Query ', final_dataframe['Query'].__len__())
    for i in range(1, 3):
        print('Rater'+str(i)+'_Name',
              final_dataframe['Rater'+str(i)+'_Name'].__len__())
        print('Rater'+str(i)+'_EmailId',
              final_dataframe['Rater'+str(i)+'_EmailId'].__len__())
        print(final_dataframe['Rater'+str(i)+'_Score'].__len__())

    print('Auditor_Name', final_dataframe['Auditor_Name'].__len__())
    print(final_dataframe['Auditor_EmailId'].__len__())
    print(final_dataframe['Auditor_Score'].__len__())


def add_repetitve_columns(final_dataframe):
    for i in range(1, 3):
        final_dataframe['Rater'+str(i)+'_Name'] = []
        final_dataframe['Rater'+str(i)+'_EmailId'] = []
        final_dataframe['Rater'+str(i)+'_Score'] = []
        # final_dataframe['Rater'+str(i)+'_RelevantFirstRankLeft'] = []
        # final_dataframe['Rater'+str(i)+'_RelevantFirstRankRight'] = []
        # final_dataframe['Rater'+str(i)+'_Officialness'] = []
        # final_dataframe['Rater'+str(i)+'_Ambiguity'] = []
        # final_dataframe['Rater'+str(i)+'_Comfort'] = []
        # final_dataframe['Rater'+str(i)+'_Hardness'] = []
        # final_dataframe['Rater'+str(i)+'_RatingsRatedOn'] = []

    final_dataframe['Auditor_Name'] = []
    final_dataframe['Auditor_EmailId'] = []
    final_dataframe['Auditor_Score'] = []
    # final_dataframe['Auditor_RelevantFirstRankLeft'] = []
    # final_dataframe['Auditor_RelevantFirstRankRight'] = []
    # final_dataframe['Auditor_Officialness'] = []
    # final_dataframe['Auditor_Ambiguity'] = []
    # final_dataframe['Auditor_Comfort'] = []
    # final_dataframe['Auditor_Hardness'] = []
    # final_dataframe['Auditor_RatingsRatedOn'] = []


final_dataframe = {
    'QuerySet': [],
    'Query': [],
}

add_repetitve_columns(final_dataframe=final_dataframe)


def spread_csv_sheet(sxs_ratings: p.DataFrame):
    allqueries = sxs_ratings.iloc[:, 1].unique()
    for query in allqueries:
        raters = sxs_ratings[(sxs_ratings['Query'] == query) & (
            sxs_ratings['Rater Type'] == 'rater') & (sxs_ratings['aggregated score'].notnull())]
        if raters.__len__() > 0:
            final_dataframe['QuerySet'].append(raters.iloc[0, :]['Query Set'])
            final_dataframe['Query'].append(query)

            index = 1
            for ind, rater in raters.iterrows():
                if index == 3:
                    break
                score = rater['aggregated score']
                final_dataframe['Rater' +
                                str(index)+'_Name'].append(rater['Rater Name'])
                final_dataframe['Rater' +
                                str(index)+'_EmailId'].append(rater['Rater email'])
                final_dataframe['Rater' +
                                str(index)+'_Score'].append(score)
                # final_dataframe['Rater' +
                #                 str(index)+'_RelevantFirstRankLeft'].append(rater['rank_first_relevant_left'])
                # final_dataframe['Rater' +
                #                 str(index)+'_RelevantFirstRankRight'].append(rater['rank_first_relevant_right'])
                # final_dataframe['Rater' +
                #                 str(index)+'_Officialness'].append(rater['officialness'])
                # final_dataframe['Rater' +
                #                 str(index)+'_Ambiguity'].append(rater['ambiguity'])
                # final_dataframe['Rater' +
                #                 str(index)+'_Comfort'].append(rater['comfort'])
                # final_dataframe['Rater' +
                #                 str(index)+'_Hardness'].append(rater['hardness'])
                # final_dataframe['Rater' +
                #                 str(index)+'_RatingsRatedOn'].append(rater['Ratings Rated On'])
                index += 1

            if index == 2:
                final_dataframe['Rater2_Name'].append('')
                final_dataframe['Rater2_EmailId'].append('')
                final_dataframe['Rater2_Score'].append('')

            auditors = sxs_ratings[(sxs_ratings['Query'] == query) & (sxs_ratings['Rater Type']
                                                                      == 'auditor') & sxs_ratings['aggregated score'].notnull()]
            if auditors.__len__() == 0:
                final_dataframe['Auditor_Name'].append('')
                final_dataframe['Auditor_EmailId'].append('')
                final_dataframe['Auditor_Score'].append('')
                # final_dataframe['Auditor_RelevantFirstRankLeft'].append('')
                # final_dataframe['Auditor_RelevantFirstRankRight'].append('')
                # final_dataframe['Auditor_Officialness'].append('')
                # final_dataframe['Auditor_Ambiguity'].append('')
                # final_dataframe['Auditor_Hardness'].append('')
                # final_dataframe['Auditor_Comfort'].append('')
                # final_dataframe['Auditor_RatingsRatedOn'].append('')
            else:
                audit_index = 0
                for ind, auditor in auditors.iterrows():
                    if audit_index < 1:
                        score = auditor['aggregated score']

                        final_dataframe['Auditor_Name'].append(
                            auditor['Rater Name'])
                        final_dataframe['Auditor_EmailId'].append(
                            auditor['Rater email'])
                        final_dataframe['Auditor_Score'].append(score)
                        # final_dataframe['Auditor_RelevantFirstRankLeft'].append(
                        #     auditor['rank_first_relevant_left'])
                        # final_dataframe['Auditor_RelevantFirstRankRight'].append(
                        #     auditor['rank_first_relevant_right'])

                        # final_dataframe['Auditor_Officialness'].append(
                        #     auditor['officialness'])

                        # final_dataframe['Auditor_Ambiguity'].append(
                        #     auditor['ambiguity'])
                        # final_dataframe['Auditor_Hardness'].append(
                        #     auditor['hardness'])
                        # final_dataframe['Auditor_Comfort'].append(
                        #     auditor['comfort'])
                        # final_dataframe['Auditor_RatingsRatedOn'].append(
                        #     auditor['Ratings Rated On'])
                    audit_index += 1


def get_rater_diff(row):
    if row['Rater2_Score'].notnull():
        if(row['Rater1_Score'] == row['Rater2_Score']):
            return '1'
        elif (abs(int(row['Rater1_Score'])) - abs(int(row['Rater2_Score']))) == 1:
            return '0.5'
        else:
            return '0'
    return ''


def subsets_combi_ratersInColumn(folder_name: str):
    # Demo Path: D:\beans\Neeva\Opeartions\All Ratings Post Audit\Absolute Ratings\discussion_onebox_reddit_stack_quora\discussion_onebox_reddit_stack_quora-Subset1AllRating.csv
    # input('Input File Root Path:')
    base_path = SXS_BASE_PATH
    file_path = base_path + folder_name

    all_files = os.listdir(file_path)

    for single_file in all_files:
        abs_path = file_path+"/"+single_file
        absoluteratings = p.read_csv(abs_path)
        spread_csv_sheet(sxs_ratings=absoluteratings)

    # print_final_dataframe()

    export_dataframe = p.DataFrame(final_dataframe)
    export_dataframe['RaterDiffPoints'] = export_dataframe.apply(lambda row: ((1 if(row['Rater1_Score'] == row['Rater2_Score']) else (
        0.5 if abs((abs(int(row['Rater1_Score'])) - abs(int(row['Rater2_Score'])))) == 1 else 0)) if (row['Rater2_Score'] != '') else p.NA), axis=1)

    export_dataframe['Rater1_Diff'] = export_dataframe.apply(lambda row: ((1 if(row['Rater1_Score'] == row['Auditor_Score']) else (
        0.5 if abs((abs(int(row['Rater1_Score'])) - abs(int(row['Auditor_Score'])))) == 1 else 0)) if (row['Auditor_Score'] != '') else p.NA), axis=1)

    export_dataframe['Rater2_Diff'] = export_dataframe.apply(lambda row: ((1 if(row['Rater2_Score'] == row['Auditor_Score']) else (
        0.5 if abs((abs(int(row['Rater2_Score'])) - abs(int(row['Auditor_Score'])))) == 1 else 0)) if (row['Auditor_Score'] != '') else p.NA), axis=1)
    return export_dataframe


folder_name = 'test'

export_dataframe = subsets_combi_ratersInColumn(
    folder_name=folder_name)
export_dataframe.to_csv(folder_name+'.csv')
