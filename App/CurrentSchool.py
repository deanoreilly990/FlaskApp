def get_daft():
    from pymongo import MongoClient
    client = MongoClient('mongodb://dor:Abbie321@83.212.82.156:27017/rentalData')
    db = client.rentalData
    return db
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
    date = date - 1
    if date == 2:
        enddate = "-28"
    elif date in [4, 6, 11, 9]:
        enddate = "-30"
    else:
        enddate = "-31"
    return date,enddate
def get_db():
    from pymongo import MongoClient
    client = MongoClient('mongodb://user:Abbie321@83.212.82.156:27017/HistData')
    db=client.HistData
    return db
def logdata(value1, value2):
    from pymongo import MongoClient
    import pandas as pd
    global data
    global data
    db = get_db()
    data = db.primaryschools.find({},{'_id':0})
    data = pd.DataFrame(list(data))
    data['PC'] = data['PC'].str.lower()
    v1 =[]
    v2=[]
    bedroomsLastMonth(value1,'v1')
    bedroomsLastMonth(value2,'v2')
    averagePerRoom(value1,'v1')
    averagePerRoom(value2,'v2')
    rentalCharts(value1,'v1')
    rentalCharts(value2,'v2')
    saleovertime(value1,'v1')
    saleovertime(value2,'v2')
    rentovertime(value1,'v1')
    rentovertime(value2,'v2')
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

    plotly.offline.plot(fig, filename='/home/user/FlaskApp/App/static/images/2017/V1-'+v+'.html', show_link=False,auto_open=False)
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

    plotly.offline.plot(fig, filename='/home/user/FlaskApp/App/static/images/2017/V2-'+v+'.html', show_link=False,auto_open=False)

def bedroomsLastMonth(value1,v1):
    import pandas as pd
    from pymongo import MongoClient
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

    plotly.offline.plot(fig,filename='/home/user/FlaskApp/App/static/images/2017/V3-'+v1+'.html',show_link=False,auto_open=False)
