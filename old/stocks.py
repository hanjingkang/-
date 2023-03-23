#工作年限    月薪 年薪    每年投资股数(价值)  
# 1-3       1w/m 15w     10000(4.5w)          
# 3-5       2w/m 30w     20000(9w)
# 5-10      3w/m 40w     40000(18w)
# >10       4w/m 60w     50000(25w)



base = 0
newbuy=0

for i in range(0, 40):
    if(0 <= i <= 2):
        newbuy= 10000
    if(3 <= i <= 5):
        newbuy= 20000
    if(6 <= i <= 9):
        newbuy= 40000
    if(i > 9):
        newbuy= 50000
    """ if(i>=17):
        newbuy=0 """
    print("第",i+23,"岁 ","股票数量:",'%.2f'%float(base/10000),'w股',"价值:",'%.2f'%float(base*4.3/10000),'w元',"分红:",'%.2f'%float(base*4.3*0.07/10000),'w元',"新购入股票:",newbuy,"股 价值:",'%.2f'%float(newbuy*4.3/10000),'w元',"占分红比例 ",'%.2f'%float(newbuy/base)if base>0 else '0')
    base=(base+newbuy)*1.07

    

