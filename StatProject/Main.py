import urllib2
import plotly
import plotly.graph_objs as go
from bs4 import BeautifulSoup
import numpy as np
from scipy import stats

from Tkinter import *

class TennisPlayer:
    name = None
    ranking = None
    age = None
    statsLink = None

    # service stats

    aces = None
    doubleFaults = None
    firstServe = None  # percentage
    firstServePointsWon = None  # percentage
    secondServePointsWon = None  # percentage
    breakPointsFaced = None
    breakPointsSaved = None  # percentage
    serviceGamesPlayed = None
    serviceGamesWon = None  # percentage
    totalServicePointsWon = None  # percentage

    # return stats

    firstServeReturnPointsWon = None  # percentage
    secondServeReturnPointsWon = None  # percentage
    breakPointOpportunities = None
    breakPointsConverted = None  # percentage
    returnGamesPlayed = None
    returnGamesWon = None  # percentage
    returnPointsWon = None  # percentage
    totalPointsWon = None  # percentage

    def __init__(self):
        self.name = None

    def __init__(self, name, ranking, age, statsLink, aces):
        self.name = name
        self.ranking = ranking
        self.age = age
        self.statsLink = statsLink
        self.aces = aces

    def __str__(self):
        return "Name: " + self.name + "; Rank " + self.ranking + "; Age: " + self.age + "; Link: " + self.statsLink

    def printFull(self):
        print('Name: ' + self.name)
        print('Rank: ' + self.ranking)
        print('Age: ' + self.age)
        print('Stats Link: ' + self.statsLink)
        print('Aces: ' + self.aces)
        print('Double Faults: ' + self.doubleFaults)
        print('1st Serve: ' + self.firstServe)
        print('1st Serve Points Won: ' + self.firstServePointsWon)
        print('2nd Serve Points Won: ' + self.secondServePointsWon)
        print('Break Points Faced: ' + self.breakPointsFaced)
        print('Break Points Saved: ' + self.breakPointsSaved)
        print('Service Games Played: ' + self.serviceGamesPlayed)
        print('Service Games Won: ' + self.serviceGamesWon)
        print('Total Service Points Won: ' + self.totalServicePointsWon)
        print('1st Serve Return Points Won: ' + self.firstServeReturnPointsWon)
        print('2nd Serve Return Points Won: ' + self.secondServeReturnPointsWon)
        print('Break Point Opportunities: ' + self.breakPointOpportunities)
        print('Break Points Converted: ' + self.breakPointsConverted)
        print('Return Games Played: ' + self.returnGamesPlayed)
        print('Return Games Won: ' + self.returnGamesWon)
        print('Return Points Won: ' + self.returnPointsWon)
        print('Total Points Won: ' + self.totalPointsWon)
        print("")


rankings_page= "http://www.atpworldtour.com/en/rankings/singles"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

req = urllib2.Request(rankings_page, headers=hdr)

try:
    page = urllib2.urlopen(req)
except urllib2.HTTPError as e:
    pass

soup = BeautifulSoup(page, 'html.parser')
table = soup.find('table', attrs={'class': "mega-table"})
tbody = soup.find('tbody')

playerArr = []

for element in soup.findAll('tr'):
    rankcell = element.find('td', attrs = {'class': 'rank-cell'})
    namecell = element.find('td', attrs = {'class': 'player-cell'})
    agecell =  element.find('td', attrs = {'class': 'age-cell'})

    rank = None
    age = None
    name = None
    link = None
    aces = None

    player = TennisPlayer(name, rank, age, link, aces)

    if rankcell is not None:
        rank = rankcell.text
        player.ranking = rank.strip()
    if agecell is not None:
        age = agecell.text
        player.age = age.strip()
    if namecell is not None:
        a = namecell.find('a')
        name = a.text
        link = a.attrs
        player.name = name.strip()

    if (namecell is not None) and (agecell is not None) and (rankcell is not None):
        newLink = 'http://www.atpworldtour.com' + link['href']
        newLink = newLink.replace("overview", "player-stats")
        player.statsLink = newLink;
        playerArr.append(player)


