import libs.absoluterating_subsetscombi_ratersInColumn as combineraters
import pandas as p
import numpy as np
import matplotlib.pyplot as plt
import io

CHART_FIGURE_SIZE = (6, 4)

RATERS_INFO = [
    {
        'emailId': 'all',
        'name': 'All'
    },
    {
        'emailId': 'eb.neeva.a8@gmail.com',
        'name': 'Badal'
    },
    {
        'emailId': 'eb.neeva.a9@gmail.com',
        'name': 'Deepak'
    }
]


def get_output(final_dataframe: p.DataFrame, rater, writer):

    # Copy the original dataframe so that the changes do not affect
    reduced_dataframe = final_dataframe.copy()

    # filter by email if required
    if(rater['emailId'] != 'all'):
        reduced_dataframe = reduced_dataframe[(reduced_dataframe['Rater1_EmailId'] == rater['emailId']) | (
            reduced_dataframe['Rater2_EmailId'] == rater['emailId'])]

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

    p.DataFrame(summary_df).to_excel(
        writer, sheet_name=summary_sheet_name, startcol=1, startrow=0, index=False)
    pivot_df.to_excel(writer, sheet_name=summary_sheet_name,
                      startrow=4, startcol=0, index=False)

    worksheet = writer.sheets[summary_sheet_name]

    # Save pyplot chart image to excel
    imgdata = io.BytesIO()
    fig.savefig(imgdata, format='png')
    worksheet.insert_image('F2', '', {'image_data': imgdata})
    # chart = workbook.add_chart(
    #     {'type': 'line', 'title': 'Rater vs Rater % Diff'})
    # chart.add_series({'values': '=Summary!$D$6:$D$'+str(max_row+5)})

    # worksheet.insert_chart('G7', chart)

    reduced_dataframe.to_excel(
        writer, sheet_name=logs_sheet_name, index=False)


folder_name = 'discussion_onebox_reddit_stack_quora_v2'
final_dataframe = combineraters.subsets_combi_ratersInColumn(
    folder_name=folder_name)

with p.ExcelWriter(folder_name+'.xlsx', engine="xlsxwriter") as writer:
    for rater in RATERS_INFO:
        get_output(final_dataframe=final_dataframe, rater=rater, writer=writer)
