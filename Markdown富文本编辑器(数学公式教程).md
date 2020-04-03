![Markdown](https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Markdown-mark.svg/208px-Markdown-mark.svg.png)![Alt](https://avatar.csdn.net/7/7/B/1_ralf_hx163com.jpg =128x128)

------ **欢迎来到Markdown的世界 biu biu biu ~** ------
# 标题：本文主要讲解<font color=red>「文本样式」</font>
**斜体、加粗、高亮、删除线、引用、上下角标**
___
1. ① *斜体*；② _斜体_；
2. ① **加粗**；② __加粗__；
3. ==高亮文本==
4. ~~删除文本~~
5. >引用文本
6. H~2~O是液体
7. 2^10^运算结果是1024
___
**总结**
 1. 斜体：① `*`前面可以加空格，也可以不加；② `_`前面必选加空格；
 2. 加粗：① `**`前面可以加空格，也可以不加；② `__(两个下划线)`前面必选加空格；
 3. 高亮：`==`前面可加可不加空格；
 4. 删除：`~~`前面可加可不加空格；
 5. 引用：`>`前面可加可不加空格；

<font color=green> **上文代码块** </font>


## Markdown富文本编辑器（数学公式教程）
目录(使用`[toc]`)
[toc]

## 简单分类
    一般分为行内公式和行间公式。

### 行内公式示例如下
`$\Gamma(z) = \int_0^\infty t^{z-1}e^{-t}dt$`


    行内公式是要在公式的前后加”$“（美元）符号。
```
$\Gamma(z) = \int_0^\infty t^{z-1}e^{-t}dt$
```
### 行间公式实例如下
    行间公式一般是会**居中**的，与行内公式不同的地方是行间公式需要在公式的前后都加”$$“(双美元)符号。

`$$\Gamma(z) = \int_0^\infty t^{z-1}e^{-t}dt$$`

```
$$\Gamma(z) = \int_0^\infty t^{z-1}e^{-t}dt$$
```

## 希腊字母
    希腊字母的表示如下表格所示，其他字符如表格中所示。
| 名称   | 大写       |大| code    | 小写       |小| code    |
|-------|------------|--|--------|------------|--|--------|
| alpha | `$\Alpha$` |A | A      |`$\alpha$`  |α | \alpha |
| beta  | `$\Beta$`  |B | B      |`$\beta$`   |β | \beta  |
| gamma | `$\Gamma$` |Γ | \Gamma |`$\gamma$`  |γ | \delta |
| delta | `$\Delta$` |Δ | \Delta |`$\delta$`  |δ | \delta |
|epsilon|`$\Epsilon$`|E | E      |`$\epsilon$`|ϵ |\epsilon|
| zeta  | `$\Zeta$`  |Z |Z或\Zeta| `$\zeta$`  |ϵ | \zeta  |
| eta   | `$\Eta$`   |H |H或\Eta | `$\eta$`   |ζ | \eta   |
| theta | `$\Theta$` |Θ | \Theta | `$\theta$` |η | \theta |
| iota  | `$\Iota$`  |I |I或\Iota| `$\iota$`  |ι | \iota  |
| kappa | `$\Kappa$` |K |K或\Kappa| `$\kappa$`|κ | \kappa |
|lambda |`$\Lambda$` |Λ |\Lambda |`$\lambda$` |λ |\lambda |
| mu    | `$\Mu$`    |M | M或\Mu | `$\mu$`    |μ | \mu    |
| nu    | `$\Nu$`    |N | N或\Nu | `$\nu$`    |ν | \nu    |
| xi    | `$\Xi$`    |Ξ | \xi    | `$\xi$`    |ξ | \xi    |
|omicron|`$\Omicron$`|O | O      |`$\omicron$`|ο |\omicron|
| pi    | `$\Pi$`    |Π | \Pi    | `$\pi$`    |π | \pi    |
| rho   | `$P$`      |P | P      | `$\rho$`   |ρ | \rho   |
| sigma | `$\Sigma$` |Σ | \Sigma | `$\sigma$` |σ | \sigma |
| tau   | `$\Tau$`   |T | T或\Tau| `$\tau$`   |τ | \tau   |
|upsilon|`$\Upsilon$`|Υ |\Upsilon|`$\upsilon$`|u |\upsilon|
| phi   | `$\Phi$`   |Φ | \Phi   | `$\phi$`   |ϕ | \phi   |
| chi   | `$\Chi$`   |X | X或\Chi | `$\chi$`  |χ | \chi   |
| psi   | `$\Psi$`   |Ψ | \Psi   | `$\psi$`   |ψ | \psi   |
| omega | `$\Omega$` |Ω | \Omega | `$\omega$` |ω | \omega |
    或者查看这个补充表格。
| 说明        | 代码           | 结果            | 结果 |
|------------|---------------|-----------------|------|
| varepsilon | $\varepsilon$ | `$\varepsilon$` |ε     |
| vartheta	 | $\vartheta$   | `$\vartheta$`   |ϑ     |
| varpi	     | $\varpi$      | `$\varpi$`	   |ϖ     |
| varrho	 | $\varrho$     | `$\varrho$`	   |ϱ     |
| varsigma	 | $\varsigma$   | `$\varsigma$`   |ς     |
| varphi	 | $\varphi$     | `$\varphi$`	   |φ     |

## 上标与下标
    上标和下标分别使用\^ 与\_，例如`$x_i^2 $`的书写方式是：`x_i^2`。

    默认情况下，上、下标符号仅仅对下一个组起作用。一个组即单个字符或者使用{}(大括号)包裹起来的内容。如果使用`10^10` 表示的是`$10^10$`，而`10^{10}` 才可以表示为`$10^{10}$`。

    同时，大括号还能消除二义性，如x^5^6 将得到一个错误，必须使用大括号来界定`^`的结合性，如{x\^5}\^6表示的`${x^5}^6$` ：或者用x\^{5\^6}表示的`$x^{5^6}$` 。

## 括号
### 小括号与方括号
    使用原始的 **( )** ， **[ ]** 即可，如(2+3)[4+4] 可表示：```$(2+3)[4+4]$```。

    使用 **\left** (或 **\right** )使符号大小与邻近的公式相适应（该语句适用于所有括号类型），如 **\left(\frac{x}{y}\right)** 可表示```$\left(\frac{x}{y}\right)$ ```
：

### 大括号
    由于大括号{} 被用于分组，因此需要使用\\{和\\}表示大括号，也可以使用`\lbrace` 和`\rbrace`来表示。如`\{ab\}`或`\lbrace ab\rbrace`表示$\{ab\}$  与  $\lbrace ab\rbrace$。

### 尖括号
    区分于小于号和大于号，使用`\langle` 和`\rangle` 表示左尖括号和右尖括号。如 **\langle x \rangle**表示为：`$\langle x \rangle$` 。

### 上取整
    使用 **\lceil** 和 **\rceil** 表示。 如⌈x⌉，`$\lceil x \rceil$` 表示为： **\lceil x \rceil** 。

### 下取整
    使用`\lfloor` 和 `\rfloor` 表示。如⌊x⌋，`$\lfloor x \rfloor$`表示为： **\lfloor x \rfloor**

## 求和与积分
### 求和

`\sum` 用来表示求和符号∑ `$\sum$` ，其下标表示求和下限，上标表示上限。如:
$\sum\_{r=1}^n$表示：`$\sum_{r=1}^n$`。
 
$$\sum\_{r=1}^n$$表示：`$$\sum_{r=1}^n$$`

