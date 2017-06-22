# simple_program_synthesis
FOPL 课期末大作业，仿照 [POPL'11 的一篇文章](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/popl11-synthesis.pdf)

类似于 Excel 里的自动填充，不过主要是对字符串的处理。

## 运行
请使用 Python3
```
Python final.py
```

## 说明
程序开始运行之后手动输入一些示例，格式为`原字符串,目标字符串`，每行一个示例，如输入：
```
Central Intelligence Agency,CIA
National Security Agency,NSA
World Wide Web,WWW
```
然后再输入一个空行，接着新的字符串，如：
```
British Broadcasting Corporation
```

就会得到
```
BBC
```

实现的很垃圾，paper 里的很多功能还没完全实现，所以可能碰到奇怪的情况，有空（不知道是什么时候了）再改
