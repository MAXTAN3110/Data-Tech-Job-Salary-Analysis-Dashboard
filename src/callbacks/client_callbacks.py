from dash.dependencies import Input, Output


def register_client_callbacks(app):
    app.clientside_callback(
        """
    function(trigger) {
        // Use getElementById instead of querySelectorAll
        const el = document.getElementById('my-donut-graph');
        if (el && !el.hasChildNodes() && window.dashComponents && window.dashComponents.DonutChart) {
            const props = JSON.parse(el.getAttribute('data-props'));
            const graphEl = window.dashComponents.DonutChart(props);
            el.appendChild(graphEl);
        }
        return window.dash_clientside.no_update;
    }
    """,
        Output("my-donut-graph", "children"),
        Input("my-donut-graph", "id"),  # Triggers on component mount
    )
