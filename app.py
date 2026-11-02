"""Stellula Mini：用于 Python 课程答辩的独立竞赛导航后端。

设计思路参考 Stellula 正式项目，但不复制生产账号、管理或部署代码。
运行：pip install -r requirements.txt，然后 uvicorn app:app --reload
接口文档：http://127.0.0.1:8000/docs
"""
from contextlib import asynccontextmanager
from pathlib import Path
import json
import sqlite3

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

DB_FILE = Path(__file__).with_name("stellula_mini.db")

# 演示数据是虚构的，仅用于课堂，不代表真实竞赛通知。
DEMO = [
    ("校园程序设计挑战赛（演示）", "计算机科学与技术,软件工程,网络工程", "编程,算法", "1,2,3,4", "学习编程与算法的竞赛示例"),
    ("大学生创意设计赛（演示）", "视觉传达设计,数字媒体艺术", "设计,创意", "1,2,3,4", "创意作品设计竞赛示例"),
    ("校园英语表达赛（演示）", "英语,商务英语", "英语,演讲", "1,2,3,4", "英语演讲竞赛示例"),
    ("大学生科技创新赛（演示）", "不限专业", "创新,科技", "1,2,3,4", "跨学科创新竞赛示例"),
]


def connect_db():
    """每次数据库操作新建连接；row_factory 让查询结果按列名访问。"""
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    return connection


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
        number = db.execute("SELECT COUNT(*) FROM competitions").fetchone()[0]
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


class CompetitionInput(BaseModel):
    """定义新增/修改竞赛时，前端必须提供的数据。"""
    name: str = Field(min_length=1, max_length=120)
    majors: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)
    years: list[int] = Field(default_factory=list)
    summary: str = ""


def parse_row(row):
    """数据库把列表保存成 JSON 字符串；返回接口前再还原成列表。"""
    data = dict(row)
    for key in ("majors", "interests", "years"):
        data[key] = json.loads(data[key])
    return data


def all_competitions():
    with connect_db() as db:
        rows = db.execute("SELECT * FROM competitions ORDER BY id").fetchall()
    return [parse_row(row) for row in rows]


@app.get("/")
def home():
    return {"message": "欢迎使用 Stellula Mini", "docs": "/docs"}


@app.get("/competitions")
def list_competitions(q: str = ""):
    """查询：未输入关键字时返回全部，输入后按名称或简介筛选。"""
    result = all_competitions()
    if q.strip():
        keyword = q.strip().lower()
        result = [c for c in result if keyword in (c["name"] + c["summary"]).lower()]
    return result


@app.get("/competitions/match")
def match_competitions(
    major: str = "",
    year: int | None = Query(default=None, ge=1, le=8),
    interest: str = "",
):
    """简化版规则匹配：专业占 70 分，兴趣占 30 分，年级只做资格过滤。

    正式 Stellula 还包含更复杂的专业映射与关联规则；
    这里保留适合课堂解释的核心思想。
    """
    results = []
    for item in all_competitions():
        # 指定年级时，不在可参赛年级里的赛事直接跳过。
        if year is not None and item["years"] and year not in item["years"]:
            continue
        reasons = []
        major_score = 0
        interest_score = 0
        if major:
            if major.strip() in item["majors"]:
                major_score = 70
                reasons.append("专业直接匹配")
            elif "不限专业" in item["majors"]:
                major_score = 25
                reasons.append("面向多个专业开放")
        if interest and any(interest.strip().lower() in x.lower() for x in item["interests"]):
            interest_score = 30
            reasons.append("兴趣方向相关")
        score = major_score + interest_score
        # 无筛选条件时显示全部；有专业/兴趣条件时只显示相关项。
        if (major or interest) and score == 0:
            continue
        results.append({**item, "match_score": score, "match_reasons": reasons})
    return sorted(results, key=lambda c: (-c["match_score"], c["id"]))


@app.get("/competitions/{competition_id}")
def get_competition(competition_id: int):
    with connect_db() as db:
        row = db.execute("SELECT * FROM competitions WHERE id = ?", (competition_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="竞赛不存在")
    return parse_row(row)


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


@app.delete("/competitions/{competition_id}")
def delete_competition(competition_id: int):
    """删除：按主键删除，返回简单的提示信息。"""
    get_competition(competition_id)
    with connect_db() as db:
        db.execute("DELETE FROM competitions WHERE id = ?", (competition_id,))
    return {"message": "删除成功"}
