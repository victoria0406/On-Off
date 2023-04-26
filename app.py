import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__, use_pages=True)


app.layout = html.Div([
    html.H2('OnOff'),
    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),

	dash.page_container
],
style={
}
)

if __name__ == '__main__':
    app.run_server(debug=True)