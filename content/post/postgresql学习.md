Postgresql

<!--more-->
# 安装

windows，官网下载即可。

linux,

# 创建数据库，用户

sql语句以==；==结尾,一开始可以使用psql -U postgres进入初始的超级用户

生成新数据库`CREATE DATABASE mypsql;`

创建用户` CREATE USER liripo WITH PASSWORD '123456';`密码需加引号。

赋予权限`GRANT ALL PRIVILEGES ON DATABASE mysql TO liripo;`

之后即可使用`psql -U liripo -d mypsql -h localhost -p 5432`登录。

# 使用R语言与数据库连接

> 使用SQL语句查询数据。

使用三个R包`dplyr`,`DBI`,`odbc`以及`RPostgreSQL`连接postgresql

[教程](https://db.rstudio.com/)

连接数据库，默认端口，host与shell中psql命令一致。
```R
mypsql <- DBI::dbConnect(RPostgreSQL::PostgreSQL(), 
               dbname = "mypsql",
               user = "liripo",
               password = rstudioapi::askForPassword("Database password")
)
```
返回一个s4对象；考虑到安全性，Rstudio使用其api端口键入密码。【永远不要将其记录在分析脚本中或在控制台中键入密码。】

```R
> dbListTables(mypsql)
character(0)
```

可以看到数据库中还没有表，使用最常用的mtcars数据

```R
> dbWriteTable(mypsql,"mtcars", mtcars)
[1] TRUE
> dbListTables(mypsql)
[1] "mtcars"
>res <- dbSendQuery(mypsql, "SELECT * FROM mtcars")
>res_df <- dbFetch(res)#返回数据框
#返回后记得清除缓存
>dbClearResult（res）#避免浪费资源的关键步骤
#数据集过大应一块块获取。
dbGetQuery()为上述三个获取数据的整合。
```

试试检索数据耗时，==注：这里有无意义不清楚，而且数据量太小。==
```R
> system.time(res <- dbSendQuery(mypsql, "SELECT * FROM mtcars WHERE cyl = 4"))
用户 系统 流逝 
   0    0    0 
> system.time(filter(mtcars,cyl==4)%>%select(everything()))
用户 系统 流逝 
0.01 0.00 0.08 
```

试着用266M的数据测试，耗时分别为

```R
#有一点需注意，我使用的文件列数为56,203列，在R中操作列远没有行快。不知道数据库如何，还是作一番比较试试。

```

试试进入数据库操作` SELECT * FROM mtcars;`确实已经有这个表了。

odbc包可用于Rstudio连接数据库，在Rstudio访问数据库。

下载postgresql的windows[odbc](https://www.postgresql.org/ftp/odbc/versions/msi/)驱动

暂时没配置好，影响的是连接到数据库的速度。相较RPostgreSQL五到六倍??。

**交互**

```R
cyl_code <- "4"
dbGetQuery(mypsql, paste0("SELECT * FROM mtcars WHERE cyl = '", cyl_code ,"'"))
#上面的cyl_code就可以自由修改了呢。
```

但是又引发一个问题，故意写成`4 ;DROP TABLE mtcars`不就会删除数据库表了么。gg

修改成参数化查询。

```R
cyl <- dbSendQuery(con, "SELECT * FROM mtcars WHERE cyl = ?")
dbBind(cyl, list("4")) #使用dbBind()特定值执行查询
dbFetch(cyl)
dbClearResult(cyl)
#所以一步到位dbGetQuery有分险
```

使用dplyr操作数据库？？dbplyr自动转化R代码为SQL语句？？不需载入dbplyr,看到使用数据库自动载入？？

```R
library(dplyr)
airline_list <- tbl(con, "airlines") %>%
  collect  %>%
  split(.$name) %>%    # Field that will be used for the labels
  map(~.$carrier)      # Field that will be used for keys
```



