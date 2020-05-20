import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plots.trace_visualisation as trace_visualisation
import pathlib
import os

APP_PATH = str(pathlib.Path(__file__).parent.resolve())

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
server = app.server

def get_app(sampled_vehicle_ids, best_fit_vehicle, trace_visual, summary_df):

    display_data_table = pd.DataFrame(index=[0, 1], columns=['Vehicle ID', 'Distance (miles)', 'Time in Network',
                                                             'Fuel Economy (mpg)'])
    # display_data_table.loc[0] = summary_df.loc['Total_average']
    # display_data_table.loc[1] = summary_df.loc[best_fit_vehicle]


    font = {'family': "Courier New, monospace"}

    SIDEBAR_STYLE = {
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "20rem",
        "padding": "2rem 1rem",
        "background-color": "#f9f9f9",
        'box-shadow': "2px 2px 2px lightgrey",
    }

    NAV_TEXT_STYLE = {'font-size': 'medium',
                      'font-family': font['family'],
                      }

    CONTENT_STYLE = {
        "margin-left": "2rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem",
        'font-size': 'medium',
        'font-family': font['family'],
    }

    tabs_styles = {
        'height': '44px'
    }

    tab_style = {
        # 'borderBottom': '1px solid #d6d6d6',
        'margin-top': "2rem",
        'box-shadow': "2px 2px 2px lightgrey",
        'padding': "2rem 1rem",
        'font-family': font['family'],
        'font-size': 'medium',
    }

    tab_selected_style = {
        # 'borderTop': '1px solid #d6d6d6',
        # 'borderBottom': '1px solid #d6d6d6',
        'margin-top': "2rem",
        'backgroundColor': '#119DFF',
        'color': 'white',
        'padding': "2rem 1rem",
        'font-family': font['family'],
        'font-size': 'medium',
    }

    drop_down_options = ['Best Fit'] + list(sampled_vehicle_ids)

    html_base = html.Div([
        html.H1("US69 SUMO Vehicle Emissions Output Analysis",
                style={
                    "text-align": "center",
                    "font-family": font['family'],
                    'padding': 5,
                }),
        html.Div([
            html.H4("Vehicle_ID",
                    style={
                        "text-align": "center",
                        "font-family": font['family'],
                        'padding': 5,
                    }),
            dcc.Dropdown(
                id='vehicle_id',
                options=[{'label': id, 'value': id} for id in drop_down_options],
                value=drop_down_options[0]
            ),
        ],
            style={"margin-left": "2rem", 'width': '33%', 'display': 'inline-block', 'font-size': 'medium',
                   'font-family': font['family']}),
        html.Div([html.Div(id='summary-table', style=CONTENT_STYLE)]),
        html.Div([dcc.Graph(id='trace-figure',
                            style={
                                'height': 600,
                                "border-radius": 5,
                                'background-color': "#f9f9f9",
                                'margin': 5,
                                # 'padding': 10,
                                'position': "relative",
                                'box-shadow': "2px 2px 2px lightgrey",
                            },
                            )]),
    ], style=CONTENT_STYLE)


    @app.callback(
        dash.dependencies.Output('trace-figure', 'figure'),
        [dash.dependencies.Input('vehicle_id', 'value'), ])
    def update_graph(vehicle_id):
        if vehicle_id == 'Best Fit':
            vehicle_id = best_fit_vehicle

        return trace_visual(vehicle_id)


    @app.callback(
        dash.dependencies.Output('summary-table', 'children'),
        [dash.dependencies.Input('vehicle_id', 'value')])
    def update_table(vehicle_id):
        # ['Distance (miles)', 'Time in Network', 'Fuel Economy (mpg)']

        if vehicle_id == 'Best Fit':
            vehicle_id = best_fit_vehicle

        display_data_table.loc[0, 'Vehicle ID'] = 'Simulation Average'
        display_data_table.loc[1, 'Vehicle ID'] = vehicle_id

        display_data_table.loc[0, 'Distance (miles)'] = summary_df.loc['Total_average', ('distance', 'total')]
        display_data_table.loc[1, 'Distance (miles)'] = summary_df.loc[vehicle_id, ('distance', 'total')]

        display_data_table.loc[0, 'Time in Network'] = summary_df.loc['Total_average', ('norm_time', 'total')]
        display_data_table.loc[1, 'Time in Network'] = summary_df.loc[vehicle_id, ('norm_time', 'total')]

        display_data_table.loc[0, 'Fuel Economy (mpg)'] = summary_df.loc['Total_average', ('vehicle_fuel', 'mpg')]
        display_data_table.loc[1, 'Fuel Economy (mpg)'] = summary_df.loc[vehicle_id, ('vehicle_fuel', 'mpg')]

        # return dash_table.DataTable(
        #     id='dash-table',
        #     columns=[{"name": i, "id": i} for i in display_data_table.columns],
        #     data=display_data_table.to_dict('records'),
        # )
        return dbc.Table.from_dataframe(display_data_table, striped=True, bordered=True, hover=True)


    return html.Div([html_base])



if __name__ == "__main__":

    summary_df = pd.read_csv(os.path.join(APP_PATH, 'data', 'summary_df.csv'), header=[0, 1],
                             skipinitialspace=True,
                             )

    summary_df.set_index(summary_df.iloc[:,0], inplace=True)
    trace_visualisation.sampled_emissions_df = pd.read_csv(os.path.join(APP_PATH, 'data', 'sampled_emissions.csv'))

    html_div = get_app(
                           sampled_vehicle_ids=trace_visualisation.sampled_emissions_df['vehicle_id'].unique(),
                           best_fit_vehicle='480_8.2',
                           trace_visual=trace_visualisation.trace_visual,
                           summary_df=summary_df)

    app.layout = html_div
    app.run_server(debug=True)