def averagePerRoom(pc,version):

    import pandas as pd
    from pymongo import MongoClient
    import plotly.plotly as py
    import plotly.graph_objs as go
    import plotly
    import datetime
    import calendar
    py.sign_in('deanoreilly990', 'WgnPSOLqPlZ5uXFu6WKx')
    db = get_daft()
    data = db.sale.find({}, {'_id': 0})
    data = pd.DataFrame(list(data))
    data = data.dropna()
    date,enddate = getdate()
    str1 = "2017-0" + str(date) + "-01"
    str2 = "2017-0" + str(date) + enddate
    data = data[data['Post Code'] == pc]
    data['Date Entered'] = pd.to_datetime(data['Date Entered'])
    data = data[data["Date Entered"].isin(pd.date_range(str1, str2))]
    beds = data['Beds'].unique()
    bed =['1','2','3','4','5','6','7']
    bedC = []
    for i in bed:
        sumi = []
        count = 0
        for index,row in data.iterrows():
            if i in row[1]:
                count =count +1
                sumi.append(int(row[4]))
        sumi=sum(sumi)
        try:
            sumi=sumi/count
        except:
            pass
        bedC.append(sumi)
    Fbed=[]
    FbedC =[]
    for i in range(len(bed)):
        if bedC[i] == 0:
            pass
        else:
            Fbed.append(bed[i])
            FbedC.append(bedC[i])
    trace = go.Bar(
        x=Fbed,
        y=FbedC
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
    plotly.offline.plot(fig, filename='/home/user/FlaskApp/App/static/images/2017/V4-' + version + '.html', show_link=False,auto_open=False)


def rentalCharts(pc,v1):
    """ This function, is concenered with the gathering, perparation, analysisng and the visual representation of the daft rental data"""
    import pandas as pd
    from pymongo import MongoClient
    import plotly.plotly as py
    import plotly.graph_objs as go
    import plotly
    import datetime
    import calendar
    py.sign_in('deanoreilly990', 'WgnPSOLqPlZ5uXFu6WKx')
    db= get_daft()
    data = db.rentFinal.find({},{'_id':0})
    data = pd.DataFrame(list(data))
    data = data.dropna()
    date,enddate = getdate()
    str1 = "2017-0" + str(date) + "-01"
    str2 = "2017-0" + str(date) + enddate
    data = data[data['Post Code'] == pc]
    data['Date Entered'] = pd.to_datetime(data['Date Entered'])
    data = data[data["Date Entered"].isin(pd.date_range(str1, str2))]
    typecount = [0, 0, 0]
    studioprice = 0
    houseprice = [0, 0, 0, 0]
    housetype = [0, 0, 0, 0]
    apartmentprice = [0, 0, 0, 0]
    apartmenttype = [0, 0, 0, 0]
    for index, row in data.iterrows():
        price = row[4]
        price = price.encode('ascii', 'ignore')
        try:
            price = price.replace(',', '')
        except:
            pass
        try:
            price = float(price)
        except:
            continue
        if 'Studio' in row[5]:
            typecount[0] = typecount[0] + 1
            studioprice = studioprice + price
        if 'House' in row[5]:
            typecount[1] = typecount[1] + 1
            if '2' in row[1]:
                housetype[0] = housetype[0] + 1
                houseprice[0] = houseprice[0] + price
            elif '3' in row[1]:
                housetype[1] = housetype[1] + 1
                houseprice[1] = houseprice[1] + price
            elif '4' in row[1]:
                housetype[2] = housetype[2] + 1
                houseprice[2] = houseprice[2] + price
            elif '5' in row[1]:
                housetype[3] = housetype[3] + 1
                houseprice[3] = houseprice[3] + price
        elif 'Apartment' in row[5]:
            typecount[2] = typecount[2] + 1
            if '2' in row[1]:
                apartmenttype[0] = apartmenttype[0] + 1
                apartmentprice[0] = apartmentprice[0] + price
            elif '3' in row[1]:
                apartmenttype[1] = apartmenttype[1] + 1
                apartmentprice[1] = apartmentprice[1] + price
            elif '4' in row[1]:
                apartmenttype[2] = apartmenttype[2] + 1
                apartmentprice[2] = apartmentprice[2] + price
            elif '5' in row[1]:
                apartmenttype[3] = apartmenttype[3] + 1
                apartmentprice[3] = apartmentprice[3] + price
    try:
        studioprice = studioprice / typecount[0]
    except:
        pass
    houseaverage = []
    apartmentaverage = []
    apartmentaverage.append(studioprice)

    for i in range(4):
        try:
            averageh = houseprice[i] /housetype[i]
            houseaverage.append(averageh)
            averageA = apartmentprice[i]/apartmenttype[i]
            apartmentaverage.append(averageA)
        except:
            pass
    f = lambda x:round(x,2)
    apartmentaverage = map(f,apartmentaverage)
    houseaverage = map(f,houseaverage)

    fig = {
                'data': [{'labels': [ 'Studio - 1bed','Houses','Apartments'],
                              'values': typecount,
                              'type': 'pie'}],
                    'layout': {'title': 'Ratio of properties availble last month ',
                              'autosize':False,
                              'width':500,
                              'height':400,
                              'margin':{'l':10,'r':10,'b':50,'t':50,'pad':4}}
                     }
    plotly.offline.plot(fig,filename='/home/user/FlaskApp/App/static/images/2017/V5-'+v1+'.html',show_link=False,auto_open=False)

    trace = go.Bar(
            x=['1 Bed-Studio','2 Bed','3 Bed','4 Bed','5 Bed'],
            y=apartmentaverage
        )
    layout = go.Layout(
        title='Average Price of Apartment by room type in  : ' + calendar.month_name[date],
        yaxis=dict(
            title='Average Price Per Month'),
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
    plotly.offline.plot(fig, filename='/home/user/FlaskApp/App/static/images/2017/V6-' + v1 + '.html', show_link=False,auto_open=False)
    trace = go.Bar(
            x=['2 Bed','3 Bed','4 Bed','5 Bed'],
            y=houseaverage
        )
    layout = go.Layout(
        title='Average Price of Houses by room type in: ' + calendar.month_name[date],
        yaxis=dict(
            title='Average Price Per Month'),
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
    plotly.offline.plot(fig, filename='/home/user/FlaskApp/App/static/images/2017/V7-' + v1 + '.html', show_link=False,auto_open=False)
    apartmenttype.append(typecount[0])
    fig = {
                'data': [{'labels': ['2 Bed','3 Bed','4 Bed','5 Bed','Studio - 1 bed'],
                              'values': apartmenttype,
                              'type': 'pie'}],
                    'layout': {'title': 'Ratio of type of Apartments Available ',
                              'autosize':False,
                              'width':500,
                              'height':400,
                              'margin':{'l':10,'r':20,'b':50,'t':50,'pad':4}}
                     }
    plotly.offline.plot(fig,filename='/home/user/FlaskApp/App/static/images/2017/V8-'+v1+'.html',show_link=False,auto_open=False)
    fig = {
                'data': [{'labels': ['2 Bed','3 Bed','4 Bed','5 Bed'],
                              'values': housetype,
                              'type': 'pie'}],
                    'layout': {'title': 'Ratio of type of Houes Available ',
                              'autosize':False,
                              'width':500,
                              'height':400,
                              'margin':{'l':10,'r':20,'b':50,'t':50,'pad':4}}
                     }
    plotly.offline.plot(fig,filename='/home/user/FlaskApp/App/static/images/2017/V9-'+v1+'.html',show_link=False,auto_open=False)

def saleovertime(postcode,v1):
    """ This function is used in the gathering of the averaging sale information in each area given. The function is also responsiable for producing the
    Data visualisation aids needed
    """
    import pandas as pd
    import plotly.plotly as py
    import plotly.graph_objs as go
    import plotly
    import datetime
    py.sign_in('deanoreilly990', 'WgnPSOLqPlZ5uXFu6WKx')
    db = get_daft()
    data = db.Average.find({},{'_id':0})
    data = pd.DataFrame(list(data))
    month = datetime.datetime.now()
    month = month.strftime("%b")
    bed2av =[]
    bed3av =[]
    bed4av =[]
    data = data[data['Postcode']==str(postcode)]
    Months = ['Feb','March','April','May','June','July','August','Sept','Nov','Dec','Jan']
    columns = data.columns
    count=[]
    for i in columns:
        if i =='Postcode':
            pass
        else:
            count.append(i)
    for i in count:
        bed2av.append(data[i].values[0][0])
        bed3av.append(data[i].values[0][1])
        bed4av.append(data[i].values[0][2])

    trace0 = go.Scatter(
        x = Months,
        y = bed2av,
        mode = 'lines',
        name = '2 Bed Average'
    )
    trace1 = go.Scatter(
        x = Months,
        y = bed3av,
        mode = 'lines+markers',
        name = '3 Bed Average'
    )
    trace2 = go.Scatter(
        x = Months,
        y = bed4av,
        mode = 'markers',
        name = '4 Bed Average '
    )
    layout = go.Layout(
        title ='Average House Sale Price, Per Room Count',
        yaxis=dict(
            title='Average Price'),
        xaxis=dict(
            title= 'Months'),
        autosize=False,
            width=500,
            height=400,
            margin=go.Margin(
                l=80,
                r=10,
                b=90,
                t=50,
                pad=10)
    )
    data = [trace0,trace1,trace2]
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig,filename='/home/user/FlaskApp/App/static/images/2017/V10-'+v1+'.html',show_link=False,auto_open=False)
def rentovertime(postcode,v1):
    """ This function is used in the gathering of the averaging rental information in each area given. The function is also responsiable for producing the
    Data visualisation aids needed
    """
    import pandas as pd
    import plotly.plotly as py
    import plotly.graph_objs as go
    import plotly
    import datetime
    py.sign_in('deanoreilly990', 'WgnPSOLqPlZ5uXFu6WKx')
    db = get_daft()
    data = db.AverageRent.find({},{'_id':0})
    data = pd.DataFrame(list(data))
    data = data[data['Postcode']==str(postcode)]
    columns = data.columns
    count=[]
    bed2av =[]
    bed3av =[]
    bed4av =[]
    for i in columns:
        if i =='Postcode':
            pass
        else:
            count.append(i)
    for i in count:
        bed2av.append(data[i].values[0][0])
        bed3av.append(data[i].values[0][1])
        bed4av.append(data[i].values[0][2])
    f = lambda x:round(x,2)
    bed2av= map(f,bed2av)
    bed3av= map(f,bed3av)
    bed4av= map(f,bed4av)
    Months = ['Feb','March','April','May','June','July','August','Sept','Nov','Dec','Jan']
    trace0 = go.Scatter(
            x = Months,
            y = bed2av,
            mode = 'lines',
            name = '2 Bed Average'
        )
    trace1 = go.Scatter(
        x = Months,
        y = bed3av,
        mode = 'lines+markers',
        name = '3 Bed Average'
    )
    trace2 = go.Scatter(
        x = Months,
        y = bed4av,
        mode = 'markers',
        name = '4 Bed Average '
    )
    layout = go.Layout(
        title ='Rent Price, Per Room Count',
        yaxis=dict(
            title='Average Price'),
        xaxis=dict(
            title= 'Months'),
        autosize=False,
            width=500,
            height=400,
            margin=go.Margin(
                l=80,
                r=10,
                b=90,
                t=50,
                pad=10)
    )
    data = [trace0,trace1,trace2]
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig,filename='/FlaskApp/App/static/images/2017/V11-'+v1+'.html',show_link=False,auto_open=False)
