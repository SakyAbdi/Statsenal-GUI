import customtkinter
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from datetime import date
import os
from openpyxl import load_workbook
import matplotlib.pyplot as plt 
from adjustText import adjust_text

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()

root.geometry("500x350")

root.title('Statsenal v0.1.0')

root.resizable(0,0)

label = customtkinter.CTkLabel(root, text="Welcome to Statsenal!", font=("Roboto", 24))
label.grid(row=1, pady=12, padx=100)

def combo_selection():
    club_choice = club_options.get()
    stat_choice = stat_options.get()
    season_choice = season_options.get()
    club_picker(club_choice, stat_choice, season_choice)
    
def club_picker(club_choice, stat_choice, season_choice):
    driver = webdriver.Chrome()
    driver.maximize_window()
    if stat_choice=='Goals':
        driver.get('https://www.premierleague.com/stats/top/players/goals')
    else:
        pass
    if stat_choice=='Assists':
        driver.get('https://www.premierleague.com/stats/top/players/goal_assist')
    else:
        pass

    cookies_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")    
    if cookies_button == driver.find_element(By.ID, "onetrust-accept-btn-handler"):
        cookies_button.click()
    else:
        pass
    time.sleep(1)
    
    hidden_element = driver.find_element(By.CLASS_NAME, 'label')
    driver.execute_script("arguments[0].click();", hidden_element)
    time.sleep(1)

    if season_choice==season_choice:
        driver.execute_script("arguments[0].click();", hidden_element)
        time.sleep(1)
        season_filter_button= driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[2]/div[1]/section/div[2]/div[2]')
        season_filter_button.click()
        time.sleep(1)
        season_selection_button= driver.find_element(By.XPATH, f'//li[@data-option-name="{season_choice}"]')
        season_selection_button.click()
        time.sleep(1)
    else:
        pass
    if club_choice==club_choice:
        driver.execute_script("arguments[0].click();", hidden_element)
        time.sleep(1)
        club_filter_button= driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[2]/div[1]/section/div[3]/div[2]')
        club_filter_button.click()
        time.sleep(1)
        club_selection_button= driver.find_element(By.XPATH, f'//li[@data-option-name="{club_choice}"]')
        club_selection_button.click()
        time.sleep(1)
    else:
        pass
        
    today = date.today()
    
    folder_path = 'Goals Spreadsheets'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    else:
        pass

    stat_link = driver.page_source.encode('ISO-8859-1')
    stat_data = pd.read_html(stat_link, header =0)[0]
    stat_date = f'{folder_path}/{club_choice}_{stat_choice}_List_{today}.csv'
    stat_data.to_csv(stat_date, encoding='ISO-8859-1')
    stat_workbook = pd.read_csv(stat_date, encoding='ISO-8859-1')
    columns_to_drop = [0, 6]
    stat_workbook = stat_workbook.drop(stat_workbook.columns[columns_to_drop], axis=1)
    stat_workbook.to_csv(stat_date, encoding='ISO-8859-1', index = False)

    x_axis = stat_workbook['Rank']
    y_axis = stat_workbook['Stat']
    names = stat_workbook['Player']
    fig, ax = plt.subplots()
    plt.bar(x_axis, y_axis, label = "Player")
    player_names = []
    for i, txt in enumerate(names):
        player_names.append(ax.annotate(txt, (x_axis[i], y_axis[i])))
    adjust_text(player_names, expand = (1.0, 3.5), arrowprops = {'color': 'blue'})
    plt.xlabel('Rank') 
    plt.ylabel('Goals Scored') 
    plt.title(f'{club_choice} {stat_choice} Stats ({season_choice}):')
    plt.gcf().patch.set_edgecolor('b')
    plt.gcf().patch.set_linewidth(3)
    new_season_choice = season_choice.replace('/', '-')
    plt.savefig(f'{folder_path}/{club_choice} {stat_choice} Stats for {new_season_choice}.png')
    plt.show()

premier_league_list = ["All Clubs", "Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton & Hove Albion", "Burnley", "Chelsea", "Crystal Palace", "Everton", "Fulham", "Liverpool", "Luton Town", "Manchester City", "Manchester United", "Newcastle United", "Nottingham Forest", "Sheffield United", "Tottenham Hotspur", "West Ham United", "Wolverhampton Wanderers"]

stat_list = ["Goals", "Assists"]

season_list = ["1992/93", "1993/94", "1994/95", "1995/96", "1996/97", "1997/98", "1998/99", "1999/00", "2000/01", "2001/02", "2002/03", "2003/04", "2004/05", "2005/06", "2006/07", "2007/08", "2008/09", "2009/10", "2010/11", "2011/12", "2012/13", "2013/14", "2014/15", "2015/16", "2016/17", "2017/18", "2018/19", "2019/20", "2020/21", "2021/22", "2022/23", "2023/24"]

club_label = customtkinter.CTkLabel(root, text="Select a Club:", font=("Roboto", 20))
club_label.grid(sticky='w', row= 2, pady=10, padx=10)

club_options = customtkinter.CTkComboBox(root, values=premier_league_list)
club_options.grid(row=2, pady=10, padx=(50, 0))

stat_label = customtkinter.CTkLabel(root, text="Select a Stat:", font=("Roboto", 20))
stat_label.grid(sticky='w', row= 3, pady=0, padx=10)

stat_options = customtkinter.CTkComboBox(root, values=stat_list)
stat_options.grid(row= 3, pady=12, padx=(50, 0))

season_label = customtkinter.CTkLabel(root, text="Select a Season:", font=("Roboto", 20))
season_label.grid(sticky='w', row= 4, pady=0, padx=10)

season_options = customtkinter.CTkComboBox(root, values=season_list)
season_options.grid(row= 4, pady=12, padx=(50, 0))

button = customtkinter.CTkButton(root, text="Select", command=combo_selection)
button.grid(row=5, pady=12, padx=(50, 0))

root.mainloop()