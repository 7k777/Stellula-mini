# Stellula ✦

<p align="center">
  <strong>Find the competitions that actually fit you.</strong><br>
  <sub>面向大学生的竞赛发现、匹配与参赛记录平台</sub>
</p>

<p align="center">
  <a href="https://stellula.cloud">Live Product</a>
  ·
  <a href="#中文">中文</a>
  ·
  <a href="#english">English</a>
</p>

---

## 中文

### Stellula 是什么？

**Stellula** 是一个面向大学生的竞赛发现平台。

它想解决的不是“网上有没有竞赛信息”，而是一个更具体的问题：

> **我学这个专业，现在到底有哪些比赛适合我？**

竞赛信息并不少，但它们常常散落在不同的官网、学校通知、公众号、社交平台和往届经验里。对于刚开始接触竞赛的学生来说，真正困难的往往不是找到一个比赛名称，而是判断：

- 这个比赛和我的专业有没有关系？
- 我现在的年级能不能参加？
- 为什么它会被推荐给我？
- 哪个链接才是官方入口？
- 我参加过什么，之后还能不能找回来？

Stellula 围绕这条学生路径设计：

> **发现 → 判断 → 参赛 → 记录 → 回看**

它希望把“找比赛”从一次临时搜索，慢慢变成一份属于自己的大学竞赛轨迹。

### 核心体验

#### 竞赛发现

根据专业、年级、兴趣与地区等信息，帮助学生缩小搜索范围，并优先展示更相关的竞赛。

#### 可解释匹配

推荐不应该只是一个黑盒结果。Stellula 尽量保留结构化的匹配依据，让学生能够理解一个比赛为什么出现在结果中。

#### 赛事详情与官方信息

赛事页面整理比赛简介、适合方向、参赛条件及官方资源。Stellula 不替代官方报名渠道，而是帮助用户更快抵达可信的信息来源。

#### 个人竞赛墙

用户可以记录自己想参加、已经参加以及完成过的比赛，让几年大学经历不必只剩下一张成绩单。

竞赛墙更接近一条个人经历时间线，而不是排行榜。

### 产品原则

- **先有用，再聪明。** 基础匹配逻辑应该独立成立，AI 不是前提。
- **官方来源优先。** 重要赛事信息尽可能指向可验证的官方来源。
- **推荐需要解释。** 用户应该知道“为什么是它”。
- **为普通学生设计。** 不假设用户已经熟悉竞赛体系。
- **经历本身值得被记录。** 奖项重要，但参赛经历不应该被简单压缩成“成功 / 失败”。
- **隐私默认收紧。** 个人参赛记录不应因为注册账号就自动成为公开数据。

### 技术方向

当前正式版本主要采用：

- **Backend:** Python / FastAPI
- **Database:** SQLite
- **Frontend:** HTML / CSS / JavaScript
- **Deployment:** Linux / Uvicorn / Nginx

线上版本还包含账号、数据维护、提醒、安全与部署等生产环境能力。

### 关于这个仓库

这个仓库是 **Stellula 的公开项目展示与课程提交仓库**。

它**不是** Stellula 正式生产仓库，也不会作为线上版本的源码镜像。

目前这里主要用于：

- 介绍 Stellula 的产品目标与设计思路；
- 记录适合公开的项目说明；
- 作为 Python 课程设计的展示入口；
- 在课程提交阶段提供一份经过整理、可独立运行的 **Mini Python 后端实现**。

#### 计划公开的课程代码

课程阶段会整理与 Python 学习目标直接相关的部分，例如：

- 基础赛事数据模型；
- FastAPI 路由；
- SQLite 数据访问；
- 专业关键词 / 映射逻辑；
- 竞赛搜索、筛选与排序；
- 适合课程演示的 API。

#### 不在公开范围内

- Stellula 正式前端源代码；
- 生产环境完整后端实现；
- 真实用户数据；
- 管理后台与内部运营能力；
- OAuth、邮件、提醒等完整生产逻辑；
- 部署密钥、环境变量与安全配置；
- 内部数据维护流程及其他仅用于线上环境的实现。

> **答辩展示的是 Stellula；课程提交的是 Stellula Mini 的 Python 后端实现。**

两者共享产品思想，但并不是同一份完整源码。

### 当前状态

Stellula 仍在持续迭代。

这个公开仓库会保持克制：只有适合展示、学习和课程提交的内容才会进入这里。

**Live:** https://stellula.cloud

---

## English

### What is Stellula?

**Stellula** is a competition discovery platform designed for university students.

The problem is not that competition information does not exist. The problem is that it is scattered, inconsistent, and often difficult to evaluate.

A student may know their major and year of study and still have no clear answer to a simple question:

> **Which competitions actually make sense for me?**

Stellula is built around the student journey:

> **Discover → Decide → Participate → Record → Look back**

Instead of acting as a giant directory, it aims to help students narrow the field, understand why a competition is relevant, reach trustworthy official information, and preserve their own participation history.

### Core experience

#### Competition discovery

