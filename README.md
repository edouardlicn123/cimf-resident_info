# 居民信息模块 (Resident Info Module)

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Django](https://img.shields.io/badge/django-6.0+-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

> 用于CIMF系统的居民住户信息管理模块，适用于居委会及网格员的管理场景。

## 目录

- [功能特性](#功能特性)
- [快速开始](#快速开始)
- [数据模型](#数据模型)
- [路由接口](#路由接口)
- [权限配置](#权限配置)
- [词汇表配置](#词汇表配置)
- [项目结构](#项目结构)

---

## 功能特性

- **居民信息管理** - 完整的 CRUD 操作，支持增删改查
- **多维度筛选** - 按人员类型、所属网格、关键词搜索
- **重点人员标记** - 支持标记和分类重点人员（独居老人、低保户等）
- **人口状态追踪** - 追踪迁出、人户分离、死亡等状态
- **权限控制** - 基于角色的细粒度权限管理
- **仪表盘统计** - 提供 API 接口用于仪表盘数据展示

---

## 快速开始

### 安装

模块已集成到系统中，初始化时自动安装：

```bash
# 初始化数据库（自动安装所有模块）
python init_db.py --with-data
```

### 手动安装

```bash
# 进入 Django shell
python manage.py shell

# 安装模块
from core.node.services import ModuleService
ModuleService.install_module('resident_info')
```

### 访问

初始化完成后，访问 `/resident_info/` 即可进入居民信息管理页面。同时系统会在事务管理页增加入口

---

## 数据模型

### ResidentInfoFields

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `node` | OneToOneField | ✅ | 关联 Node 节点 |
| `name` | CharField(100) | ✅ | 姓名 |
| `relation` | ForeignKey | - | 与户主关系（词汇表） |
| `id_card` | CharField(18) | - | 身份证号 |
| `gender` | ForeignKey | - | 性别（词汇表） |
| `birth_date` | DateField | - | 出生日期 |
| `phone` | CharField(100) | - | 联系电话 |
| **现住址信息** | | | |
| `current_community` | CharField(200) | - | 现住小区/建筑 |
| `current_door` | CharField(100) | - | 门牌地址 |
| `grid` | ForeignKey | - | 所属网格（词汇表） |
| **人员分类** | | | |
| `resident_type` | ForeignKey | - | 人员类型（词汇表） |
| `is_key_person` | BooleanField | - | 是否重点人员 |
| `key_category` | ForeignKey | - | 重点类别（词汇表） |
| **户籍信息** | | | |
| `registered_community` | CharField(200) | - | 户籍小区/建筑 |
| `registered_address` | CharField(200) | - | 户籍地址 |
| `registered_region` | JSONField | - | 户籍地址省市区 |
| `household_number` | CharField(50) | - | 户编号 |
| **人户分离** | | | |
| `is_separated` | BooleanField | - | 是否人户分离 |
| `actual_residence` | CharField(200) | - | 实际居住地 |
| **迁出信息** | | | |
| `is_moved_out` | BooleanField | - | 是否已迁出 |
| `move_out_date` | DateField | - | 迁出日期 |
| `move_to_place` | CharField(200) | - | 迁往地 |
| **死亡信息** | | | |
| `is_deceased` | BooleanField | - | 是否已死亡 |
| `death_date` | DateField | - | 死亡日期 |
| **基本信息** | | | |
| `nation` | ForeignKey | - | 民族（词汇表） |
| `political_status` | ForeignKey | - | 政治面貌（词汇表） |
| `marital_status` | ForeignKey | - | 婚姻状况（词汇表） |
| `education` | ForeignKey | - | 文化程度（词汇表） |
| `work_status` | CharField(50) | - | 工作学习情况 |
| `health_status` | ForeignKey | - | 健康状况（词汇表） |
| `notes` | TextField | - | 备注 |
| `created_at` | DateTimeField | ✅ | 创建时间（自动） |
| `updated_at` | DateTimeField | ✅ | 更新时间（自动） |

---

## 路由接口

### 页面路由

| 路径 | 方法 | 视图 | 说明 |
|------|------|------|------|
| `/resident_info/` | GET | `node_list` | 居民列表页 |
| `/resident_info/create/` | GET/POST | `node_create` | 创建居民 |
| `/resident_info/<node_id>/` | GET | `node_view` | 查看详情 |
| `/resident_info/<node_id>/edit/` | GET/POST | `node_edit` | 编辑居民 |
| `/resident_info/<node_id>/delete/` | POST | `node_delete` | 删除居民 |

### API 接口

| 路径 | 方法 | 说明 | 返回 |
|------|------|------|------|
| `/resident_info/api/stats/` | GET | 获取统计数据 | `{ total, recent }` |

**响应示例：**

```json
{
  "success": true,
  "data": {
    "total": 1250,
    "recent": 15
  }
}
```

---

## 权限配置

模块使用系统统一的权限控制机制：

| 权限标识 | 说明 |
|----------|------|
| `node.resident_info.view_others` | 查看他人的居民信息 |
| `node.resident_info.edit_others` | 编辑他人的居民信息 |
| `node.resident_info.delete_others` | 删除他人的居民信息 |

**默认规则：**
- 管理员（`is_admin=True`）拥有所有权限
- 创建者可查看/编辑/删除自己创建的记录
- 非管理员查看他人数据需配置对应权限

---

## 词汇表配置

模块安装时自动创建以下词汇表（Taxonomy）：

| Slug | 名称 | 预设选项 |
|------|------|----------|
| `resident_relation` | 与户主关系 | 户主、配偶、子女、父母、租户、其他 |
| `resident_type` | 人员类型 | 常住人口、流动人口、暂住人口 |
| `grid` | 所属网格 | 网格1 ~ 网格5 |
| `key_category` | 重点类别 | 独居老人、低保户、残疾人、重症患者、刑满释放人员、社区矫正对象、涉毒人员、其他 |
| `nation` | 民族 | 56个民族 + 其他 |
| `political_status` | 政治面貌 | 中共党员、中共预备党员、共青团员、群众 |
| `marital_status` | 婚姻状况 | 未婚、已婚、离异、丧偶 |
| `education` | 文化程度 | 研究生、本科、大专、高中、初中、小学、文盲 |
| `health_status` | 健康状况 | 健康、良好、残疾、疾病、慢性病 |

---

## 项目结构

```
modules/resident_info/
├── __init__.py          # 模块初始化
├── apps.py              # Django App 配置
├── module.py            # 模块元信息（版本、词汇表定义等）
├── models.py            # 数据模型
├── services.py          # 业务逻辑层
├── views.py             # 视图控制器
├── urls.py              # URL 路由
├── migrations/          # 数据库迁移文件
└── templates/           # 模板文件
    └── resident_info/
        ├── list.html    # 列表页
        ├── view.html    # 详情页
        ├── edit.html    # 编辑页
        └── dashboard_card.html  # 仪表盘卡片
```

---

## 依赖

- Django 6.0+
- core 应用（Node、NodeType、Taxonomy 等核心模型）

---

## 更新日志

### 1.0.0 (2026-03-31)

- ✨ 初始版本发布
- ✨ 居民信息 CRUD 功能
- ✨ 多维度筛选（人员类型、网格、搜索）
- ✨ 重点人员标记与分类
- ✨ 人口状态追踪（迁出、人户分离、死亡）
- ✨ 权限控制（创建者/他人数据隔离）
- ✨ 仪表盘统计 API
- ✨ 9类词汇表自动初始化
