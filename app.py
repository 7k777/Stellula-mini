"""Stellula Mini：用于 Python 课程答辩的独立竞赛导航后端。

设计思路参考 Stellula 正式项目，但不复制生产账号、管理或部署代码。
运行：pip install -r requirements.txt，然后 uvicorn app:app --reload
接口文档：http://127.0.0.1:8000/docs
"""
from contextlib import asynccontextmanager
from pathlib import Path
import json
# import 用于导入模块；sqlite3 是 Python 自带的轻量数据库工具。
import sqlite3

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

# DB_FILE 是变量名；= 将右边的数据库路径保存给它；__file__ 代表当前文件路径。
DB_FILE = Path(__file__).with_name("stellula_mini.db")

# 演示数据是虚构的，仅用于课堂，不代表真实竞赛通知。
DEMO = [
    ("校园程序设计挑战赛（演示）", "计算机科学与技术,软件工程,网络工程", "编程,算法", "1,2,3,4", "学习编程与算法的竞赛示例"),
    ("大学生创意设计赛（演示）", "视觉传达设计,数字媒体艺术", "设计,创意", "1,2,3,4", "创意作品设计竞赛示例"),
    ("校园英语表达赛（演示）", "英语,商务英语", "英语,演讲", "1,2,3,4", "英语演讲竞赛示例"),
    ("大学生科技创新赛（演示）", "不限专业", "创新,科技", "1,2,3,4", "跨学科创新竞赛示例"),
]


# def 是 Python 定义函数的关键字；括号中是参数列表。注意：def 本身不是构造函数，__init__ 是类中常见的初始化方法。
def connect_db():
    """每次数据库操作新建连接；row_factory 让查询结果按列名访问。"""
# sqlite3.connect 打开数据库文件，文件不存在时会自动创建。
    connection = sqlite3.connect(DB_FILE)
# 让查询结果支持按字段名字读取，如 row["name"]。
    connection.row_factory = sqlite3.Row
# return 把连接对象返回给调用它的代码。
    return connection


