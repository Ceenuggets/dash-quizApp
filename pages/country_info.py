import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import random
import pandas as pd
# from .data import countries
# from .countries_data import countries_info

# sample = list(countries.keys())
# capitals = list(countries.values())

"======== Generate country and options ============="


def question_and_options(country_and_cap):
    all_countries = country_and_cap["Country"].values
    all_capitals = country_and_cap["Capital"].values
    # print(all_capitals)
    m = 0
    options = []
    question = random.choice(all_countries)
    answer = country_and_cap.loc[country_and_cap["Country"] == question]["Capital"].iloc[0]
    # print(f" Answers is: {answer}")
    # answer = countries[question]
    options.append(answer)
    while m < 3:
        incorrect_option = random.choice(all_capitals)
        # print(incorrect_option)
        if (incorrect_option.strip().lower() != answer.strip().lower()) and (incorrect_option not in options):
            options.append(incorrect_option)
            m += 1
    random.shuffle(options)
    return question, options, answer


"==================================================="

dash.register_page(__name__, name="Capital Quiz", path="/country_info")

# print(countries_info)
layout = dbc.Row([
    dbc.Col([
        html.Div([
            html.Div([
                html.H5("Capital Challenge")
            ], className='d-flex justify-content-center text-align-center p-0', id="title"),
            html.Div([
                html.Div([
                    html.Div([
                        html.H4(id="question"),
                        html.Button("Next", id="btn_next")
                    ], id="question_div"),
                    html.Div([
                        dcc.RadioItems(id="rd_capitals")
                    ], id="options_div"),
                ], id="question_options_div"),
                html.Div([
                     html.Div([

                    ], id="country_table"),
                    html.Div([
                        html.Div([
                            html.Img(id="country_img")
                        ], id="flag_img_div"),
                        html.Div([

                        ], id="indpndnc_date")
                    ], id="country_more_info"),
                     
                ], id="country_table_and_flag"),
                html.Div([

                ], id="city_div")
            ])
        ], id="div_parent")
    ], xs=12, sm=12, md=12, lg=12, xl=12),
    dcc.Store(id="right_answer", data=None),
], justify="center", className="g-0 ci")


@callback(
    Output("question", "children"),
    Output("rd_capitals", "options"),
    Output("right_answer", "data"),
    Output("country_table", "children"),
    Output("country_img", "src"),
    Output("country_img", "style"),
    Output("indpndnc_date", "children"),
    Output("city_div", "children"),
    Input("btn_next", "n_clicks"),
    State("df", "data"),


)
def display_question(n_clicks, df):
    country_record = pd.DataFrame(df)
    countries_and_capitals = country_record[["Country", "Capital"]]
    # print(countries_and_capitals)
    if n_clicks:
        question, choices, right_answer = question_and_options(countries_and_capitals)
        options = [{"label": choice, "value": choice} for choice in choices]
        country_and_capital = {"Country": question, "Capital": right_answer}
        return question, options, country_and_capital, "", "", {"width": "0", "height": "0"}, "", ""
    else:
        # print(countries_and_capitals)
        question, choices, right_answer = question_and_options(countries_and_capitals)
        options = [{"label": choice, "value": choice} for choice in choices]
        country_and_capital = {"Country": question, "Capital": right_answer}
        return question, options, country_and_capital, "", "", {"width": "0", "height": "0"}, "", ""


@callback(
    Output("rd_capitals", "options", allow_duplicate=True),
    Output("country_table", "children", allow_duplicate=True),
    Output("country_img", "src", allow_duplicate=True),
    Output("country_img", "style", allow_duplicate=True),
    Output("indpndnc_date", "children", allow_duplicate=True),
    Output("city_div", "children", allow_duplicate=True),
    [Input("rd_capitals", "value"),
     State("rd_capitals", "options"),
     State("right_answer", "data")],
    State("df", "data"),
    prevent_initial_call=True
)
def check_answers(select_capital, options, solution, df):
    country_record = pd.DataFrame(df)
    table_body = []
    table_div = ""
    govt_type = ""
    date_of_independence = ""
    # pop_cities = ""
    caption_pop_cities = ""
    updated_options = []
    flag_src = ""
    flag_styl = {"width": "0", "height": "0"}

    if select_capital and solution:
        for option in options:
            label = option["label"]
            value = option["value"]
            if value != solution["Capital"] and value == select_capital:
                if "❌" not in label:
                    label += " ❌ "
            elif value == solution["Capital"] and value == select_capital:
                if "✅" not in label:
                    label += " ✅ "

                right_answer_details = country_record.loc[country_record["Country"] == solution["Country"]]
                cap = right_answer_details["Capital"].iloc[0]
                continent = right_answer_details["Continent"].iloc[0]
                langauges = right_answer_details["Languages"].iloc[0]
                currency = right_answer_details["Currency"].iloc[0]
                time_zones = right_answer_details["TimeZones"].iloc[0]
                gmt_offsets = right_answer_details["GMTOffSets"].iloc[0]
                govt_types = right_answer_details["GovernmentTypes"].iloc[0]
                motto = right_answer_details["Motto"].iloc[0]
                table_rows = [
                    html.Tr(
                        [html.Td("Continent:", className="cell_title"), html.Td(continent)]),
                    html.Tr([html.Td("Capital:", className="cell_title"), html.Td(cap)]),
                    html.Tr([html.Td("Language:", className="cell_title"),
                             html.Td(langauges)]),
                    html.Tr([html.Td("Currency:", className="cell_title"), html.Td(currency)]),
                    html.Tr([html.Td("Time Zone:", className="cell_title"),
                             html.Td(time_zones)]),
                    html.Tr([html.Td("GMT Offset:", className="cell_title"),
                             html.Td(gmt_offsets.replace("'", ""))]),
                    html.Tr([html.Td("Govt. Type:", className="cell_title"),
                             html.Td(govt_types.capitalize())]),
                    html.Tr([html.Td("Motto:", className="cell_title"), html.Td(motto)]),
                ]
                for row in table_rows:
                    table_body.append(row)
                table_div = html.Div([
                    html.Table([
                        html.Tbody(table_body)
                    ])
                ])
                flag_src = f"/assets/flags/{solution['Country']}.jpg"
                indpndce_date = right_answer_details["IndependenceDate"].iloc[0]

                date_of_independence = html.Div([
                    html.Div("Independence", id="indp_div"),
                    html.Div(indpndce_date, id="indp_date"),
                ], className="img_date_container")

                cities = right_answer_details["Cities"].iloc[0]
                # print(cities)
                pop_cities = html.Div(
                    [html.Div(city, className="pop_city") for city in cities.split(",")]
                    , id="cities_container")

                caption_pop_cities = html.Div([
                    html.Div("Some Cities:", id="caption"),
                    pop_cities
                ], id="caption_pop_cities")
                # pop_cities = [html.Div(city, className="pop_city") for city in cities]
                flag_styl = {"width": "200px", "height": "auto"}

            updated_options.append({'label': label, 'value': option['value']})

        return updated_options, table_div, flag_src, flag_styl, date_of_independence, caption_pop_cities

    return updated_options, table_div, flag_src, flag_styl, date_of_independence, caption_pop_cities





