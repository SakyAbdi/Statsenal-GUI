import customtkinter
from selenium import webdriver
from selenium.webdriver.common.by import By
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

root.title('Statsenal v0.01')

root.resizable(0,0)

label = customtkinter.CTkLabel(root, text="Welcome to Statsenal!", font=("Roboto", 24))
label.grid(row=1, pady=12, padx=100)

def combo_selection():
    club_choice = club_options.get()
    stat_choice = stat_options.get()
    Club_picker(club_choice, stat_choice)
    
def Club_picker(club_choice, stat_choice):
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

    Cookies_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")    
    if Cookies_button == driver.find_element(By.ID, "onetrust-accept-btn-handler"):
        Cookies_button.click()
    else:
        pass
    time.sleep(1)
    
    hidden_element = driver.find_element(By.CLASS_NAME, 'label')
    driver.execute_script("arguments[0].click();", hidden_element)
    time.sleep(1)

    Club_Filter_button= driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[2]/div[1]/section/div[3]/div[2]')
    Club_Filter_button.click()
    time.sleep(1)

    if club_choice==club_choice:
        Arsenal_Filter_button= driver.find_element(By.XPATH, f'//li[@data-option-name="{club_choice}"]')
        Arsenal_Filter_button.click()
    else:
        pass
    time.sleep(1)
    today = date.today()
    
    folder_path = 'Goals Spreadsheets'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    else:
        pass

    club_goal_link = driver.page_source.encode('ISO-8859-1')
    Club_goal_data = pd.read_html(club_goal_link, header =0)[0]
    Club_goal_date = f'{folder_path}/{club_choice}_{stat_choice}_List_{today}.csv'
    Club_goal_data.to_csv(Club_goal_date, encoding='ISO-8859-1')
    cgwb = pd.read_csv(Club_goal_date, encoding='ISO-8859-1')
    columns_to_drop = [0, 6]
    cgwb = cgwb.drop(cgwb.columns[columns_to_drop], axis=1)
    cgwb.to_csv(Club_goal_date, encoding='ISO-8859-1', index = False)

    cgwb = pd.read_csv(Club_goal_date, encoding='ISO-8859-1')
    x_axis = cgwb['Rank']
    y_axis = cgwb['Stat']
    names = cgwb['Player']
    fig, ax = plt.subplots()
    plt.bar(x_axis, y_axis, label = "Player")
    player_names = []
    for i, txt in enumerate(names):
        player_names.append(ax.annotate(txt, (x_axis[i], y_axis[i])))
    adjust_text(player_names, expand = (1.0, 3.5), arrowprops = {'color': 'blue'})
    plt.xlabel('Goals Scored') 
    plt.ylabel('Rank') 
    plt.title(f'{club_choice} {stat_choice} Stats:')
    plt.gcf().patch.set_edgecolor('b')
    plt.gcf().patch.set_linewidth(3)
    plt.show()         
    plt.savefig(f'{folder_path}/{club_choice} {stat_choice} Stats:'.png)
    
Premier_League_List = ["All Clubs", "Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton & Hove Albion", "Burnley", "Chelsea", "Crystal Palace", "Everton", "Fulham", "Liverpool", "Luton Town", "Manchester City", "Manchester United", "Newcastle United", "Nottingham Forest", "Sheffield United", "Tottenham Hotspur", "West Ham United", "Wolverhampton Wanderers"]

Stat_List = ["Goals", "Assists"]

club_label = customtkinter.CTkLabel(root, text="Select a Club:", font=("Roboto", 20))
club_label.grid(sticky='w', row= 2, pady=10, padx=10)

club_options = customtkinter.CTkComboBox(root, values=Premier_League_List)
club_options.grid(row=2, pady=10, padx=10)

Stat_label = customtkinter.CTkLabel(root, text="Select a Stat:", font=("Roboto", 20))
Stat_label.grid(sticky='w', row= 3, pady=0, padx=10)

stat_options = customtkinter.CTkComboBox(root, values=Stat_List)
stat_options.grid(row= 3, pady=12, padx=10)

button = customtkinter.CTkButton(root, text="Select", command=combo_selection)
button.grid(row=4, pady=12, padx=10)

root.mainloop()