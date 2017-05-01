###########################################
# This script is the evolutionary script  #
# of the orginal static code developed    #
#  in early versions.                     #
##########################################

def get_hist():
    from pymongo import MongoClient
    client = MongoClient('mongodb://dor:Abbie321@83.212.82.156:27017/HistData')
    #client = MongoClient('mongodb://localhost:27017//HistData')
    #client = MongoClient('mongodb://localhost:27017/rentalData')
    db = client.HistDatauser
    return db

def control(year,postcode):
    ## This function acts as control function for the script
    DH1(year,'Dublin '+str(postcode))
    DH2(year,'Dublin '+str(postcode))
    DH3(year,str(postcode))
    DH4(year,str(postcode))
    DH5(year,str(postcode))
    DH6(str(postcode))
def DH1(year,Postcode): # Needs to be Dublin + postcode
    # Used to identify year and gather information regarding that year. Create Graph
    import plotly.plotly as py
    import plotly.graph_objs as go
    import plotly
    import pandas as pd
    db = get_hist()
    py.sign_in('deanoreilly990', 'WgnPSOLqPlZ5uXFu6WKx')
    data = db.PPRC1.find({},{'_id':0})
    Table = 0
    if year == 2016:
        Table = db.Data2016.find()
    elif year == 2015:
        Table = db.Data2015.find()
    elif year == 2014:
        Table = db.Data2014.find()
    elif year == 2013:
        Table = db.Data2013.find()
    elif year == 2012:
        Table = db.Data2012.find()
    elif year == 2011:
        Table = db.Data2011.find()
    elif year == 2010:
        Table = db.Data2010.find()
    Table = pd.DataFrame(list(Table))
    data = pd.DataFrame(list(data))
    data = data[data['Postcode']==Postcode]
    data['Date']=pd.to_datetime(data['Date'])
    format = lambda x: x/ 100
    f = lambda x:float(x)
    str1 = str(year)+"-01-01"
    str2 =str(year)+"-12-31"
    data=data[data["Date"].isin(pd.date_range(str1, str2))]
    data =data[['Postcode','Price','Date']]
    data['Price']=data['Price'].apply(format)
    data['Price']=data['Price'].apply(f)
    info = Table.loc[Table['PostCode'] ==Postcode]
    try:
            mean =list(info['Mean'])
            mean =mean[0]
            mean =mean.encode('ascii','ignore')
            mean = mean.strip()
            mean = mean.replace(',','')
            mean = float(mean)
    except:
        pass
    meanlist=[]
    for j in range(0,data['Price'].count()):
            meanlist.append(mean)
    trace = go.Scatter(
        y=data['Price'],
        x=data['Date'],
        mode='markers',
        name='House price')
    trace0 = go.Scatter(
        y=meanlist,
        x=data['Date'],
        mode='lines',
        name='Mean')
    layout = go.Layout(
        title='Including Outliers ',
        autosize=False,
        width=500,
        height=500,
        xaxis=dict(
            title='Date',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='House Price',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )

    )
    data = [trace, trace0]
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig,filename='/home/user/FlaskApp/App/static/images/history/H1.html',show_link=False,auto_open=False)


def testpath(filename):
    ## Used in testing
    import os.path
    path = filename
    exist = os.path.exists(path)
    return exist



def DH2(year, Postcode): #Dublin + Postcode
    import plotly.plotly as py
    import plotly.graph_objs as go
    import plotly
    import pandas as pd
    db = get_hist()
    py.sign_in('deanoreilly990', 'WgnPSOLqPlZ5uXFu6WKx')
    data = db.PPRC1.find({},{'_id':0})
    if year == 2016:
        Table = db.Data2016.find()
    elif year == 2015:
        Table = db.Data2015.find()
    elif year == 2014:
        Table = db.Data2014.find()
    elif year == 2013:
        Table = db.Data2013.find()
    elif year == 2012:
        Table = db.Data2012.find()
    elif year == 2011:
        Table = db.Data2011.find()
    elif year == 2010:
        Table = db.Data2010.find()
    Table = pd.DataFrame(list(Table))
    data = pd.DataFrame(list(data))
    data = data[data['Postcode'] == Postcode]
    data['Date']=pd.to_datetime(data['Date'])
    format = lambda x: x/ 100
    f = lambda x: '{:20,.2f}'.format(x)
    str1 = str(year)+"-01-01"
    str2 =str(year)+"-12-31"
    data=data[data["Date"].isin(pd.date_range(str1, str2))]
    data =data[['Postcode','Price','Date']]
    data['Price']=data['Price'].apply(format)
    info = Table.loc[Table['PostCode'] == Postcode]
    price = []
    date = []
    line = []
    for index,row in info.iterrows():
        mean = row['New Mean']
        upper = row['UpperMV']
        lower = row['LowerMV']
    for index,row in data.iterrows():
        priceVal = row['Price']
        if priceVal <= upper:
            if priceVal > lower:
                price.append(priceVal)
                date.append(row['Date'])
            else:
                priceVal = lower
                price.append(priceVal)
                date.append(row['Date'])
        else:
            priceVal = upper
            price.append(priceVal)
            date.append(row['Date'])
        line.append(mean)

    trace = go.Scatter(
        y = price,
        x = date,
        mode = 'markers',
        name = 'House price')
    trace0 = go.Scatter(
        y = line,
        x = data['Date'],
        mode = 'lines',
        name = 'Mean')
    layout = go.Layout(
        title='Excluding Outliers',
        xaxis=dict(
            title='Date',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='House Price',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        autosize=False,
        width=500,
        height=500,
    )
    data = [trace,trace0]
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='/home/user/FlaskApp/App/static/images/history/H2.html', show_link=False,auto_open=False)




