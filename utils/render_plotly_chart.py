import json
import plotly

def render_plotly_chart(file):

    start = json.dumps(file, cls=plotly.utils.PlotlyJSONEncoder)
    data = json.loads(start)['data']
    data_layout = json.loads(start)['layout']

    return data, data_layout