for player in playerArr:
    print(player)
    statsUrl = player.statsLink
    secondReq = urllib2.Request(statsUrl, headers=hdr)
    try:
        statsPage = urllib2.urlopen(secondReq)
    except urllib2.HTTPError as e:
        pass

    soup = BeautifulSoup(statsPage, 'html.parser')
    megaTableWrapper = soup.find('div', attrs={'id': 'playerMatchFactsContainer', 'class': 'mega-table-wrapper'})
    tableCounter = 0
    for table in megaTableWrapper.findAll('table'):
        tbody = table.find('tbody')
        if(tableCounter == 0):
            for tr in tbody.findAll('tr'):
                tdCounter = 0
                statName = None
                for td in tr.findAll('td'):
                    if(tdCounter == 0):
                        statName = td.text.strip()
                        tdCounter += 1
                    else:
                        statValue = td.text.strip()
                        # print(statName)
                        if(statName == 'Aces'):
                            player.aces = statValue
                        elif(statName == 'Double Faults'):
                            player.doubleFaults = statValue
                        elif(statName == '1st Serve'):
                            player.firstServe = statValue
                        elif(statName == '1st Serve Points Won'):
                            player.firstServePointsWon = statValue
                        elif(statName == '2nd Serve Points Won'):
                            player.secondServePointsWon = statValue
                        elif(statName == 'Break Points Faced'):
                            player.breakPointsFaced = statValue
                        elif(statName == 'Break Points Saved'):
                            player.breakPointsSaved = statValue
                        elif(statName == 'Service Games Played'):
                            player.serviceGamesPlayed = statValue
                        elif(statName == 'Service Games Won'):
                            player.serviceGamesWon = statValue
                        elif(statName == 'Total Service Points Won'):
                            player.totalServicePointsWon = statValue
                        elif(statName == '1st Serve Return Points Won'):
                            player.firstServeReturnPointsWon = statValue
                        elif(statName == '2nd Serve Return Points Won'):
                            player.secondServeReturnPointsWon = statValue
                        elif(statName == 'Break Points Opportunities'):
                            player.breakPointOpportunities = statValue
                        elif(statName == 'Break Points Converted'):
                            player.breakPointsConverted = statValue
                        elif(statName == 'Return Games Played'):
                            player.returnGamesPlayed = statValue
                        elif(statName == 'Return Games Won'):
                            player.returnGamesWon = statValue
                        elif(statName == 'Return Points Won'):
                            player.returnPointsWon = statValue
                        elif(statName == 'Total Points Won'):
                            player.totalPointsWon = statValue


    player.printFull()

nameArray = []
ageArray = []
rankArray = []
aceArray = []
doubleFaultArray = []
firstServeArray = []
firstServePointsWonArray = []
secondServePointsWonArray = []
breakPointsFacedArray = []
breakPointsSavedArray = []
serviceGamesPlayedArray = []
serviceGamesWonArray = []
totalServicePointsWonArray = []
firstServeReturnPointsWonArray = []
secondServeReturnPointsWonArray = []
breakPointsOpportunitiesArray = []
breakPointsConvertedArray = []
returnGamesPlayedArray = []
returnGamesWonArray = []
returnPointsWonArray = []
totalPointsWonArray = []

for player in playerArr:
    nameArray.append(player.name)
    ageArray.append(float(player.age))
    rankArray.append(float(player.ranking))
    aceArray.append(float(player.aces.replace(',','')))
    doubleFaultArray.append(float(player.doubleFaults.replace(',','')))
    firstServeArray.append(float(player.firstServe.strip('%')))
    firstServePointsWonArray.append(float(player.firstServePointsWon.strip('%')))
    secondServePointsWonArray.append(float(player.secondServePointsWon.strip('%')))
    breakPointsFacedArray.append(float(player.breakPointsFaced.replace(',','')))
    breakPointsSavedArray.append(float(player.breakPointsSaved.strip('%')))
    serviceGamesPlayedArray.append(float(player.serviceGamesPlayed.replace(',','')))
    serviceGamesWonArray.append(float(player.serviceGamesWon.strip('%')))
    totalServicePointsWonArray.append(float(player.totalServicePointsWon.strip('%')))
    firstServeReturnPointsWonArray.append(float(player.firstServeReturnPointsWon.strip('%')))
    secondServeReturnPointsWonArray.append(float(player.secondServeReturnPointsWon.strip('%')))
    breakPointsOpportunitiesArray.append(player.breakPointOpportunities.replace(',',''))
    breakPointsConvertedArray.append(float(player.breakPointsConverted.strip('%')))
    returnGamesPlayedArray.append(float(player.returnGamesPlayed.replace(',','')))
    returnGamesWonArray.append(float(player.returnGamesWon.strip('%')))
    returnPointsWonArray.append(float(player.returnPointsWon.strip('%')))
    totalPointsWonArray.append(float(player.totalPointsWon.strip('%')))

