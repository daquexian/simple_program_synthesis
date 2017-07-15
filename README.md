# simple_program_synthesis
FOPL 课期末大作业，仿照 [POPL'11 的一篇文章](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/popl11-synthesis.pdf)

类似于 Excel 里的自动填充，不过主要是对字符串的处理。

## 运行
建议用 Python3 运行（一开始的版本有愚蠢的错误在 Python3 下会报错只能用 Python2， 现在已经好了）
```
python3 final.py
```

## 说明
程序开始运行之后手动输入一些示例，格式为`原字符串,目标字符串`（不需要空格），每行一个示例，如输入：
```
Principles Of Programming Languages,POPL
International Business Machines,IBM
International Conference on Software Engineering,ICSE
```
然后再输入一个空行，接着新的字符串，如：
```
Asian Symposium on Programming Languages and Systems
```

就会得到
```
ASPLS
```
（其实这个会叫 APLAS）

或者输入
```
Mike Wallace,M.W
Alan Turing,A.T
Donald Knuth,D.K
```
然后输入
```
Barbara Liskov
```
就会得到
```
B.L
```

## 已知问题
输入的示例中的目标字符串较长（6-7个字符）时，速度会非常慢。因为`generate_loop`中对每一个满足 i < j < k 的 s[i:j] 和 s[j:k] 都尝试生成一个有限状态机，paper 中的确是这样的（并且 paper 中还有一些不正确的细节）
