def get_hist():
    from pymongo import MongoClient
    client = MongoClient('mongodb://dor:Abbie321@83.212.82.156:27017/HistData')
    db = client.HistData
    return db
def get_db():
    from pymongo import MongoClient
    client = MongoClient('mongodb://dor:Abbie321@83.212.82.156:27017/rentalData')
    db = client.rentalData
    return db
def home1():
    import pandas as pd
    from pymongo import MongoClient
    def getdate():
        import datetime
        Months = {
            'Jan': 1,
            'Feb': 2,
            'Mar': 3,
            'Apr': 4,
            'May': 5,
            'Jun': 6,
            'Jul': 7,
            'Aug': 8,
            'Sep': 9,
            'Oct': 10,
            'Nov': 11,
            'Dec': 12
        }
        month = datetime.datetime.now()
        month = month.strftime("%b")
        date = Months[month]
        date = date
        begindate = 2
        collect = []
        for i in range(begindate, date):
            if i == 2:
                enddate = "-28"
            elif i in [4, 6, 11, 9]:
                enddate = "-30"
            else:
                enddate = "-31"
            collect.append([i, enddate])
        return collect
    dbH= get_hist()
    dbC = get_db()
    data2016 = dbH.new2016.find({},{'_id':0})
    data2016 = pd.DataFrame(list(data2016))
    datasale = dbC.sale.find({},{'_id':0})
    datasale = pd.DataFrame(list(datasale))
    datasale = datasale.dropna()
    date=getdate()
    datasale['Date Entered']=pd.to_datetime(datasale['Date Entered'])
    averageprice =[]
    averageprice.append(455940)
    for i in date:
        str1 = '2017-'+str(i[0])+'-01'
        str2 = '2017-'+str(i[0])+str(i[1])
        datas = datasale[datasale["Date Entered"].isin(pd.date_range(str1,str2))]
        price = datas['Price']
        sumi =0
        for j in price:
            sumi= sumi + int(j.encode('ascii','ignore'))
        sumi = sumi/len(price)
        averageprice.append(sumi)
    def getM():
        import datetime
        Months = {
            'Jan': 1,
            'Feb': 2,
            'Mar': 3,
            'Apr': 4,
            'May': 5,
            'Jun': 6,
            'Jul': 7,
            'Aug': 8,
            'Sep': 9,
            'Oct': 10,
            'Nov': 11,
            'Dec': 12
        }
        month = datetime.datetime.now()
        month = month.strftime("%b")
        date = Months[month]
        date = date - 1
        return date
    month= getM()
    histaverage=[]
    for i in range(month,13):
        if i == 2:
            enddate = "-28"
        elif i in [4, 6, 11, 9]:
            enddate = "-30"
        else:
            enddate = "-31"
        str1 = '2016-'+str(i)+'-01'
        str2 = '2016-'+str(i)+str(enddate)
        datad = data2016[data2016["Date"].isin(pd.date_range(str1,str2))]
        price = datad['Price']
        sumi =0
        for j in price:
            sumi= sumi + float(j)
        sumi = sumi/len(price)
        histaverage.append(sumi)
    average = histaverage + averageprice
    Months = {
             1:'Jan',
             2:'Feb',
             3:'Mar',
             4:'Apr',
             5:'May',
             6:'Jun',
             7:'Jul',
             8:'Aug',
             9:'Sep',
             10:'Oct',
             11:'Nov',
             12:'Dec'
        }
    months = []
    for i in range(month,13):
        date = Months[i]
        months.append(date)
    for i in range(1,month+1):
        date = Months[i]
        months.append(date + str(-2017))
    import plotly.plotly as py
    import plotly.graph_objs as go
    import plotly
    py.sign_in('deanoreilly990', 'WgnPSOLqPlZ5uXFu6WKx')
    trace0 = go.Scatter(
        x = months,
        y = average,
        name = 'Average Price'
    )

    data = [trace0]
    layout = go.Layout(
        title='Average House price Per Month',
        yaxis=dict(
            title='Value'),
        xaxis=dict(
            title='Month'),
        autosize=False,
        width=900,
        height=400,
        margin=go.Margin(
            l=80,
            r=10,
            b=50,
            t=50,
            pad=10
        ),
    )
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='/home/user/FlaskApp/App/static/images/History/home1.html',show_link=False,auto_open=False)
def home2():
    import pandas as pd
    returnd =[]
    db = get_hist()
    data = db.Crime.find({},{'_id':0})
    data = pd.DataFrame(list(data))
    columns = data.columns
    crimecol = []
    crimecol.append(columns[5])
    crimecol.append(columns[6])
    crimecol.append(columns[7])
    data = data[[crimecol[0],crimecol[1],crimecol[2]]]
    crimes = data['Crime'].unique()
    for i in crimes:
        datad = data[data['Crime']==i]
        d2015 = datad[crimecol[0]].sum()
        d2016 = datad[crimecol[1]].sum()
        if d2015 < d2016:
            returnd.append('Up')
        else:
            returnd.append('Down')
    return returnd
def home3():
    import pandas as pd
    db =get_hist()
    data = db.construction.find({},{'_id':0})
    data = pd.DataFrame(list(data))
    con2016=[]
    for i in data.columns:
        if '2016' in i:
            con2016.append(data[i].sum())
    months =['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    import plotly.plotly as py
    import plotly.graph_objs as go
    import plotly
    py.sign_in('deanoreilly990', 'WgnPSOLqPlZ5uXFu6WKx')
    data = [go.Bar(
                x=months,
                y=con2016
        )]
    layout = go.Layout(
        title='Construction Year Pervious: 2016',
        yaxis=dict(
            title='No. of Properties Constructed'),
        xaxis=dict(
            title='Month'),
        autosize=False,
        width=900,
        height=400,
        margin=go.Margin(
            l=80,
            r=10,
            b=50,
            t=50,
            pad=10
        ),
    )
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='/home/user/FlaskApp/App/static/images/History/home3.html',show_link=False,auto_open=False)
def home4():
    import pandas as pd

    db = get_hist()
    data = db.population.find({},{'_id':0})
    data = pd.DataFrame(list(data))
    ages = data['Age '].unique()
    ages.sort()
    countages =[]
    for i in ages:
        datad = data[data['Age ']==i]
        sumi = datad['Population 2011'].sum()
        countages.append(sumi)
    import plotly.plotly as py
    import plotly.graph_objs as go
    import plotly
    py.sign_in('deanoreilly990', 'WgnPSOLqPlZ5uXFu6WKx')
    data = [go.Bar(
                x=ages,
                y=countages
        )]
    layout = go.Layout(
        title='Age of Population Cenus 2011',
        yaxis=dict(
            title='No. Of People'),
        xaxis=dict(
            title='Age Groups'),
        autosize=False,
        width=900,
        height=450,
        margin=go.Margin(
            l=80,
            r=10,
            b=100,
            t=50,
            pad=10
        ),
    )
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='/home/user/FlaskApp/App/static/images/History/home4.html', show_link=False,auto_open=False)

def homecontrol():
    home1()
    home3()
    home4()
    crimes = home2()
    return crimes
