# Stellula Mini｜Python 零基础源码讲解（答辩专用）

这份讲义对应仓库里的 `app.py`。按“先认语法，再理解函数，最后解释运行流程”学习。

## 1. 从最基础的 Python 符号开始

- `#`：注释。写给人看的说明，不会作为代码执行。
- `=`：赋值，把右边的值保存到左边变量中，例如 `score = 0`。
- `==`：比较是否相等，例如 `number == 0`。
- `:`：表示开启一段缩进代码，如函数、条件、循环或类定义。
- `def`：**定义函数**。例如 `def connect_db():` 定义名为 `connect_db` 的函数，括号里可以放参数。
- **不要把 `def` 说成构造函数！** `class` 用来定义类；`__init__` 是类的常见初始化方法。
- `return`：从函数返回一个结果，函数在此结束。
- `if`：如果条件成立就执行缩进代码。
- `elif`：上面的 `if` 不成立时再检查另一条件。
- `else`：前面条件都不成立时执行。
- `for x in items:`：依次取出 `items` 中的元素，每次赋给 `x`。
- `continue`：跳过本轮循环，处理下一个元素。
- `in`：判断一个元素是否存在于列表中，也可判断文本是否包含子串。
- `and`：两边条件都成立才成立；`or`：至少有一个条件成立。
- `not`：逻辑取反；`is None`：判断是否为“没有值”。
- `[]`：列表，例如 `[1, 2, 3]`。
- `{}`：字典，例如 `{"name": "比赛A", "score": 70}`。
- `()`：可用在函数调用或表示元组。
- `list[str]`：类型标注，表示由字符串组成的列表。
- `str` 是字符串类型；`int` 是整数类型。
- `import`：导入模块；`from ... import ...` 从模块里导入指定名称。

## 2. 导入的库分别做什么？

`sqlite3`：Python 自带的 SQLite 数据库模块，连接数据库并执行 SQL。

`json`：将 Python 列表、字典转成 JSON 字符串，或从 JSON 字符串还原。

`pathlib.Path`：处理文件位置。`__file__` 是当前代码文件位置；`with_name("stellula_mini.db")` 在同目录生成数据库路径。

`FastAPI`：定义 Web API；`HTTPException` 返回 HTTP 错误；`Query` 规定查询参数条件。

`BaseModel`：定义请求数据的结构；`Field`：规定字段长度、默认值等。

`asynccontextmanager`：配合 Web 框架在应用启动与关闭时执行指定逻辑。

## 3. 主要函数逐个讲

### connect_db()

`def connect_db():` 定义数据库连接函数。

`sqlite3.connect(DB_FILE)`：打开数据库文件，不存在就新建。

`connection.row_factory = sqlite3.Row`：让查询得到的行能使用 `row["name"]` 访问。

`return connection`：把连接返回给调用者。

**老师问：为什么要单独写函数？** 因为多个功能都要打开数据库，集中成函数可以复用代码。

### init_db()

`with connect_db() as db:`：开始数据库操作作用域。这里的上下文管理会在正常退出时提交事务，出错时回滚；注意它本身**不会自动关闭 sqlite3 连接**。

`CREATE TABLE IF NOT EXISTS competitions`：表不存在就创建。字段中，`id` 是自增主键，`name` 是竞赛名称。

`SELECT COUNT(*)`：统计已有多少条记录。

`fetchone()[0]`：读取第一行的第一列。

`if number == 0:`：如果没有数据，插入四条虚构的课堂演示竞赛。

`executemany(...)`：一次执行多组插入参数；SQL 中 `?` 是占位符。

`json.dumps(...)`：把列表保存成数据库可存储的 JSON 文本。演示数据中的 `split(",")` 是根据英文逗号拆分文本。

### lifespan() 与 app

`async def lifespan(app: FastAPI):`：定义异步生命周期函数。

`init_db()`：启动时初始化数据库。

`yield`：把控制权交回框架，继续运行服务。

`app = FastAPI(...)`：创建 Web 后端应用对象。

### CompetitionInput

`class CompetitionInput(BaseModel):`：定义一个类，作为新增或修改竞赛时的输入模板。

`name: str`：名称应是字符串；`Field(min_length=1, max_length=120)` 规定长度范围。

`majors: list[str]`：专业列表由字符串组成。

`Field(default_factory=list)`：未填写时生成新的空列表。

`years: list[int]`：参赛年级是整数列表。

### parse_row(row)

函数参数 `row` 是数据库查询结果中的一行。

`dict(row)`：把这一行变成字典。

`for key in ("majors", "interests", "years"):`：依次处理三个字段。

`json.loads(data[key])`：把数据库中的 JSON 字符串恢复为 Python 列表。

### all_competitions()

`SELECT * FROM competitions ORDER BY id`：读取竞赛表所有字段，按编号排序。

`fetchall()`：获取所有结果。