# 初始化函数：建立竞赛数据表，如果表为空就插入虚构演示数据。
def init_db():
    """首次运行自动建表并插入演示商品（其实是竞赛）数据。"""
    with connect_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS competitions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                majors TEXT NOT NULL,
                interests TEXT NOT NULL,
                years TEXT NOT NULL,
                summary TEXT NOT NULL
            )
        """)
# SELECT COUNT(*) 统计行数；fetchone() 取一行；[0] 取第一列。
        number = db.execute("SELECT COUNT(*) FROM competitions").fetchone()[0]
# if 表示条件判断；== 判断两边是否相等，空表时才插入演示数据。
        if number == 0:
            db.executemany(
                "INSERT INTO competitions (name, majors, interests, years, summary) VALUES (?, ?, ?, ?, ?)",
                [(name, json.dumps(majors.split(","), ensure_ascii=False),
                  json.dumps(interests.split(","), ensure_ascii=False),
                  json.dumps([int(y) for y in years.split(",")]), summary)
                 for name, majors, interests, years, summary in DEMO],
            )


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Stellula Mini API", description="Python 课程演示后端", lifespan=lifespan)


# class 用来定义类；BaseModel 负责检查提交的数据类型和字段条件。
class CompetitionInput(BaseModel):
    """定义新增/修改竞赛时，前端必须提供的数据。"""
    name: str = Field(min_length=1, max_length=120)
    majors: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)
    years: list[int] = Field(default_factory=list)
    summary: str = ""


def parse_row(row):
    """数据库把列表保存成 JSON 字符串；返回接口前再还原成列表。"""
# dict() 把一条数据库记录转换成字典，字典通过“键”查找对应“值”。
    data = dict(row)
# for 循环依次访问三个字段；key 是当前字段名称。
    for key in ("majors", "interests", "years"):
# json.loads 把 JSON 文本重新转换成 Python 列表。
        data[key] = json.loads(data[key])
    return data


def all_competitions():
    with connect_db() as db:
# SELECT * 查所有字段；ORDER BY id 排序；fetchall() 获取全部查询结果。
        rows = db.execute("SELECT * FROM competitions ORDER BY id").fetchall()
    return [parse_row(row) for row in rows]


# @app.get 是路由装饰器：访问这个 URL 时，框架会调用下面的函数。
@app.get("/")
def home():
    return {"message": "欢迎使用 Stellula Mini", "docs": "/docs"}


@app.get("/competitions")
def list_competitions(q: str = ""):
    """查询：未输入关键字时返回全部，输入后按名称或简介筛选。"""
    result = all_competitions()
# strip() 清除字符串首尾空格；只有关键词非空才执行筛选。
    if q.strip():
# lower() 把英文字母转成小写，搜索时可以忽略英文大小写。
        keyword = q.strip().lower()
        result = [c for c in result if keyword in (c["name"] + c["summary"]).lower()]
    return result


@app.get("/competitions/match")
# 匹配流程：for 遍历每条赛事，if/elif 判断专业，any 检查兴趣，最后 sorted 按分数排序。
# 这里用固定规则评分，不涉及机器学习模型训练。
def match_competitions(
    major: str = "",
    year: int | None = Query(default=None, ge=1, le=8),
    interest: str = "",
):
    """简化版规则匹配：专业占 70 分，兴趣占 30 分，年级只做资格过滤。

    正式 Stellula 还包含更复杂的专业映射与关联规则；
    这里保留适合课堂解释的核心思想。
    """
    # [] 表示空列表，之后用 append() 依次放入匹配结果。
    results = []
    # for ... in ... 表示依次取出每一个元素，item 是当前竞赛。
    for item in all_competitions():
        # 指定年级时，不在可参赛年级里的赛事直接跳过。
# and 表示条件同时满足；如果年级不在允许列表中，就不推荐。
        if year is not None and item["years"] and year not in item["years"]:
# continue 跳过当前赛事，进入下一轮 for 循环。
            continue
        reasons = []
        major_score = 0
        interest_score = 0
        if major:
            if major.strip() in item["majors"]:
                major_score = 70
# append() 的作用是向列表末尾添加一条推荐理由。
                reasons.append("专业直接匹配")
            elif "不限专业" in item["majors"]:
                major_score = 25
                reasons.append("面向多个专业开放")
# any() 只要发现至少一个兴趣标签符合条件就返回 True。
        if interest and any(interest.strip().lower() in x.lower() for x in item["interests"]):
            interest_score = 30
            reasons.append("兴趣方向相关")
        # = 是赋值；+ 把专业分与兴趣分相加，得到匹配总分。
        score = major_score + interest_score
        # 无筛选条件时显示全部；有专业/兴趣条件时只显示相关项。
        if (major or interest) and score == 0:
            continue
# **item 展开原字典的键值，再附上评分与理由；append 将其放进列表。
        results.append({**item, "match_score": score, "match_reasons": reasons})
    # return 返回排序结果；sorted 负责排序；lambda 定义临时的排序规则。
    return sorted(results, key=lambda c: (-c["match_score"], c["id"]))


@app.get("/competitions/{competition_id}")
def get_competition(competition_id: int):
    with connect_db() as db:
        row = db.execute("SELECT * FROM competitions WHERE id = ?", (competition_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="竞赛不存在")
    return parse_row(row)


# POST 表示新增数据；状态码 201 表示创建成功。
@app.post("/competitions", status_code=201)
def add_competition(item: CompetitionInput):
    """增加：使用 SQL 参数占位符，避免直接拼接输入内容。"""
    with connect_db() as db:
        cursor = db.execute(
            "INSERT INTO competitions (name, majors, interests, years, summary) VALUES (?, ?, ?, ?, ?)",
            (item.name, json.dumps(item.majors, ensure_ascii=False),
             json.dumps(item.interests, ensure_ascii=False), json.dumps(item.years), item.summary),
        )
        new_id = cursor.lastrowid
    return get_competition(new_id)


# PUT 用于更新一条指定编号的竞赛；编号在 URL 路径里传入。
@app.put("/competitions/{competition_id}")
def update_competition(competition_id: int, item: CompetitionInput):
    """修改：先检查目标存在，再使用 UPDATE 更新其字段。"""
    get_competition(competition_id)
    with connect_db() as db:
        db.execute(
            "UPDATE competitions SET name=?, majors=?, interests=?, years=?, summary=? WHERE id=?",
            (item.name, json.dumps(item.majors, ensure_ascii=False),
             json.dumps(item.interests, ensure_ascii=False), json.dumps(item.years),
             item.summary, competition_id),
        )
    return get_competition(competition_id)


# DELETE 表示删除一条指定编号的竞赛。
@app.delete("/competitions/{competition_id}")
def delete_competition(competition_id: int):
    """删除：按主键删除，返回简单的提示信息。"""
    get_competition(competition_id)
    with connect_db() as db:
        db.execute("DELETE FROM competitions WHERE id = ?", (competition_id,))
    return {"message": "删除成功"}
