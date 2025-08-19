import bs4
import requests
import csv

def GetTyphoonName(soup):
    typhoon_name=soup.find("div", class_="TYNAME").text
    start=typhoon_name.find("(") + len("(")
    end=typhoon_name.find(")")
    typhoon_name_f=typhoon_name[start:end]
    return typhoon_name_f
def GetPageContent(url):
    page = requests.get(url, headers={"Acept-Language":"en-US"})
    return bs4.BeautifulSoup(page.text,"html.parser")
def CrawlDataTyphoon():
    output_rows=[]
    for typhoon_number in range(1,27):
        typhoon_number_f = str(typhoon_number).zfill(2)
        print(typhoon_number_f)
        url = 'https://agora.ex.nii.ac.jp/digital-typhoon/summary/wnp/l/2024'+typhoon_number_f+'.html.en'
        soup=GetPageContent(url)
        typhoon_name = GetTyphoonName(soup)
        
        table=soup.find("table",class_="TRACKINFO")
        for table_row in table.find_all('tr'):
            columns = table_row.find_all('td')
            output_row=[]
            output_row.append(typhoon_number_f)
            output_row.append(typhoon_name)
            for column in columns:
                output_row.append(column.text.replace("\n\t\t",""))

            if (len(output_row) > 2):
                output_rows.append(output_row)
            # print(output_row) 
    return output_rows
def ExportCsv(output_rows):
    with open('output.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output_rows)
output_rows = CrawlDataTyphoon()
ExportCsv(output_rows)