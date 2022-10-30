from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chart1')
def chart1():
    df_stocks = px.data.stocks()
    px.line(df_stocks, x='date', y='GOOG', labels={'x':'Date', 'y':'Price'})

    px.line(df_stocks, x='date', y=['GOOG','AAPL'], labels={'x':'Date','y':'Price'}, title='Apple Vs Google' )

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_stocks.date, y=df_stocks.AAPL, mode='lines', name='Apple'))
    fig.add_trace(go.Scatter(x=df_stocks.date, y=df_stocks.AMZN, mode='lines+markers', name='Amazon', line_shape = 'hvh'))
    fig.add_trace(go.Scatter(x=df_stocks.date, y=df_stocks.GOOG, mode='lines+markers', name='Google', line=dict(color='firebrick', width=2, dash='dashdot')))

    #fig.update_layout(title= "Stock price for year 2018 to 2020",
    ##                 xaxis_title='Share graph', yaxis_title='Price in US$')

    fig.update_layout(
    xaxis=dict(showline=True, showgrid=False, showticklabels=True, 
               linecolor='rgb(204,204,204)', 
               linewidth=2, ticks='outside', 
               tickfont=dict(family='Arial', size=12, color='rgb(82,82,82)')),
    yaxis=dict(showgrid=False, zeroline=False, showline=True, showticklabels=False), autosize=False,
    width=1600,
    height=600,
    margin=dict(autoexpand=False, l=100, r=20, t=110), showlegend=False, plot_bgcolor='light green')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Stock price comparison line graph"
    description = """
    The graph shows Amazon, Apple and Google stock prize comparison.
    """
    return render_template('notdash2.html', graphJSON=graphJSON, header=header,description=description)

@app.route('/chart2')
def chart2():
    df_us = px.data.gapminder().query("country == 'United States'")
    px.bar(df_us, x='year', y='pop')

    df_tips = px.data.tips()
    px.bar(df_tips, x='day', y='tip', color='sex',
           title ='Tips by Sex on Each day',
           labels={'tip':'Tip Amount', 'day':'Day of the week'})

    px.bar(df_tips, x='sex', y='total_bill', color='smoker', barmode='group')

    df_europe = px.data.gapminder().query("continent=='Europe' and year==2007 and pop>2.e6")
    fig = px.bar(df_europe, x='country', y='pop', text='pop', color='country')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(width=1600, height=600)
    fig.update_layout(uniformtext_minsize=20)
    fig.update_layout(xaxis_tickangle=-45)
    fig


    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Country population bar graph"
    description = """
    The rumor that vegetarians are having a hard time in London and Madrid can probably not be
    explained by this chart.
    """
    return render_template('notdash2.html', graphJSON=graphJSON, header=header,description=description)


@app.route('/chart3')
def chart3():
    df_tips=px.data.tips()
    px.box(df_tips, x='sex', y='tip', color='day', points='all')

    px.box(df_tips, x='day', y='tip', color='sex')

    fig=go.Figure()
    fig.add_trace(go.Box(x=df_tips.sex, y=df_tips.tip, marker_color='blue',boxmean='sd'))

    df_stocks = px.data.stocks()
    fig=go.Figure()
    fig.add_trace(go.Box(y=df_stocks.GOOG, boxpoints='all',
                        fillcolor='blue',jitter=0.5, whiskerwidth=0.2))
    fig.add_trace(go.Box(y=df_stocks.AAPL, boxpoints='all',
                        fillcolor='red',jitter=0.5, whiskerwidth=0.2))
    fig.update_layout(title='Google vs. Apple', 
                    yaxis=dict(gridcolor='rgb(255,255,255)',
                            gridwidth=3),
                    paper_bgcolor='rgb(243,243,243)',
                    plot_bgcolor='rgb(243,243,243)',width=1600, height=600)


    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Tips Box plot"
    description = """
    This graph shows analysis of tips given by customers
    """
    return render_template('notdash2.html', graphJSON=graphJSON, header=header,description=description)


@app.route('/chart4')
def chart4():
    df_tips=px.data.tips()
    px.violin(df_tips, y='total_bill', box=True, points='all')

    px.violin(df_tips, y='tip', x='smoker',color='sex', box=True, points='all', hover_data=df_tips.columns)

    fig = go.Figure()
    fig.add_trace(go.Violin(x=df_tips['day'][df_tips['smoker']=='Yes'],
                        y=df_tips['total_bill'][df_tips['smoker']=='Yes'],
                        legendgroup='Yes', scalegroup='Yes', name='Yes',side='negative', line_color='blue'))
    fig.add_trace(go.Violin(x=df_tips['day'][df_tips['smoker']=='No'],
                        y=df_tips['total_bill'][df_tips['smoker']=='No'],
                        legendgroup='Yes', scalegroup='Yes', name='No',side='positive', line_color='red'))
    fig.update_layout(width=1600, height=600)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Tips Box plot"
    description = """
    This graph shows analysis of tips given by customers
    """
    return render_template('notdash2.html', graphJSON=graphJSON, header=header,description=description)


@app.route('/chart5')
def chart5():
    flights = sns.load_dataset('flights')
    fig = px.scatter_3d(flights, x='year', y='month', z='passengers', color='year', opacity=0.7, animation_frame="year")
    fig
    fig.update_layout(width=1600, height=900)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="3D Plot"
    description = """
    This graph shows analysis of tips given by customers
    """
    return render_template('notdash2.html', graphJSON=graphJSON, header=header,description=description)


@app.route('/chart6')
def chart6():
    df_wind = px.data.wind()
    fig = px.line_polar(df_wind, r = 'frequency', theta='direction', color='strength', line_close=True, template="ggplot2")
    fig
    fig.update_layout(width=1600, height=900)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Polar Graph"
    description = """
    This graph shows analysis of tips given by customers
    """
    return render_template('notdash2.html', graphJSON=graphJSON, header=header,description=description)


@app.route('/chart7')
def chart7():
    fig = go.Figure()
    
    fig.add_trace(go.Indicator(
    value = 200,
    delta = {'reference': 160},
    gauge = {'axis': {'visible': False}},
    domain = {'row': 0, 'column': 0}))
    
    fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = 300,
    domain = {'row': 0, 'column': 1}))
    
    fig.add_trace(go.Indicator(
    mode = "delta",
    value = 40,
    domain = {'row': 4, 'column': 0}))

    fig
    fig.update_layout(
    grid = {'rows': 4, 'columns': 2, 'pattern': "independent"},
    template = {'data' : {'indicator': [{
        'title': {'text': "Speed"},
        'mode' : "number+delta+gauge",
        'delta' : {'reference': 90}}]
                         }})
    fig.update_layout(width=1000, height=800)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Indicators"
    description = """
    This graph shows analysis of tips given by customers
    """
    return render_template('notdash2.html', graphJSON=graphJSON, header=header,description=description)

if __name__ == "__main__":
    app.run(debug=True)


    