`[parse_row(row) for row in rows]`：列表推导式，意思是“把每一行经过 parse_row 处理，组成一个新列表”。

### home() 与 list_competitions()

`@app.get("/")` 是路由装饰器：访问网站根路径就执行 `home()`。

`return {"message": ..., "docs": ...}`：返回字典，FastAPI 转换为 JSON。

`q: str = ""`：查询关键词参数，默认空字符串。

`q.strip()`：去掉两端空格。

`lower()`：把英文转小写，使搜索不区分英文大小写。

`keyword in (c["name"] + c["summary"]).lower()`：检查关键词是否包含在竞赛名称与简介中。

### match_competitions()：重点中的重点

`major`：专业；`year`：年级；`interest`：兴趣。

`Query(default=None, ge=1, le=8)`：年级可以不填；填写时须在 1～8 之间。

`results = []`：新建空列表存储结果。

`for item in all_competitions():`：遍历每条竞赛。

如果输入年级不在竞赛允许年级里，用 `continue` 跳过它。

`major_score = 0`、`interest_score = 0`：先初始化评分。

`if major.strip() in item["majors"]:`：专业直接匹配，得 70 分。

`elif "不限专业" in item["majors"]:`：跨专业可参加，作为拓展项得 25 分。

`any(... for x in item["interests"])`：只要有一个兴趣标签包含输入关键词，就满足兴趣匹配，得 30 分。

`score = major_score + interest_score`：专业分与兴趣分相加。

`reasons.append("...")`：向推荐理由列表增加一条说明。

`results.append({**item, ...})`：把原竞赛字典展开，再添加分数与原因。

`sorted(results, key=lambda c: (-c["match_score"], c["id"]))`：按分数从高到低，分数相同再按编号从小到大排列。`lambda` 是这里临时定义的小函数。

**老师问：这是机器学习吗？** 不是。Mini 使用固定规则进行加权匹配，没有使用训练数据来学习模型参数。正式 Stellula 的关联规则更复杂。

### get_competition(competition_id)

`competition_id: int`：函数接收整数类型的竞赛编号。

`SELECT * FROM competitions WHERE id = ?`：只查询指定编号的竞赛。

`fetchone()`：读取一条结果。

`if row is None:`：如果找不到数据，`raise HTTPException(status_code=404, ...)` 返回“竞赛不存在”。

### add_competition(item)

`@app.post(..., status_code=201)`：POST 用于新增，201 表示创建成功。

`item: CompetitionInput`：输入须符合前面定义的数据结构。

`INSERT INTO ... VALUES (?, ...)`：向数据库插入新记录。

`cursor.lastrowid`：获得新记录的编号。

`return get_competition(new_id)`：返回刚创建的竞赛。

### update_competition(competition_id, item)

`@app.put(...)`：PUT 用于提交整份更新后的竞赛数据。

先调用 `get_competition` 确保目标存在。

`UPDATE competitions SET ... WHERE id=?`：修改指定编号对应的数据库记录。

最后再读取一次，返回更新后的数据。

### delete_competition(competition_id)

`@app.delete(...)`：DELETE 用于删除资源。

先检查编号，再执行 `DELETE FROM competitions WHERE id = ?`。

返回 `{"message": "删除成功"}`。

## 4. 从输入到输出，一次请求经历什么？

以“按专业匹配”为例：

1. 学生在页面中输入“软件工程”和“算法”。
2. 浏览器请求 `GET /competitions/match?major=软件工程&interest=算法`。
3. FastAPI 找到与 URL 对应的 `match_competitions` 函数。
4. 函数读取 SQLite 中的竞赛列表。
5. `for` 循环逐条检查，`if` 判断条件。
6. 计算专业分、兴趣分，加入匹配理由。
7. `sorted` 将结果按分数排序。
8. `return` 把列表交给 FastAPI，作为 JSON 返回。

## 5. 答辩常问五题（参考答案）

**问：Python 在项目中负责什么？** 答：负责后端业务逻辑，包括接收输入、读取数据、条件筛选、评分和返回结果。

**问：为什么有这么多 def？** 答：将不同功能拆成函数，减少重复代码，便于测试和维护。

**问：什么是增删改查？** 答：增是 INSERT，删是 DELETE，改是 UPDATE，查是 SELECT；分别对应项目的新增、删除、修改和查看竞赛。

**问：数据库与列表有什么不同？** 答：列表在程序运行时保存在内存；SQLite 写到数据库文件，重启后仍可读取。

**问：展示的正式站点与 Mini 有什么不同？** 答：正式站点是持续运营的产品，Mini 是独立课程实现，保留竞赛筛选与 Python 数据处理的核心思想，用虚构数据教学，不包含生产账号和私有前端。

---

**学习建议：** 先把 `def`、`if`、`for`、`list`、`dict`、`return` 熟练说清楚，再讲 FastAPI 的路由装饰器。答辩时保持诚实：能讲清 Mini 的真实实现，比记大量听不懂的术语可靠。
