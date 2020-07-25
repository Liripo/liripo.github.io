---
title: java更新word文档目录页码
mathjax: true
date: 2020-03-04 22:22:45
tags: word
categories: java
---
使用[aspose-words java](https://products.aspose.com/words/java)更新word文档目录页码。正版需要购买。

<!--more-->

代码，保存为文件word.java

```java
import com.aspose.words.Document;
public class word {
    public static void main(String[] args) throws Exception{
    Document doc = new Document("模板.docx"); // 更新目录
    doc.updateFields();
    doc.save("结果文件.docx");
   }
}
```

之后构建CLASSPATH环境变量。

添加`export CLASSPATH=~/.jar/aspose-words-15.8.0-jdk16.jar`到~/.bashrc

`source ~/.bashrc`

即可编译java源文件

```bash
#$CLASSPATH可以缺省
javac -cp $CLASSPATH word.java
java -cp $CLASSPATH word
```