def DH3(year,Postcode):#just PC

    import pandas as pd
    import plotly.plotly as py
    import plotly.graph_objs as go
    import plotly
    py.sign_in('deanoreilly990', 'WgnPSOLqPlZ5uXFu6WKx')
    db = get_hist()
    crimed = db.Crime.find({}, {'_id': 0})
    crimed = pd.DataFrame(list(crimed))
    crimed = crimed[[str(year), 'Crime', 'Postcode']]
    crime = ['03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '15']
    postcodes = crimed['Postcode'].unique()
    crimesI = crimed['Crime'].unique()
    f = lambda x: x / len(postcodes)
    means = []
    for i in crimesI:
        datac = crimed[crimed['Crime'] == i]
        means.append(datac[str(year)].sum())
    means = map(f, means)
    crimes = ['03:Attemps/Treats of Murder/Assault/Harressment', '04:Dangerous/Negligent', '05:Kidnapping',
              '06:Robbery,extortion& hijacking', '07:Burglary', '08:Theft', '09:Fraud', '10:Controlled Drug',
              '11:Weapons& Explosives'
              '12:Damage to Property', '13:Public Order', '15:Offences against Government']
    if Postcode == 'SCD':
        Postcode = '24'
    data = crimed[crimed['Postcode'] == Postcode]
    data = data[[str(year), 'Crime']]
    count = []
    for i in crimesI:
        datac = data[data['Crime'] == i]
        count.append(datac[str(year)].sum())
    trace0 = go.Bar(
        y=count,
        x=crime,
        name='Crimes Commited',
        text=crimes,
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity=0.6
    )
    trace1 = go.Scatter(
        y=means,
        x=crime,
        mode='markers+lines',
        name='Average Rate of Crime',
        line=dict(
            color='red'
        )
    )
    data = [trace0, trace1]
    layout = go.Layout(
        legend=dict(
            orientation="h")
    ,
        title='Crimes in Dublin:' + str(Postcode),
        autosize=False,
        width=500,
        height=450,
        margin=go.Margin(
            l=45,
            r=10,
            b=100,
            t=50,
            pad=4
        ),
        yaxis=dict(
            title='No. Of Instances',
        ),
        xaxis=dict(
            title='Crimes', )
    )
    fig = dict(data=data, layout=layout)
    plotly.offline.plot(fig,filename='/home/user/FlaskApp/App/static/images/history/H3.html',show_link=False,auto_open=False)









def DH4(year,Postcode):# Postcode String
    import pandas as pd

    import plotly.plotly as py
    import plotly.graph_objs as go
    import plotly
    py.sign_in('deanoreilly990', 'WgnPSOLqPlZ5uXFu6WKx')
    db = get_hist()
    welfare = db.SocialData.find({}, {'_id': 0})
    welfare = pd.DataFrame(list(welfare))
    pc = welfare['Postcode'].unique()
    DC = welfare[welfare['Location'] == 'Dublin County']
    x = Postcode
    if x == '1' or x == '3' or x == '4':
        x = '2'
    elif x == '12':
        x = '8'
    elif x == '13':
        x = '5'
    elif x == '16':
        x = '14'
    elif x == '18':
        x = 'Dun Laoghaire Rathdown'
    elif x == '20':
        x = '10'
    elif x == '6w':
        x = '6'
    Postcode = x
    welfare = welfare[welfare['Postcode'] == Postcode]
    signon = []
    Average = []
    for row in welfare:
        if str(year) in row:
            Average.append(DC[row].sum())
            signon.append(welfare[row].sum())
    f = lambda x: x.encode('ascii', 'ignore')
    flo = lambda x: int(x)
    av = lambda x: x / len(pc) - 1
    try:
        signon = map(f, signon)
        Average = map(f, Average)
    except:
        pass
    signon = map(flo, signon)
    Average = map(flo, Average)
    Average = map(av, Average)
    trace0 = go.Scatter(
        y=signon,
        x=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
        name='Area',
        line=dict(
            color='blue'
        ),
    )
    trace1 = go.Scatter(
        y=Average,
        x=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
        name='Average',
        line=dict(
            color='red'
        ),
    )
    data = [trace0, trace1]
    layout = go.Layout(
        legend=dict(
            orientation="h")
        ,
        title='Welfare Sign On Per Month',
        autosize=False,
        width=500,
        height=400,
        margin=go.Margin(
            l=50,
            r=10,
            b=50,
            t=50,
            pad=4
        ),
        xaxis=dict(
            title='Months',
        ),
        yaxis=dict(
            title='No.Sign on',
        )
    )
    fig = dict(data=data, layout=layout)
    plotly.offline.plot(fig,filename='/home/user/FlaskApp/App/static/images/history/H4.html',show_link=False,auto_open=False)








def DH5(year,Postcode):#Postcode as string
    import pandas as pd

    db = get_hist()
    data = db.construction.find({}, {'_id': 0})
    data = pd.DataFrame(list(data))
    fingal = ['11', '13', '15', '17', 'NCD']
    DC = ['1', '3', '7', '8', '9', '2', '10']
    SD = ['12', '20', '22', '24', '6w', 'WCD']
    DLR = ['4', '6', '14', '16', '18', 'Dun Laoghaire Rathdown']
    location = Postcode
    if Postcode in fingal:
        location = 'Fingal'
    elif Postcode in SD:
        location = 'South Dublin'
    elif Postcode in DC:
        location = 'Dublin City'
    elif Postcode in DLR:
        location = 'DLR'
    data = data[data['Location'] == location]
    Condata = []
    for i in data.columns:
        if str(year) in i:
            if i == '2011M02':
                Condata.append(0)
            else:
                Condata.append(data[i].sum())
    import plotly.plotly as py
    import plotly.graph_objs as go
    import plotly
    py.sign_in('deanoreilly990', 'WgnPSOLqPlZ5uXFu6WKx')
    trace1 = go.Scatter(
        x=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        y=Condata
    )
    layout = go.Layout(
        title='Construction in ' + location,
        xaxis=dict(
            title='Month of year'),
        yaxis=dict(
            title='No.Constructions'),
        autosize=False,
        width=500,
        height=400,
        margin=go.Margin(
            l=40,
            r=10,
            b=50,
            t=50,
            pad=4
        )
    )
    data = [trace1]
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig,filename='/home/user/FlaskApp/App/static/images/history/H5.html',show_link=False,auto_open=False)










