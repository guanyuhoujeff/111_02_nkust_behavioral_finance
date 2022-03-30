# def function
def fibonacci(high_point, low_point): 
    # 邏輯組合
    diff = high_point - low_point
    raito_1 = diff*0.236
    raito_2 = diff*0.382
    raito_3 = diff*0.5
    raito_4 = diff*0.618
    raito_5 = diff*0.786
    
    # 輸出什麼
    return (
            low_point, 
            low_point + raito_1, 
            low_point + raito_2, 
            low_point + raito_3,
            low_point + raito_4,
            low_point + raito_5
           )