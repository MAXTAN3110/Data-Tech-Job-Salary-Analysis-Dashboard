import os
import pandas as pd
from dash import html
from dash.dependencies import Input, Output, State
from components.wordcloud import create_wordcloud
from components import pie_and_violin, heatmap, line_and_bar, treemap, scattergeo


def register_server_callbacks(app):
    @app.callback(
        Output("store", "data"),
        Input("_pages_location", "pathname"),
        State("store", "data"),
    )
    def get_data(pathname, data):
        if data is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(os.path.dirname(current_dir))
            file_path = os.path.join(root_dir, "processed_data.csv")
            df = pd.read_csv(file_path)
            return df.to_dict("records")
        return data

    @app.callback(Output("wordcloud_div", "children"), Input("store", "data"))
    def update_wordcloud(data):
        df = pd.DataFrame(data)

        return html.Div(
            create_wordcloud(["Data", "Engineer", "Scientist", "of"], df, "1")
        )

    @app.callback(Output("pie_violin_div", "children"), Input("store", "data"))
    def update_plot(data):
        df = pd.DataFrame(data)
        return html.Div(pie_and_violin.create_subplots(df, "1"))

    @app.callback(Output("heatmap_div", "children"), Input("store", "data"))
    def update_plot(data):
        df = pd.DataFrame(data)
        return html.Div(heatmap.create_heatmap(df))

    @app.callback(Output("line_bar_div", "children"), Input("store", "data"))
    def update_plot(data):
        df = pd.DataFrame(data)
        return html.Div(line_and_bar.create_linebarplot(df))

    @app.callback(Output("treemap_div", "children"), Input("store", "data"))
    def update_plot(data):
        df = pd.DataFrame(data)
        return html.Div(treemap.create_treemap(df))

    @app.callback(Output("scattergeo_div", "children"), Input("store", "data"))
    def update_plot(data):
        df = pd.DataFrame(data)
        return html.Div(scattergeo.create_scattergeo(df))
