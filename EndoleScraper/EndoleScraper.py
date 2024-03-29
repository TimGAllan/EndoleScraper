import urllib.request
import pandas as pd
import datetime as dt

def getValue(webContent, startText, endText):
    startPos = webContent.find(startText)+len(startText)
    endPos = webContent.find(endText,webContent.find(startText)+len(startText))
    return webContent[startPos:endPos]

def fetchEndoleDetails(RegNo):
    output = {'RegNo':RegNo}

    url = 'https://suite.endole.co.uk/insight/company/' + RegNo
    response = urllib.request.urlopen(url)  
    webContent = response.read().decode('utf-8')

    output['Name']          = getValue(webContent,'<div class=_heading> Name </div><div class="-font-size-l">'           ,'</div>')
    output['Incorporation'] = getValue(webContent,'<div class=_heading> Incorporation </div><div class="-font-size-l">'  ,'</div>')
    output['Size']          = getValue(webContent,'<div class=_heading> Size </div><div class="-font-size-l">'           ,'</div>').replace('</span>','')
    output['Year Ended']    = getValue(webContent,'<span class=t2>Year Ended</span><span class=t1>'                      ,'</span>')
    output['Employees']     = int(getValue(webContent,'<span class=t2>Employees</span><span class=t1>'                   ,'</span>').replace(',','').replace('Unreported','0'))
    return output

def main():
    f = open('Input.txt', 'r')

    df = pd.DataFrame()

    for line in f.readlines():

        x = fetchEndoleDetails(line.replace('\n',''))
        df = df.append(x, ignore_index=True)
        print(dt.datetime.now().strftime("%H:%M:%S"), "Fetched info for", x['RegNo'])

    df.to_csv('OutPut.csv',index=False)
    print(dt.datetime.now().strftime("%H:%M:%S"), "Output to csv complete")

main()