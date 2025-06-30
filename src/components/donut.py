from dash import html
import json


def DonutChart(id, data, centerText):
    return html.Div(
        [
            html.Div(
                id=id,
                className="donut-graph",
                **{"data-props": json.dumps({"data": data, "centerText": centerText})}
            )
        ]
    )
