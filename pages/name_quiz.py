import dash
from dash import dcc, html, Input, Output, State,no_update, callback, clientside_callback
import dash_bootstrap_components as dbc
import re
import random
import pandas as pd


dash.register_page(__name__, name="Name Quiz", path="/name_quiz")

def random_pick(countries):
    # print(words)
    random_word = random.choice(countries)
    rnd_mask = re.sub(r".", "-", random_word)
    guessed_letters = set()
    return rnd_mask, random_word, guessed_letters


def word_screen(input_char, answer, masked_output):
    for i in range(len(answer)):
        if answer[i].lower() == input_char.lower():
            new_word = list(masked_output)
            new_word[i] = input_char.lower()
            masked_output = "".join(new_word)
    return masked_output


# sample = list(countries.keys())

layout = dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.H1("Word Guess")
                    ], className='d-flex justify-content-center text-align-center', id="title"),
                    html.Div([
                        html.Div([
                            html.Label("Country:",
                                       style={'fontSize': '18px', 'marginRight': '5px', 'fontWeight': 'bold', 'display': 'inline-block'}),
                            html.Div([
                                html.Div([
                                html.Span(id="expected_word"),
                                html.Span(id="capital"),
                                    ], id="result1"),
                                html.Div([
                                    html.Img(id="cflag", style={"width": "100px", "height": "70px"})
                                ], id="country_flag"),
                            ],id="result_flag"),

                            html.Hr(style={"width": "100% !important", }),
                            html.Span(id="min_expected_guess"),
                            html.Span(id="guessed_letters"),
                            html.Span(id="num_of_attempts"),

                        ], id="info_div"),
                        html.Hr(),
                        html.Label("Guess a letter:", style={'fontSize': '18px'}),
                        dcc.Input(
                            id="user_input",
                            type="text",
                            # placeholder="Guess a word",
                            style={'margin': '10px'},
                            maxLength=1,
                            pattern=".{1,1}",
                        ),
                    ])
                ], id="input_div")
            ], xs=12, sm=12, md=12, lg=12, xl=12,
                className="mx-auto"
            ),
            dcc.Store("new_interaction", data=True),
            dcc.Store("store_content", data=None),
            dcc.Store(id="store_plain_random_output"),
            dcc.Store(id="store_masked_random_output"),
            dcc.Store(id="store_guessed_letters", data=[]),
            dcc.Store(id="match_found", data=False),
            dcc.Store(id="store_num_of_attempts", data=0),
        ], justify="center", className='g-0 nq')
pattern = re.compile(r"^[a-zA-Z\s.]+$")
@callback(
    Output("expected_word", "children"),
    Output("new_interaction", "data"),
    Output("store_masked_random_output", "data"),
    Output("store_plain_random_output", "data"),
    Output("store_guessed_letters", "data"),
    Output("match_found", "data"),
    Output("min_expected_guess", "children"),
    Output("guessed_letters", "children"),
    Output("num_of_attempts", "children"),
    Output("store_num_of_attempts", "data"),
    Output("result1", "style"),
    Output("capital", "children"),
    Output("cflag", "src"),
    Output("cflag", "style"),
    Input("user_input", "value"),
    [State("new_interaction", "data"),
     State("store_masked_random_output", "data"),
     State("store_plain_random_output", "data"),
     State("store_guessed_letters", "data"),
     State("match_found", "data"),
     State("store_num_of_attempts", "data"),
     State("df", "data")],
)
def display_result(user_input, new_interaction, store_masked_output, store_plain_output, store_guessed_letters,
                   match_found, num, df):
    countries_info = pd.DataFrame(df)
    if new_interaction and not match_found:
        num = 0
        masked_random_output, plain_random_output,  guessed_letters = random_pick(countries_info["Country"].values)
        print(plain_random_output)
        return (masked_random_output, False, masked_random_output, plain_random_output, list(guessed_letters), False,
                html.P(["Minimum expected guesses: ",
                        html.Span(len(set(plain_random_output.strip().lower())), className="min-attempts shared-span-style")]),
                html.P(["Already guessed: ",
                        html.Span(None, className="guessed_letters shared-span-style")]),
                html.P(["Attempts: ", html.Span(str(0), className="attempts shared-span-style")]),
                num,
                {'backgroundColor': '#f0f0f0', 'color': 'black',
                 'boxShadow': 'box-shadow: 5px 10px 5px rgba(0, 0, 0, 0.2)'},
                "", "",
                {"width": "0", "height": "0"},
                )

    else:
        if pattern.match(user_input):
            num += 1
            print(store_masked_output)
            store_guessed_letters.append(user_input)
            unique_guesses = set(store_guessed_letters)
            guess_outcome = word_screen(user_input, store_plain_output, store_masked_output)
            print(guess_outcome)
            if guess_outcome.lower() == store_plain_output.lower():
                country_capital = countries_info.loc[countries_info["Country"] == store_plain_output]["Capital"]
                # print("match found!")
                # print(store_plain_output)
                # print(countries[store_plain_output])
                return (store_plain_output, True, guess_outcome, store_plain_output, store_guessed_letters, False,
                        html.P(["Minimum expected guesses: ",
                                html.Span(len(set(store_plain_output.strip().lower())),
                                          className="min-attempts shared-span-style")]),
                        html.P(["Already guessed: ",
                                html.Span(",".join(unique_guesses), className="guessed_letters shared-span-style")]),
                        html.P(["Attempts: ", html.Span(str(num), className="attempts shared-span-style")]),
                        num,
                        {'backgroundColor': 'green', 'color': 'white', 'boxShadow': '5px 10px 5px rgba(0, 0, 0, 0.4)',
                         'border': '2px solid white'},
                        country_capital,
                        # countries[store_plain_output],
                        f"/assets/flags/{store_plain_output}.jpg",
                        {"width": "100px", "height": "70px"},
                        )

            return (guess_outcome, False, guess_outcome,  store_plain_output, store_guessed_letters, False,html.P(["Minimum expected guesses: ",
                            html.Span(len(set(store_plain_output.strip().lower())), className="min-attempts shared-span-style")]),
                    html.P(["Already guessed: ",
                            html.Span(",".join(unique_guesses), className="guessed_letters shared-span-style")]),
                    html.P(["Attempts: ", html.Span(str(num), className="attempts shared-span-style")]),
                    num,
                    {'backgroundColor': '#f0f0f0', 'color': 'black',
                     'boxShadow': 'box-shadow: 5px 10px 5px rgba(0, 0, 0, 0.2)'},
                    "", "",
                    {"width": "0", "height": "0"},
                    )
        else:
            return (store_masked_output, False, store_masked_output, store_plain_output, store_guessed_letters, False,
                    html.P(["Minimum expected guesses: ",
                            html.Span(len(set(store_plain_output.strip().lower())),
                                      className="min-attempts shared-span-style")]),
                    html.P(["Already guessed: ",
                            html.Span(",".join(set(store_guessed_letters)), className="guessed_letters shared-span-style")]),
                    html.P(["Attempts: ", html.Span(str(num), className="attempts shared-span-style")]),
                    num,
                    {'backgroundColor': '#f0f0f0', 'color': 'black',
                     'boxShadow': 'box-shadow: 5px 10px 5px rgba(0, 0, 0, 0.2)'},
                    "", "",
                    {"width": "0", "height": "0"},
                    )


clientside_callback(
    """
    function(value) {
        var inputElem = document.getElementById('user_input');
        if (inputElem) {
            inputElem.focus();
            inputElem.select();
        }
        return value;
    }
    """,
    Output("store_content", "data"),
    Input("user_input", "value")
)
