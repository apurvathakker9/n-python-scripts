import os
import pandas as p
import constants as c

final_dataframe = p.DataFrame()


def combineSheets(absoluteratings: p.DataFrame):
    global final_dataframe
    final_dataframe = p.concat([absoluteratings, final_dataframe])


def subsheetscombi(folder_name):
    base_path = c.BASE_PATH
    file_path = base_path + folder_name
    all_files = os.listdir(file_path)

    index = 0

    for single_file in all_files:
        abs_path = file_path+"/"+single_file
        absoluteratings = p.read_csv(abs_path)

        if(index == 0):
            for col in absoluteratings.columns:
                final_dataframe[col] = ''
        combineSheets(absoluteratings=absoluteratings)
        index += 1

    final_dataframe.to_csv('combi.csv')
    return final_dataframe


file_path = 'D:/beans/Neeva/Opeartions/All Ratings Post Audit/Absolute Ratings/discussion_onebox_reddit_stack_quora/'
# file_path = 'D:/beans/Neeva/Opeartions/All Ratings Post Audit/Absolute Ratings/test/'
subsheetscombi(file_path=file_path)