STATS = [
    ("Age", ageArray),
    ("Rank", rankArray),
    ("Aces", aceArray),
    ("Double Faults", doubleFaultArray),
    ("First Serve Percentage", firstServeArray),
    ('First Serve Points Won Percentage', firstServePointsWonArray),
    ('Second Serve Points Won Percentage', secondServePointsWonArray),
    ('Break Points Faced', breakPointsFacedArray),
    ('Break Points Saved Percentage', breakPointsSavedArray),
    ('Service Games Played', serviceGamesPlayedArray),
    ('Service Games Won Percentage', serviceGamesWonArray),
    ('Total Service Points Won Percentage', totalServicePointsWonArray),
    ('First Serve Return Points Won Percentage', firstServeReturnPointsWonArray),
    ('Second Serve Return Points Won Percentage', secondServeReturnPointsWonArray),
    ('Break Point Opportunities', breakPointsOpportunitiesArray),
    ('Break Points Converted Percentage', breakPointsConvertedArray),
    ('Return Games Played', returnGamesPlayedArray),
    ('Return Games Won Percentage', returnGamesWonArray),
    ('Return Points Won Percentage', returnPointsWonArray),
    ('Total Points Won Percentage', totalPointsWonArray)
]

master = Tk()

counter = 1
rowCounter = 0

group1 = StringVar()
group2 = StringVar()

for stat, array in STATS:
    b = Radiobutton(master, text=stat, variable= group1, value = stat)
    b.pack()
    b.deselect()
    b.grid(row=rowCounter, column=0)
    rowCounter += 1
    counter += 1

rowCounter = 0
for stat, array in STATS:
    b = Radiobutton(master, text=stat, variable= group2, value = stat)
    b.pack()
    b.deselect()
    b.grid(row=rowCounter, column=1)
    rowCounter += 1
    counter += 1


def submit():
    stat1 = group1.get()
    stat2 = group2.get()

    dictionary = dict(STATS)
    stat1Array = dictionary.get(stat1)
    stat2Array = dictionary.get(stat2)

    if stat1Array is None or stat2Array is None:
        return

    x = stat2Array
    y = stat1Array

    x = np.array(x).astype(np.float)
    y = np.array(y).astype(np.float)

    slope, intercept, r_value, p_value, std_error = stats.linregress(x, y)
    line = (slope * x) + intercept

    scatterTrace = go.Scatter(
        x = x,
        y = y,
        mode = 'markers',
        marker = go.Marker(color = 'rgb(255, 127, 14)'),
        name = 'Data',
        text=nameArray
    )

    lineTrace = go.Scatter(
        x = x,
        y = line,
        mode = 'lines',
        marker = go.Marker(color='rgb(31, 119, 180)'),
        name = 'Fit',
        text='Y = ' + "{0:.5f}".format(slope) + 'X + ' + "{0:.2f}".format(intercept)
    )

    annotation = go.Annotation(
        x = 3.5,
        y = 30,
        text = "",
        showarrow = False,
        font = go.Font(size = 16)
    )

    layout = go.Layout(
        title = stat2 + ' vs ' + stat1 + "; R^2 = " + "{0:.2f}".format(r_value * r_value),
        plot_bgcolor='rgb(229, 229, 229)',
        xaxis=go.XAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)', title=stat2),
        yaxis=go.YAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)', title=stat1),
        annotations=[annotation]
    )

    data = [scatterTrace, lineTrace]
    figure = go.Figure(data = data, layout = layout)

    plotly.offline.plot(figure)



submitButton = Button(master, text="Graph", command=submit)
submitButton.pack()
submitButton.grid(row=rowCounter + 2, column = 0)

master.mainloop()
