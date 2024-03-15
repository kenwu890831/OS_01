# OS_01

方法一，用一班的bubble sort 直接排序

方法二，方法三，方法四的切割，將N個數目字切成k份，我的方法是N/K有小數的話無條件進位，即可將全部資料放入，切完執行 bubble sort。

方法二，方法三，方法四bubble sort完之後放入queue依序按照規定的方式進入process、thread，並且使用manager 管理queue，造成 race condition 的問題。
  