def DH6(Postcode):#string postcode
    import pandas as pd
    db = get_hist()
    data = db.population.find({},{'_id':0})
    data = pd.DataFrame(list(data))
    Ranges = data['Age '].unique()
    fingal = ['11','13','15','17','NCD']
    DC =['1','3','7','8','9','2','10']
    SD =['12','20','22','24','D6w','WCD']
    DLR =['4','6','14','16','18','Dun Laoghaire Rathdown']

    if Postcode in fingal:
        Postcode ='Fingal'
    if Postcode in DC:
        Postcode = 'Dublin City'
    if Postcode in SD:
         Postcode = 'South Dublin'
    if Postcode in DLR:
        Postcode = 'Dun Laoghaire-Rathdown'
    data = data[data['Location']==Postcode]
    Pop = []
    Ranges.sort()
    for i in Ranges:
        age = data[data['Age '] == i]
        Pop.append(age['Population 2011'].sum())
    import plotly.plotly as py
    import plotly.graph_objs as go
    import plotly

    py.sign_in('deanoreilly990', 'WgnPSOLqPlZ5uXFu6WKx')
    Ranges = ['0-4', '5-9', '10-14', '14-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59',
              '60-64', '65-69', '70-74', '75-79', '80-84', '85+']
    trace = go.Scatter(
        y=Pop,
        x=Ranges,
    )
    layout = {'title': 'Population and average age of buyers',
              'shapes': [{'type': 'line', 'x0': '30-34',
                          'x1': '30-34', 'y0': 0, 'y1': '25,066',
                          'line': {'color': 'red'}},
                         {'type': 'line', 'x0': '35-39',
                          'x1': '35-39', 'y0': 0, 'y1': '25,066', 'line': {'color': 'red'}}],
              'autosize': False,
              'width': 500,
              'height': 400,
              'margin': {'l': 50, 'r': 5, 'b': 70, 't': 50, 'pad': 4},
              'xaxis': {'title': 'Age Range'},
              'yaxis': {'title': 'Population'}
              }
    data = [trace]
    fig = dict(data=data, layout=layout)
    plotly.offline.plot(fig,filename='/home/user/FlaskApp/App/static/images/history/H6.html',show_link=False,auto_open=False)
