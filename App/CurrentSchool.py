def logdata(value1, value2):

    import pandas as pd
    from pymongo import MongoClient
    global data
    global data
    def get_daft():
        client = MongoClient('localhost:27017')
        db=client.HistData
        return db
    db = get_daft()
    data = db.primaryschools.find({},{'_id':0})
    data = pd.DataFrame(list(data))
    data['PC'] = data['PC'].str.lower()
    v1 =[]
    v2=[]
    bedroomsLastMonth(value1,'v1')
    bedroomsLastMonth(value2,'v2')
    averagePerRoom(value1,'v1')
    averagePerRoom(value2,'v2')
    value1 = 'dublin '+str(value1)
    value2 = 'dublin '+str(value2)
    v1.append(getdata(value1))
    v2.append(getdata(value2))
    plot(value1,v1[0][1],v1[0][2],v1[0][3],v1[0][4],'v1')
    plot(value2, v2[0][1], v2[0][2], v2[0][3], v2[0][4],'v2')

    return v1[0][1],v2[0][1]

def getdata(value1):
    global data
    dataV = data[data['PC']==value1]
    NumberofSchools = dataV['Total Pupils'].count()
    boys = dataV['Total Boys'].sum()
    girls = dataV['Total Girls'].sum()
    religions = dataV['Religion'].unique()
    religionsCount = []
    for i in religions:
        rdata = dataV[dataV['Religion']==i]
        religionsCount.append(rdata['Religion'].count())
    return NumberofSchools,boys,girls,religions,religionsCount

def plot(name,boys,girls,religions,religionsCount,v):
    import plotly.plotly as py
    import plotly.graph_objs as go
    import plotly
    py.sign_in('deanoreilly990', 'WgnPSOLqPlZ5uXFu6WKx')
    fig = {
        'data': [{'labels': ['Boys','Girls'],
                  'values': [boys,girls],
                  'type': 'pie'}],
        'layout': {'title': 'Boy/Girl ratio in schools in '+name,
                          'autosize':False,
                          'width':500,
                          'height':400,
                          'margin':{'l':10,'r':10,'b':50,'t':50,'pad':4}}
                 }

    plotly.offline.plot(fig, filename='/home/dor/FlaskApp/App/static/images/2017/V1-'+v+'.html', show_link=False,auto_open=False)
    fig = {
        'data': [{'labels': religions,
                  'values': religionsCount,
                  'type': 'pie'}],
        'layout': {'title': 'School religions in '+name,
                          'autosize':False,
                          'width':500,
                          'height':400,
                          'margin':{'l':10,'r':10,'b':50,'t':50,'pad':4}}
                 }

    plotly.offline.plot(fig, filename='/home/dor/FlaskApp/App/static/images/2017/V2-'+v+'.html', show_link=False,auto_open=False)

def bedroomsLastMonth(value1,v1):
    import pandas as pd
    from pymongo import MongoClient
    def get_daft():
        client = MongoClient('localhost:27017')
        db=client.rentalData
        return db
    import plotly.plotly as py
    import plotly.graph_objs as go
    import plotly
    py.sign_in('deanoreilly990', 'WgnPSOLqPlZ5uXFu6WKx')
    db= get_daft()
    data = db.sale.find()
    data = pd.DataFrame(list(data))
    data = data.dropna()
    bedcount = [0,0,0,0]

    ddata = data[data['Post Code'] == value1]
    for index, row in ddata.iterrows():
        if '2' in row[1]:
            bedcount[0] = bedcount[0] + 1
        elif '3' in row[1]:
            bedcount[1] = bedcount[1] + 1
        elif '4' in row[1]:
            bedcount[2] = bedcount[2] + 1
        else:
            bedcount[3] = bedcount[3] + 1
    fig = {
            'data': [{'labels': [ '2 Bedrooms','3 Bedrooms','4 Bedrooms','5+ Bedrooms'],
                          'values': bedcount,
                          'type': 'pie'}],
                'layout': {'title': 'Overview bedrooms in Dublin '+ value1,
                          'autosize':False,
                          'width':500,
                          'height':400,
                          'margin':{'l':10,'r':10,'b':50,'t':50,'pad':4}}
                 }

    plotly.offline.plot(fig,filename='/home/dor/FlaskApp/App/static/images/2017/V3-'+v1+'.html',show_link=False,auto_open=False)
def averagePerRoom(pc,version):
    import pandas as pd
    from pymongo import MongoClient
    import plotly.plotly as py
    import plotly.graph_objs as go
    import plotly
    import datetime
    import calendar
    py.sign_in('deanoreilly990', 'WgnPSOLqPlZ5uXFu6WKx')

    def get_daft():
        client = MongoClient('localhost:27017')
        db = client.rentalData
        return db

    db = get_daft()
    data = db.sale.find({}, {'_id': 0})
    data = pd.DataFrame(list(data))
    data = data.dropna()
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
    if date == 2:
        enddate = "-28"
    elif date in [4, 6, 11, 9]:
        enddate = "-30"
    else:
        enddate = "-31"
    str1 = "2017-0" + str(date) + "-01"
    str2 = "2017-0" + str(date) + enddate
    data = data[data['Post Code'] == pc]
    data['Date Entered'] = pd.to_datetime(data['Date Entered'])
    data = data[data["Date Entered"].isin(pd.date_range(str1, str2))]
    beds = data['Beds'].unique()
    bedC = []
    for i in beds:
        sumi = 0
        bdata = data[data['Beds'] == i]
        for index, row in bdata.iterrows():
            sumi = sumi + int(row[4])
        count = bdata['Price'].count()
        sumi = sumi / count
        bedC.append(sumi)
    trace = go.Bar(
        x=beds,
        y=bedC
    )
    layout = go.Layout(
        title='Average Price Per Bed Room Number in : ' + calendar.month_name[date],
        yaxis=dict(
            title='Average Price'),
        xaxis=dict(
            title='No.Beds'),
        autosize=False,
        width=500,
        height=400,
        margin=go.Margin(
            l=80,
            r=10,
            b=90,
            t=50,
            pad=10
        ),
    )
    data = [trace]
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='/home/dor/FlaskApp/App/static/images/2017/V4-' + version + '.html', show_link=False,auto_open=False)
