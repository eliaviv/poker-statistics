__author__ = "Eli Aviv"
__date__ = "25/11/2023"

import os
import shutil

OUTPUT_DIR = 'statistics_data'


def visualize_in_html(statistics_df, num_of_players):
    html = ['<head>', '<link rel="stylesheet" href="style.css" type="text/css" />', '</head>',
            '<table class="statistics">', f'<caption>Before Flop Statistics - {num_of_players} Players</caption>',
            '<tr>', '<td class="blank">', ' ', '</td>']

    for header in statistics_df.index:
        html.append('<td class="header">')
        html.append(header)
        html.append('</td>')
    html.append('</tr>')

    for i, row in enumerate(statistics_df.iterrows()):
        html.append('<tr>')

        html.append(f'<td class="header">')
        html.append(row[0])
        html.append('</td>')

        for j, cell in enumerate(row[1]):
            cell_value = float(cell[:-1])
            if cell_value < 8:
                css_class = 'fold'
            elif cell_value > 15:
                css_class = 'raise'
            else:
                css_class = 'call'

            if i == j:
                css_class += ' diagonal'

            html.append(f'<td class="{css_class}">')
            html.append(cell)
            html.append('</td>')

        html.append('</tr>')

    html.append('</table>')

    style_path = 'poker_statistics/visualization'
    style_file = 'style.css'
    if style_file not in os.listdir(OUTPUT_DIR):
        shutil.copy(f'{style_path}/{style_file}', OUTPUT_DIR)

    output_path = f'{OUTPUT_DIR}/pre_flop_statistics_{num_of_players}_players.html'
    with open(output_path, 'w') as f:
        f.writelines(html)


def visualize_in_csv(statistics_df, num_of_players):
    statistics_df.to_csv(f'{OUTPUT_DIR}/pre_flop_statistics_{num_of_players}_players.csv')
