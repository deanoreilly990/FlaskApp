def get_hist():
    from pymongo import MongoClient
    client = MongoClient('mongodb://dor:Abbie321@83.212.82.156:27017/HistData')
    #client = MongoClient('mongodb://localhost:27017//HistData')
    #client = MongoClient('mongodb://localhost:27017/rentalData')
    db = client.HistData
    return db
def get_daft():
    from pymongo import MongoClient
    client = MongoClient('mongodb://dor:Abbie321@83.212.82.156:27017/rentalData')
    #client = MongoClient('mongodb://localhost:27017/rentalData')
    db = client.rentalData
    return db
def index1(postcode):
    import pandas as pd
    from pymongo import MongoClient
    postcode = 'Dublin ' + str(postcode)
    db = get_hist()
    year2010 = db.Data2010.find({},{'_id':0})
    year2011 = db.Data2011.find({},{'_id':0})
    year2012 = db.Data2012.find({},{'_id':0})
    year2013 = db.Data2013.find({},{'_id':0})
    year2014 = db.Data2014.find({},{'_id':0})
    year2015 = db.Data2015.find({},{'_id':0})
    year2016 = db.Data2016.find({},{'_id':0})
    year2010 = pd.DataFrame(list(year2010))
    year2011 = pd.DataFrame(list(year2011))
    year2012 = pd.DataFrame(list(year2012))
    year2013 = pd.DataFrame(list(year2013))
    year2014 = pd.DataFrame(list(year2014))
    year2015 = pd.DataFrame(list(year2015))
    year2016 = pd.DataFrame(list(year2016))
    year2010=year2010[['PostCode','Mean','New Mean']]
    year2011=year2011[['PostCode','Mean','New Mean']]
    year2012=year2012[['PostCode','Mean','New Mean']]
    year2013=year2013[['PostCode','Mean','New Mean']]
    year2014=year2014[['PostCode','Mean','New Mean']]
    year2015=year2015[['PostCode','Mean','New Mean']]
    year2016=year2016[['PostCode','Mean','New Mean']]
    year2010=year2010[year2010['PostCode']==postcode]
    year2011=year2011[year2011['PostCode']==postcode]
    year2012=year2012[year2012['PostCode']==postcode]
    year2013=year2013[year2013['PostCode']==postcode]
    year2014=year2014[year2014['PostCode']==postcode]
    year2015=year2015[year2015['PostCode']==postcode]
    year2016=year2016[year2016['PostCode']==postcode]
    year2010=year2010.values.tolist()
    year2011=year2011.values.tolist()
    year2012=year2012.values.tolist()
    year2013=year2013.values.tolist()
    year2014=year2014.values.tolist()
    year2015=year2015.values.tolist()
    year2016=year2016.values.tolist()
    datasets =[year2010,year2011,year2012,year2013,year2014,year2015,year2016]
    newmean=[]
    oldmean=[]
    for j in datasets:
        for i in range(1,3):
            val = j[0][i]
            val = val.encode('ascii','ignore')
            val = val.replace(',','')
            if i ==1:
                oldmean.append(float(val))
            else:
                newmean.append(float(val))

    import plotly.plotly as py
    import plotly.graph_objs as go
    import plotly
    py.sign_in('deanoreilly990', 'WgnPSOLqPlZ5uXFu6WKx')
    years =['2010','2011','2012','2013','2014','2015','2016']
    trace0 = go.Scatter(
        x = years,
        y = oldmean,
        name = 'Average inc. outliers'
    )
    trace1 = go.Scatter(
        x = years,
        y = newmean,
        mode = 'lines+markers',
        name = 'Actual ext.Average'
    )

    data = [trace0,trace1]
    layout = go.Layout(
        title='Average House Prices Per Year, Including/excluding Outliers',
        yaxis=dict(
            title='Value'),
        xaxis=dict(
            title='Year'),
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
    plotly.offline.plot(fig, filename='/home/user/FlaskApp/App/static/images/History/index/index1.html',show_link=False,auto_open=False)

#Prep Work for Crimes Overview -- Index 2

def crime(postcode):
    import pandas as pd
    from pymongo import MongoClient
    db = get_hist()
    data = db.Crime.find({},{'_id':0})
    data = pd.DataFrame(list(data))
    crimes = data['Crime'].unique()
    crimed = []
    crimed.append(crimes[0])
    crimed.append(crimes[2])
    crimed.append(crimes[4])
    crimed.append(crimes[7])
    crimed.append(crimes[9])
    columns =[]
    columns.append(data.columns[5])
    columns.append(data.columns[6])
    data = data[data['Postcode']==postcode]
    data = data[[columns[0],columns[1],'Crime']]
    findings = []
    for i in crimed:
        datad = data[data['Crime'] == i]
        val1 = datad[columns[0]].sum()
        val2 = datad[columns[1]].sum()
        if val1 > val2:
            findings.append('Down')
        else:
            findings.append('Up')
    return findings



def index3(postcode):
    import pandas as pd
    from pymongo import MongoClient
    x = postcode
    if x == '1' or x == '3' or x =='4':
        x = '2'
    elif x =='12':
        x = '8'
    elif x == '13':
        x = '5'
    elif x == '16':
        x ='14'
    elif x == '18':
        x = 'Dun Laoghaire Rathdown'
    elif x == '20':
        x = '10'
    elif x =='6w':
        x = '6'
    elif x =='SCD':
        x = '24'
    elif x =='WCD':
        x = '15'
    postcode = x
    db = get_hist()
    data = db.SocialData.find({},{'_id':0})
    data = pd.DataFrame(list(data))
    welfare = data[data['Postcode']==postcode] #No Dublin
    yearwelfare =[]
    for j in range(0,7):
        sumi=[]
        for i in range(1,13):
            if i < 10:
                str1 = '201'+str(j)+'M0'+str(i)
            else:
                str1 = '201'+str(j)+'M'+str(i)
            try:
                if j == 5 or j == 6:
                    val =welfare[str1].values[0]
                    val = [int(s) for s in val.split() if s.isdigit()]
                    sumi.append(val)
                else:
                    sumi.append(welfare[str1].values[0])
            except:
                pass
                #print welfare[str1]
        try:
            avg = sum(sumi)
            yearwelfare.append(avg)
        except:
            avg = 0
            for i in sumi:
                avg = avg + i[0]
            yearwelfare.append(avg)
    import plotly.plotly as py
    import plotly.graph_objs as go
    import plotly
    py.sign_in('deanoreilly990', 'WgnPSOLqPlZ5uXFu6WKx')

    trace = go.Scatter(
        x = ['2010','2011','2012','2013','2014','2015','2016'],
        y = yearwelfare,
        name = 'Welfare Sign On ',
        line = dict(
            color = ('rgb(205, 12, 24)'))
    )

    layout = go.Layout(
            title='Welfare Sign On in Dublin '+str(postcode),
            yaxis=dict(
                title='No.Sign On '),
            xaxis=dict(
                title='Year'),
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
    data = [trace]
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='/home/user/FlaskApp/App/static/images/History/index/index3.html',show_link=False,auto_open=False)
"""
def main(AverageH):
    import pandas
    import requests
    from BeautifulSoup import BeautifulSoup
    import logging
    import re
    import time
    Cal = AverageH  * 20 //100
    Needed = Cal
    Cal = AverageH - Cal
    f = lambda x: x.replace(',', '')
    flo = lambda x: float(x)
    form = lambda x:round(x,2)
    url = 'http://www.mortgages.ie/go/first_time_buyers/mortgage_payments_calculator?mode=basic&go=go&buyer_type=First+Time+Buyer&house_price=' + str(
        AverageH) + '&product=2&amt=' + str(Cal) + '&lender=-1&status=Married&comparison=loc&term=30&x=44&y=18'
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)
    table = soup.find('table', attrs={'class': 'results_table_advanced'})
    list_of_rows = []
    for line in table.findAll('td'):
        list_of_rows.append(line)
    OverallValue = []
    for i in list_of_rows:
        i = str(i)
        if '<td onmouseover' in i:
            i = i.split(';')
            OverallValue.append(i[2].replace('&lt', ''))
    OverallValue = map(f, OverallValue)
    OverallValue = map(flo, OverallValue)
    mins = min(OverallValue)
    mins = mins / 360  #360 /12 returns 30 which is the average number of years a mortage is over
    mins = form(mins)
    return mins,AverageH,Cal,Needed
"""
def main(AverageH):
    AverageH # should be the average house price
    Cal = AverageH * 20 // 100
    Needed = Cal
    Cal = AverageH - Cal
    mins = AverageH
    mins = mins / 360
    form = lambda x: round(x, 2)
    mins = form(mins)
    return mins, AverageH, Cal, Needed

def function(postcode):
    import pandas
    import time
    postcode = str(postcode)
    date = (time.strftime("%d/%m/%Y"))
    date = date.split('/')
    date = int(date[1])
    date = date -3
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    date = months[date]
    db = get_daft()
    info = db.Average.find({'Postcode':postcode},{date:1,'_id':0})
    info = pandas.DataFrame(list(info))
    value =0
    for i in info.values[0][0]:
        value = value + i
    return main(value/3)

def index(postcode):
    postcode = str(postcode)
    index1(postcode) #int number
    crimes = crime(postcode) #String number
    index3(postcode)#String number
    mortage = function(postcode)
    return crimes, mortage
