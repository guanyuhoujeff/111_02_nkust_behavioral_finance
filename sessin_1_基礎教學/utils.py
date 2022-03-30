import pandas as pd

rename_column_maplist = {
    ## price
    '證券代碼' : "code", 
    '簡稱' : 'name', 
    'TSE新產業_名稱' : 'new_industry', 
    'TEJ產業_名稱' : 'industry', 
    '年月日'  : "date", 
    '開盤價(元)': 'open',
    '最高價(元)': 'high',
    '最低價(元)': 'low',
    '收盤價(元)' : 'close', 
    '成交量(千股)' : 'volume', 
    '報酬率％' : 'return', 
    '週轉率％' : "turn_over", 
    '市值(百萬元)' : "size", 
    '股價淨值比-TSE': "PB_TSE", 
    
    ### ifrs
    '公司': 'code',
    '年/月': 'date_year_month',
    '營收成長率': 'YOY',
    '總資產成長率': "TAR",
    
    ### institution
    '證券名稱': 'code',
    '外資週轉率%' : 'foreign_turnover_rate',
    '投信週轉率%' : 'trust_turnover_rate',
    '自營商週轉率%' : 'broker_turnover_rate',
    
    ## margin
    '公司代碼': 'code',
    '券資比': 'short_margin_ratio',
    '融資餘額(張)' : 'margin_balance',
    '融券餘額(張)' : 'short_balance',
}

def cleanStringSpace(value):
    return str(value).strip()

def StringToFloat(value):
    return float(value)

def shortMarginConvert(value):
    if value == 0:
        return 0
    else:
        return 1/(value)*10000

def dateToDateYearMonth(date_value):
    return int(str(date_value)[:6])
    
def getStockData():
    ## 讀取資料
    price_data = pd.read_csv('../data/price.txt',  encoding='cp950')
    ifrs_data = pd.read_csv('../data/ifrs.txt',  encoding='cp950')
    institution_data = pd.read_csv('../data/institution.txt',  encoding='cp950')
    margin_data = pd.read_csv('../data/margin.txt',  encoding='cp950')

    # 改欄位名
    price_data.rename(columns=rename_column_maplist, inplace=True)
    ifrs_data.rename(columns=rename_column_maplist, inplace=True)
    institution_data.rename(columns=rename_column_maplist, inplace=True)
    margin_data.rename(columns=rename_column_maplist, inplace=True)

    # 代號
    price_data['code'] = price_data['code'].apply(cleanStringSpace)
    institution_data['code'] = institution_data['code'].apply(cleanStringSpace)
    margin_data['code'] = margin_data['code'].apply(cleanStringSpace)
    ifrs_data['code'] = ifrs_data['code'].apply(cleanStringSpace)

    # 名字
    price_data['name'] = price_data['name'].apply(cleanStringSpace)
    institution_data['name'] = institution_data['name'].apply(cleanStringSpace)
    margin_data['name'] = margin_data['name'].apply(cleanStringSpace)
    ifrs_data['name'] = ifrs_data['name'].apply(cleanStringSpace)

    # 產業
    price_data['new_industry'] = price_data['new_industry'].apply(cleanStringSpace)
    price_data['industry'] = price_data['industry'].apply(cleanStringSpace)

    # 財報
    price_data['PB_TSE'] = price_data['PB_TSE'].apply(StringToFloat)
    ifrs_data['YOY'] = ifrs_data['YOY'].apply(StringToFloat)
    ifrs_data['TAR'] = ifrs_data['TAR'].apply(StringToFloat)

    ## 法人週轉率
    institution_data['intitution_turnover_rate'] = institution_data[[
        'foreign_turnover_rate', 
        'trust_turnover_rate', 
        'broker_turnover_rate']].sum(1)

    ## 資券比
    margin_data['margin_short_ratio'] = margin_data['short_margin_ratio'].apply(shortMarginConvert)
    
    ## 合併財報資料
    price_data['date_year_month'] = price_data['date'].apply(dateToDateYearMonth)
    merge_data = price_data.merge(ifrs_data, 
                                  on=['code', 'name', 'date_year_month'], 
                                  how='outer')
    
    ## 再根據時間排序一下
    merge_data = merge_data.sort_values(by=['date_year_month', 'date'])
    merge_data = merge_data.ffill()
    
    ## 全部合併
    stock_data =  merge_data.merge(
        institution_data, on=['code', 'name', 'date'] ## 法人週轉率
    ).merge(
        margin_data, on=['code', 'name', 'date']      ## 資券比
    )
    return stock_data
