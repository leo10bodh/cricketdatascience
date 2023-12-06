from bs4 import BeautifulSoup
import requests
import csv

#code to get two csv files 

#first csv file containing match summaries
match_summary_file = open('match_summary.csv','w', newline = '')
match_sum = csv.writer(match_summary_file)
match_sum.writerow(['Team 1','Team 2','Winner','Margin','Match Date','match_id'])

#second to get links of the matches played
match_link_file = open('match_link.csv','w',newline = '')
match_link = csv.writer(match_link_file)
match_link.writerow(['Link'])

page = requests.get('https://stats.espncricinfo.com/a/engine/records/team/match_results.html?id=14450;type=tournament')
soup = BeautifulSoup(page.text,'html.parser')

list_of_matches = soup.find_all('tr',class_='data1')

for match in list_of_matches :
    if match.find_all('td')[3].text != "" : 
        team_1 = match.find_all('td')[0].text
        team_2 = match.find_all('td')[1].text
        winner = match.find_all('td')[2].text
        margin = match.find_all('td')[3].text
        date = match.find_all('td')[5].text
        link = match.find_all('td')[6].a.get('href')
        scorecard = match.find_all('td')[6].a.text
        match_link.writerow([link])
        match_sum.writerow([team_1,team_2,winner,margin,date,scorecard])


# #code to get batting summary of the teams that played the match 
batting_summ_file = open('batting_summary.csv','w',newline='')
bat_sum = csv.writer(batting_summ_file)
bat_sum.writerow(['Match','Batting Team','Batting Position','Batsmen name','Runs','Balls','4s','6s','Strike Rate','Out/Not out'])

with open('match_link.csv') as f :
    reader = csv.reader(f)
    for row in reader :
        if row != ['Link'] :
            template = 'https://stats.espncricinfo.com'    
            url = template + row[0]

            try :
                page = requests.get(url)
                soup = BeautifulSoup(page.text,'html.parser')

                team1 = soup.find_all('span',class_="ds-text-title-xs ds-font-bold ds-capitalize")[0].text
                team2 = soup.find_all('span',class_="ds-text-title-xs ds-font-bold ds-capitalize")[1].text
                match = team1 + str(' Vs ') + team2

                team_innings_batting = soup.find_all('tr',class_="")
                bat_pos = 1
                team = team1
                for player in team_innings_batting:
                    try:
                        out = player.find('td',class_='ds-min-w-max !ds-pl-[100px]').text
                        if out != 'not out ' :
                            out = 'out'
                        else :
                            out = 'not out'

                        name = player.find('span',class_='ds-text-tight-s ds-font-medium ds-text-typo ds-underline ds-decoration-ui-stroke hover:ds-text-typo-primary hover:ds-decoration-ui-stroke-primary ds-block').span.text
                        runs = player.find_all('td',class_='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')[0].text
                        balls = player.find_all('td',class_='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')[1].text
                        fours = player.find_all('td',class_='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')[3].text
                        sixes = player.find_all('td',class_='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')[4].text
                        sr = player.find_all('td',class_='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')[5].text
                        out = player.find('td',class_='ds-min-w-max !ds-pl-[100px]').text

                        # print([match,team,bat_pos,name,runs,balls,fours,sixes,sr,out])
                        bat_sum.writerow([match,team,bat_pos,name,runs,balls,fours,sixes,sr,out])
                        bat_pos += 1
                    except Exception as e:
                        print("\n")
                        bat_pos = 1
                        team = team2
            
            except Exception as e:
                print("\n")

bowl_sum_file = open('bowling_summary.csv','w',newline='')
bowl_sum = csv.writer(bowl_sum_file)
bowl_sum.writerow(['Match','Bowling Team','Bowler Name','Overs','Maiden','runs','wickets','economy','0s','4s','6s','Wide balls','No Balls'])

with open('match_link.csv') as f :
    reader = csv.reader(f)
    for row in reader :
        if row != ['Link'] :
            template = 'https://stats.espncricinfo.com'    
            url = template + row[0]

            page = requests.get(url)
            soup = BeautifulSoup(page.text,'html.parser')

            team1 = soup.find_all('span',class_="ds-text-title-xs ds-font-bold ds-capitalize")[0].text
            team2 = soup.find_all('span',class_="ds-text-title-xs ds-font-bold ds-capitalize")[1].text
            match = team1 + str(' vs ') + team2
            print(match)

            body = soup.find_all('table',class_='ds-w-full ds-table ds-table-md ds-table-auto')
            team = team1

            for i in range(len(body)):
                try :
                    team_innings_bowling = body[i].find_all('tr',class_="")   
                    for bowler in team_innings_bowling[1:] :
                        name = bowler.find('span',class_='ds-text-tight-s ds-font-medium ds-text-typo ds-underline ds-decoration-ui-stroke hover:ds-text-typo-primary hover:ds-decoration-ui-stroke-primary ds-block').text
                        overs = bowler.find_all('td',class_='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')[0].text
                        maiden = bowler.find_all('td',class_='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')[1].text
                        runs = bowler.find_all('td',class_='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')[2].text
                        if bowler.find('span',class_='ds-flex ds-items-center ds-cursor-pointer ds-justify-end ds-relative ds-left-[15px]') != None :
                            wickets = bowler.find('span',class_='ds-flex ds-items-center ds-cursor-pointer ds-justify-end ds-relative ds-left-[15px]').strong.text
                        else :
                            wickets = 0
                        economy = bowler.find_all('td',class_='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')[3].text
                        dot_balls = bowler.find_all('td',class_='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')[4].text
                        fours = bowler.find_all('td',class_='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')[5].text
                        sixes = bowler.find_all('td',class_='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')[6].text
                        wides = bowler.find_all('td',class_='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')[7].text
                        no_balls = bowler.find_all('td',class_='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')[8].text
                        
                        print(name,overs,maiden,runs,wickets,economy,dot_balls,fours,sixes,wides,no_balls)
                        bowl_sum.writerow([match,soup.find_all('span',class_="ds-text-title-xs ds-font-bold ds-capitalize")[i].text,name,overs,maiden,runs,wickets,economy,dot_balls,fours,sixes,wides,no_balls])
                except Exception as e:
                    print()