Use information such as major, year, interests, and region to surface more relevant competitions.

#### Explainable matching

Recommendations should not feel arbitrary. Stellula favors structured and understandable matching signals over opaque results.

#### Competition details and official resources

Competition pages organize useful context and verified official resources. Stellula does not replace official registration channels; it helps students reach them with less friction.

#### Personal competition wall

Students can keep a long-term record of competitions they want to join, have joined, or have completed.

The wall is designed as a personal history, not a leaderboard.

### Product principles

- **Useful before clever.** AI is optional; the core product should work without it.
- **Official sources first.** Important information should remain traceable to authoritative sources.
- **Explain recommendations.** Students should understand why something appears.
- **Designed for ordinary students.** Prior competition knowledge should not be required.
- **Participation is more than an award.** Experiences deserve to be recorded without reducing people to rankings.
- **Privacy by default.** Personal competition history should remain private unless the student chooses otherwise.

### Technical direction

The production application currently centers on:

- **Backend:** Python / FastAPI
- **Database:** SQLite
- **Frontend:** HTML / CSS / JavaScript
- **Deployment:** Linux / Uvicorn / Nginx

The production system also includes additional account, operations, reminder, security, and deployment capabilities.

### About this repository

This repository is the **public project showcase and course-deliverable repository for Stellula**.

It is **not** the production repository and is not intended to mirror the complete Stellula source code.

Its purposes are to:

- introduce the product and its design decisions;
- keep documentation suitable for public viewing;
- serve as a presentation entry point for a Python course project;
- later contain a small, independently runnable **Mini backend implementation** prepared specifically for coursework.

#### Planned course-code scope

The course-oriented backend may include selected components such as:

- basic competition data models;
- FastAPI routes;
- SQLite data access;
- major keyword / mapping logic;
- search, filtering, and ranking;
- APIs suitable for classroom demonstration.

#### Explicitly out of scope

This repository will not publish:

- the production frontend source code;
- the complete production backend;
- real user data;
- internal administration and operations tooling;
- the full production OAuth, email, reminder, and security flows;
- deployment secrets, environment variables, or private infrastructure configuration;
- internal data-maintenance workflows and production-only implementation details.

> **The presentation uses Stellula. The course submission uses a Mini Python backend derived from the same product idea.**

They share the same product direction, but they are intentionally not the same complete codebase.

### Status

Stellula is actively evolving.

This repository will stay intentionally small: only material suitable for public presentation, learning, and coursework will be added here.

**Live product:** https://stellula.cloud

---

<p align="center">
  <strong>Stellula</strong><br>
  <sub>Small stars can still show you where to go next. ✦</sub>
</p>


---

## ✅ 已加入：可运行的 Stellula Mini Python 后端（课程版）

该仓库现在包含 `app.py` 和 `requirements.txt`。它是**独立的教学实现**，根据正式 Stellula 的业务思想简化制作，不是生产后端的原样复制。

### 在电脑上运行

安装 Python 3.10 或更新版本，下载仓库，在项目目录打开终端：

```bash
python -m pip install -r requirements.txt
python -m uvicorn app:app --reload
```

启动后打开 http://127.0.0.1:8000/docs ，就能在交互式文档中依次测试接口。

### 课堂可展示的功能

| 方法 | 路径 | 功能 |
| --- | --- | --- |
| GET | /competitions | 查看及关键词搜索竞赛 |
| GET | /competitions/match | 按专业、年级、兴趣推荐 |
| GET | /competitions/{competition_id} | 查看单个竞赛 |
| POST | /competitions | 新增竞赛 |
| PUT | /competitions/{competition_id} | 修改竞赛 |
| DELETE | /competitions/{competition_id} | 删除竞赛 |

首次启动时会自动创建本地 `stellula_mini.db` 并添加 4 条**虚构演示数据**。数据只用于课堂讲解，请勿当作真实竞赛通知。数据可保存在本机，重启程序后不会丢失。

### 推荐功能怎么讲？

1. 接收专业、年级、兴趣条件。
2. 先排除年级不符合的竞赛。
3. 专业直接匹配加 70 分，兴趣相关加 30 分；不限专业给予 25 分作为拓展选择。
4. 过滤零分结果，并按照总分从高到低排序。
5. 返回匹配分数及原因。

**说明：** 这属于基于规则的推荐算法，不是训练得到的机器学习模型。正式版还包含更详细的专业映射、相关度权重、身份认证和后台维护等能力，均未复制到本公开课程仓库。

### 答辩时可讲的基础 Python 知识

- `def` 定义函数；`if` 判断；`for` 循环；列表与字典保存数据；
- `sqlite3` 连接本地数据库，执行带 `?` 参数的 SQL；
- `json.dumps` 和 `json.loads` 在字符串与列表间转换；
- FastAPI 的 `@app.get` / `@app.post` 等装饰器负责对外提供 HTTP 接口。

课程版没有登录验证和管理员权限控制，**仅用于本地学习与演示，不应直接部署为公开可写服务**。
