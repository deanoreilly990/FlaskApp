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
