from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pymssql


def Spyder():
    soup = BeautifulSoup(htmltext, 'html.parser')
    # 爬下日期
    Date_data = soup.find_all('div', class_='item__month')
    # 爬下地區
    Area_data = soup.find_all('span', class_='item__place-area')
    # 爬下地址
    Address_data = soup.find_all('span', class_='item__place-address')
    # 爬下詳細資料(屋齡、格局等等)
    Detail_data = soup.find_all('div', class_='item__mix')
    # 爬下地坪和建坪
    Floor_Jianping_data = soup.find_all('div', class_="item__space")
    # 爬下單價和總價
    Price_data = soup.find_all('div', class_="item__price")

    Detail = []
    for i in Detail_data:
        i = i.text
        Detail.append(i)

    Floor_Jianping = []
    for i in Floor_Jianping_data:
        i = i.text
        Floor_Jianping.append(i)

    Price = []
    for i in Price_data:
        i = i.text
        Price.append(i)

    for i in Date_data:
        i = i.text
        Date.append(i)

    for i in Area_data:
        i = i.text
        Area.append(i)

    for i in Address_data:
        i = i.text
        Address.append(i)

    for i in Detail_data:
        i = i.text
        Detail.append(i)

    for i in range(0, int(len(Detail) / 2)):
        if len(Detail[i].split()) == 4 and len(Floor_Jianping[i].split()) >= 2 and '單價' in Price[i].split()[
            0] and '地' in Floor_Jianping[i].split()[0] and '建' in Floor_Jianping[i].split()[1]:
            Types.append(Detail[i].split()[0])

            if "個月" in Detail[i].split()[1]:
                Age1 = Detail[i].split()[1].replace("個月", '').replace(",", "")
                temp = float(Age1)
                Age.append(float(temp / 12))

            elif "年" in Detail[i].split()[1]:
                Age2 = Detail[i].split()[1].replace("年", '').replace(",", "")
                Age.append(Age2)
            else:
                Age3 = Detail[i].split()[1].replace("天", '').replace(",", "")
                temp1 = float(Age3)
                Age.append(float(temp1 / 365))

            Pattern.append(Detail[i].split()[2])
            Build.append(Detail[i].split()[3])

            Floor1 = Floor_Jianping[i].split()[0].replace("地", "").replace("坪", "").replace(",", "")
            Floor.append(float(Floor1))

            Floor2 = Floor_Jianping[i].split()[1].replace("建", "").replace("坪", "").replace(",", "")
            Jianping.append(float(Floor2))

            Price1 = Price[i].split()[0].replace("成交單價", "").replace("萬/坪", "").replace(",", "")
            Unit_Price.append(float(Price1))

            Price2 = Price[i].split()[1].replace("成交總價", "").replace("萬", "").replace(",", "")
            Toatal_Price.append(float(Price2))

        else:
            global t
            global Del
            Del.append(t + i)


def look():
    print(len(Date))
    print(len(Area))
    print(len(Address))
    print(len(Types))
    print(len(Age))
    print(len(Pattern))
    print(len(Build))
    print(len(Floor))
    print(len(Build))
    print(len(Jianping))
    print(len(Unit_Price))
    print(len(Toatal_Price))


for city in range(0, 21):
    Date = []
    Area = []
    Address = []
    Types = []
    Age = []
    Pattern = []
    Build = []
    Floor = []
    Jianping = []
    Unit_Price = []
    Toatal_Price = []
    t = 0
    Del = []

    driver = webdriver.Chrome()
    driver.get(
        f"https://www.rakuya.com.tw/realprice/result?city={city}&sell_type=apartment%2CelevatorBuilding%2CdetachedHouse%2Cstudio%2Cstore%2Cbusiness&sort=11")
    time.sleep(.5)
    htmltext = driver.page_source
    driver.close()
    soup = BeautifulSoup(htmltext, 'html.parser')
    number = soup.find_all('p', class_="pages")
    All = []
    for i in number:
        i = i.text
        All.append(i)
    for i in All:
        page = i.split()[3]

    driver = webdriver.Chrome()
    for i in range(1, int(page)+1):
        if i % 800 == 0:
            driver.close()
            driver = webdriver.Chrome()
        driver.get(
            f"https://www.rakuya.com.tw/realprice/result?city={city}&sell_type=apartment%2CelevatorBuilding%2CdetachedHouse%2Cstudio%2Cstore%2Cbusiness&sort=11&page={i}")
        time.sleep(.5)
        htmltext = driver.page_source
        Spyder()
        t += 20
    driver.close()

    # look()
    for i in range(len(Del) - 1, -1, -1):
        del Date[Del[i]]
        del Area[Del[i]]
        del Address[Del[i]]

    conn = pymssql.connect(host='', user='', password='', database='')
    cursor = conn.cursor()

    for i in range(0, len(Date)):
        cursor.executemany("INSERT INTO House_New values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [(Date[i], Area[i],Address[i],Types[i],Age[i],Pattern[i],Build[i],Floor[i],Jianping[i],Unit_Price[i],Toatal_Price[i])])
        conn.commit()

    conn.close()

print("完成")