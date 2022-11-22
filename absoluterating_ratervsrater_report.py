import libs.absoluterating_subsetscombi_ratersInColumn as combineraters
import pandas as p
import numpy as np
import matplotlib.pyplot as plt
import io
from libs.constants import RATERS_INFO, ALL_TEAM

CHART_FIGURE_SIZE = (6, 4)


def get_output(final_dataframe: p.DataFrame, rater, writer):

    # Copy the original dataframe so that the changes do not affect
    reduced_dataframe = final_dataframe.copy()

    # filter by email if required
    if(rater['emailId'] != 'all'):
        reduced_dataframe = reduced_dataframe[(reduced_dataframe['Rater1_EmailId'] == rater['emailId']) | (
            reduced_dataframe['Rater2_EmailId'] == rater['emailId'])]

    # Create pivot table for difference in raters
    diff_rater_pivot = reduced_dataframe[(reduced_dataframe['Diff'] > 0)].pivot_table(
        index=['Diff'],
        aggfunc={'Diff': np.count_nonzero}
    )
    diff_rater_pivot.index.name = "Diff in Raters"
    diff_rater_pivot = diff_rater_pivot.reset_index()
    diff_rater_pivot.rename(columns={'Diff': '# Queries'}, inplace=True)
    x1 = diff_rater_pivot['Diff in Raters']
    y1 = diff_rater_pivot['# Queries']

    fig2, ax2 = plt.subplots(figsize=CHART_FIGURE_SIZE)
    plt.bar(x1, y1)
    plt.title("("+rater['name']+") Count of ratings off by")
    index = 0

    # Add labels on the chart for better interpretation
    for i in x1:
        ax2.text(x1[index], y1[index], y1[index], size='9')
        index += 1

    # Next Set

    # Create pivot table for summary
    pivot_df = reduced_dataframe.pivot_table(
        values=['Diff'], index=['SubsetId'],
        aggfunc={'SubsetId': np.count_nonzero, 'Diff': np.count_nonzero}
    )
    pivot_df.index.name = 'Subsets'
    pivot_df = pivot_df.reset_index()
    pivot_df['% Diff'] = pivot_df['Diff'] / pivot_df['SubsetId']
    pivot_df['% Diff'] = (pivot_df['% Diff'] * 100).round(0)

    pivot_df.rename(columns={'SubsetId': '# Queries',
                    'Diff': '# Diff'}, inplace=True)
    pivot_df = pivot_df[['Subsets', '# Queries', '# Diff', '% Diff']]

    x = pivot_df['Subsets']
    y = pivot_df['% Diff']

    fig, ax = plt.subplots(figsize=CHART_FIGURE_SIZE)
    plt.plot(x, y, marker='o')
    plt.xlabel("Subsets")
    plt.ylabel("Diff %")
    plt.title("("+rater['name']+") Rater vs Rater Diff % in Subsets")
    index = 0

    # Add labels on the chart for better interpretation
    for i in x:
        ax.text(x[index], y[index], str(y[index])+'%', size='9')
        index += 1

    # Convert % diff from numbers to %. The % value is in string.
    pivot_df['% Diff'] = (pivot_df['% Diff'].astype(str) + '%')

    # Calculate overall summary
    summary_df = {'Total Queries': [], 'Total Differences': [], '% Diff': []}
    summary_df['Total Queries'].append(pivot_df['# Queries'].sum())
    summary_df['Total Differences'].append(pivot_df['# Diff'].sum())
    summary_df['% Diff'].append(
        str(((summary_df['Total Differences'][0]/summary_df['Total Queries'][0])*100).round(0)) + '%')

    # Dynamically compute sheet names
    summary_sheet_name = rater['name']+'-Summary'
    logs_sheet_name = rater['name']+'-Logs'

    # Dynamically get the
    start_row_diff_rater = (pivot_df.shape[0] + 4 if pivot_df.shape[0]
                            > CHART_FIGURE_SIZE[0]*4 else CHART_FIGURE_SIZE[0]*4) + 2

    p.DataFrame(summary_df).to_excel(
        writer, sheet_name=summary_sheet_name, startcol=1, startrow=0, index=False)
    pivot_df.to_excel(writer, sheet_name=summary_sheet_name,
                      startrow=4, startcol=0, index=False)

    diff_rater_pivot.to_excel(writer, sheet_name=summary_sheet_name,
                              startrow=start_row_diff_rater, startcol=0, index=False)

    worksheet = writer.sheets[summary_sheet_name]

    # Save pyplot chart image to excel
    imgdata = io.BytesIO()
    fig.savefig(imgdata, format='png')
    worksheet.insert_image('F2', '', {'image_data': imgdata})

    imgdata2 = io.BytesIO()
    fig2.savefig(imgdata2)
    worksheet.insert_image(
        'F' + str(start_row_diff_rater), '', {'image_data': imgdata2})

    # chart = workbook.add_chart(
    #     {'type': 'line', 'title': 'Rater vs Rater % Diff'})
    # chart.add_series({'values': '=Summary!$D$6:$D$'+str(max_row+5)})

    # worksheet.insert_chart('G7', chart)

    reduced_dataframe.to_excel(
        writer, sheet_name=logs_sheet_name, index=False)


def rater_vs_rater_matrix(final_dataframe: p.DataFrame) -> p.DataFrame:
    raters_list = RATERS_INFO.copy()
    rater_names = []
    rater_to_remove = None
    for rater in raters_list:
        if(rater['name']) != 'All':
            rater_names.append(rater['name'])
        else:
            rater_to_remove = rater

    if rater_to_remove:
        raters_list.remove(rater_to_remove)

    matrix_df = p.DataFrame(columns=['', *rater_names], index=[''])

    for rater in raters_list:
        rater1_email = rater['emailId']
        rater1_name = rater['name']

        obj = {}
        obj[''] = rater1_name

        for rater2 in ALL_TEAM:
            rater2_email = rater2['emailId']
            rater2_name = rater2['name']
            resultant_df = final_dataframe[((final_dataframe['Rater1_EmailId'] == rater1_email) & (
                final_dataframe['Rater2_EmailId'] == rater2_email)) | ((final_dataframe['Rater1_EmailId'] == rater2_email) & (
                    final_dataframe['Rater2_EmailId'] == rater1_email))]

            total_queries = resultant_df.shape[0]
            diff_queries = resultant_df[(resultant_df['Diff'] != 0)].shape[0]

            output_str = ''
            if total_queries > 0:
                diff_per = str(
                    round((diff_queries/total_queries)*100, 0)) + '%'
                output_str = str(diff_queries) + '/' + \
                    str(total_queries) + ' (' + diff_per + ')'

            obj[rater2_name] = output_str

        # print(p.DataFrame(obj, index=['']))
        # print(matrix_df)
        matrix_df = p.concat([matrix_df, p.DataFrame(obj, index=[''])])

    matrix_df = matrix_df[1:]
    return matrix_df


folder_name = 'discussion_onebox_reddit_stack_quora_v2'
final_dataframe = combineraters.subsets_combi_ratersInColumn(
    folder_name=folder_name)

with p.ExcelWriter(folder_name+'.xlsx', engine="xlsxwriter") as writer:
    rater_vs_rater_matrix(final_dataframe=final_dataframe).to_excel(
        writer, sheet_name="Raters Matrix", index=False)
    for rater in RATERS_INFO:
        get_output(final_dataframe=final_dataframe, rater=rater, writer=writer)
