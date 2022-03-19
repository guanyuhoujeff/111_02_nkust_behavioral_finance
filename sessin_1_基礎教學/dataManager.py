import pandas as pd

def clearSpace(value):
    return value.strip()
    
def getStockCodeList():
    price_data = pd.read_csv('./taiwan-index-price-data.txt', encoding='cp950')
    price_data['證券代碼'] = price_data['證券代碼'].apply(clearSpace)
    return price_data[['證券代碼', '簡稱']].drop_duplicates()
    
def getData(the_code):
    price_data = pd.read_csv('./taiwan-index-price-data.txt', encoding='cp950')
    price_data['證券代碼'] = price_data['證券代碼'].apply(clearSpace)
    price_data['簡稱'] = price_data['簡稱'].apply(clearSpace)
    target_data = price_data[price_data['證券代碼'] == the_code]
    target_data['ret'] = target_data['收盤價(元)'].diff(1)/target_data['收盤價(元)'].shift(1)
    target_data = target_data.dropna()
    target_data = target_data.reset_index(drop=True)
    return target_data

def getChipData(the_code):
    chip_data = pd.read_csv(
        './taiwan-index-chip-data.txt', 
        encoding='cp950').rename(columns={
        '證券名稱': '證券代碼',
    })

    chip_data['證券代碼'] = chip_data['證券代碼'].apply(clearSpace)
    chip_data['簡稱'] = chip_data['簡稱'].apply(clearSpace)
    target_data = chip_data[chip_data['證券代碼'] == the_code]
    target_data = target_data.dropna()
    target_data = target_data.reset_index(drop=True)
    return target_data

def getMarginData(the_code):
    margin_data = pd.read_csv(
        './taiwan-index-margin-data.txt', 
        encoding='cp950').rename(columns={
        '公司代碼': '證券代碼',
    })

    margin_data['證券代碼'] = margin_data['證券代碼'].apply(clearSpace)
    margin_data['簡稱'] = margin_data['簡稱'].apply(clearSpace)
    target_data = margin_data[margin_data['證券代碼'] == the_code]
    target_data = target_data.dropna()
    target_data = target_data.reset_index(drop=True)
    return target_data