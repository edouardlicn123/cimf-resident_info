# 居民信息模块技术规范

> 文档版本：1.0  
> 创建日期：2026-04-28  
> 最后更新：2026-04-28

---

## 一、模块概述

### 1.1 功能定位

`resident_info` 是居民信息管理模块，用于管理居民住户信息，适合居委会及网格员使用。模块支持人员信息登记、网格化管理、重点人员跟踪等功能。

### 1.2 核心特性

| 特性 | 说明 |
|------|------|
| 人员管理 | 完整的居民信息登记和管理 |
| 网格化管理 | 支持按网格划分管理人员 |
| 重点人员跟踪 | 独居老人、低保户、残疾人等重点人员标记 |
| 居住状态管理 | 人户分离、迁入迁出、死亡等状态跟踪 |
| 数据导入导出 | 支持 CSV/Excel 格式批量操作 |
| 权限控制 | 细粒度权限管理，支持查看/编辑/删除他人数据 |

### 1.3 与 customer 模块对比

| 对比项 | customer | resident_info |
|--------|----------|---------------|
| 业务场景 | 客户信息管理 | 居民信息管理 |
| 核心字段 | 企业信息、联系人 | 身份证、家庭关系 |
| 行政区划 | 省市县联动 | 网格化管理 |
| 状态跟踪 | 客户等级、信用 | 迁入迁出、死亡 |
| 适用对象 | 销售团队 | 居委会、网格员 |

---

## 二、目录结构

```
resident_info/
├── __init__.py              # 包初始化
├── apps.py                  # Django App 配置
├── models.py                # 数据模型 (192行)
├── module.py                # 模块信息配置 (85行)
├── services.py             # 业务服务层 (213行)
├── views.py                # 视图函数 (~400行)
├── urls.py                 # URL 路由配置 (18行)
├── migrations/             # 数据库迁移
├── templates/              # 模板目录
│   ├── list.html          # 列表页
│   ├── view.html          # 详情页
│   ├── edit.html          # 编辑页
│   └── resident_info/
│       └── dashboard_card.html
└── docs/                  # 技术文档
    └── README.md
```

---

## 三、数据模型

### 3.1 模型结构

```python
class ResidentInfoFields(models.Model):
    """居民信息字段表"""
    
    node = models.OneToOneField(Node, on_delete=models.CASCADE)
    
    # 基本信息
    name = CharField(max_length=100)
    relation = ForeignKey(TaxonomyItem)  # 与户主关系
    id_card = CharField(max_length=18)  # 身份证号
    gender = ForeignKey(TaxonomyItem)   # 性别
    birth_date = DateField()          # 出生日期
    
    # 联系方式
    phone/phone2/phone3 = CharField(max_length=20)  # 联系电话
    
    # 居住信息
    current_community = CharField()  # 现住小区/建筑
    current_door = CharField()         # 门牌地址
    grid = ForeignKey(TaxonomyItem)    # 所属网格
    resident_type = ForeignKey(TaxonomyItem)  # 人员类型
    is_key_person = BooleanField()     # 是否重点人员
    key_category = ForeignKey(TaxonomyItem)  # 重点类别
    
    # 户籍信息
    registered_community = CharField()
    registered_address = CharField()
    registered_region = CharField()  # 户籍地址省市区
    household_number = CharField()   # 户编号
    
    # 迁移状态
    is_separated = BooleanField()    # 是否人户分离
    actual_residence = CharField()  # 实际居住地
    is_moved_out = BooleanField()   # 是否已迁出
    move_out_date = DateField()      # 迁出日期
    move_to_place = CharField()     # 迁往地
    
    # 死亡信息
    is_deceased = BooleanField()    # 是否已死亡
    death_date = DateField()       # 死亡日期
    death_reason = CharField()    # 死亡原因
    
    # 附加信息
    nation = ForeignKey(TaxonomyItem)      # 民族
    political_status = ForeignKey(TaxonomyItem)  # 政治面貌
    marital_status = ForeignKey(TaxonomyItem)   # 婚姻状况
    education = ForeignKey(TaxonomyItem)      # 文化程度
    work_status = CharField()               # 工作学习情况
    health_status = ForeignKey(TaxonomyItem)  # 健康状况
    notes = TextField()                     # 备注
```

### 3.2 字段统计

| 分类 | 字段数量 |
|------|----------|
| 基本信息 | 5 |
| 联系方式 | 3 |
| 居住信息 | 6 |
| 户籍信息 | 4 |
| 迁移状态 | 4 |
| 死亡信息 | 3 |
| 附加信息 | 6 |
| **总计** | **31** |

---

## 四、服务层 (ResidentInfoService)

### 4.1 方法说明

| 方法 | 参数 | 返回 | 说明 |
|------|------|------|------|
| `get_list()` | search, resident_type_id, grid_id, current_community, show_moved_out, show_deceased, user | List | 获取居民列表，支持多条件筛选 |
| `get_by_id()` | resident_id | ResidentInfoFields | 根据ID获取居民 |
| `get_by_node_id()` | node_id | ResidentInfoFields | 根据节点ID获取居民 |
| `create()` | user, data | ResidentInfoFields | 创建居民信息 |
| `update()` | resident_id, user, data | ResidentInfoFields | 更新居民信息 |
| `delete()` | resident_id | bool | 删除居民 |
| `get_count()` | - | int | 获取居民总数 |
| `get_recent_count()` | days | int | 获取最近N天新增数 |
| `get_stats()` | - | Dict | 获取统计信息 |
| `init_sample_data()` | - | int | 初始化样本数据 |

### 4.2 使用示例

```python
from modules.resident_info.services import ResidentInfoService

# 获取列表（支持多条件筛选）
residents = ResidentInfoService.get_list(
    search='张',
    resident_type_id=1,
    grid_id=2,
    show_moved_out=False,
    show_deceased=False,
    user=request.user
)

# 获取统计信息
stats = ResidentInfoService.get_stats()
# 返回: {'total': 150, 'recent': 12, 'key_persons': 25, ...}
```

---

## 五、视图层

### 5.1 URL 路由配置

```python
app_name = 'resident_info'

urlpatterns = [
    path('', views.node_list, name='list'),
    path('create/', views.node_create, name='create'),
    path('<int:node_id>/', views.node_view, name='view'),
    path('<int:node_id>/edit/', views.node_edit, name='edit'),
    path('<int:node_id>/delete/', views.node_delete, name='delete'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
```

### 5.2 URL 与视图对照表

| URL | 视图函数 | 模板 | 说明 |
|-----|----------|------|------|
| `/modules/resident_info/` | `node_list` | `list.html` | 列表页 |
| `/modules/resident_info/create/` | `node_create` | `edit.html` | 新建页 |
| `/modules/resident_info/{node_id}/` | `node_view` | `view.html` | 详情页 |
| `/modules/resident_info/{node_id}/edit/` | `node_edit` | `edit.html` | 编辑页 |
| `/modules/resident_info/{node_id}/delete/` | `node_delete` | - | 删除（重定向） |
| `/modules/resident_info/api/stats/` | `api_stats` | - | 统计API |

### 5.3 筛选参数

列表页支持多条件筛选：

| 参数 | 类型 | 说明 |
|------|------|------|
| `search` | string | 搜索（姓名/身份证/电话） |
| `resident_type` | int | 人员类型筛选 |
| `grid` | int | 网格筛选 |
| `current_community` | string | 现住小区筛选 |
| `show_moved_out` | bool | 显示已迁出 |
| `show_deceased` | bool | 显示已死亡 |
| `page` | int | 页码 |

### 5.4 API 响应格式

**api_stats 接口：**

```json
{
    "success": true,
    "data": {
        "total": 150,
        "recent": 12,
        "key_persons": 25,
        "moved_out": 8,
        "deceased": 3
    }
}
```

### 5.5 权限控制

| 权限 key | 说明 |
|----------|------|
| `node.resident_info.view_others` | 查看他人创建的居民信息 |
| `node.resident_info.edit_others` | 编辑他人创建的居民信息 |
| `node.resident_info.delete_others` | 删除他人创建的居民信息 |

---

## 六、模板

### 6.1 模板列表

| 模板 | 说明 |
|------|------|
| `list.html` | 居民列表页 |
| `view.html` | 居民详情页 |
| `edit.html` | 新建/编辑表单页 |
| `resident_info/dashboard_card.html` | 首页卡片 |

### 6.2 模板继承结构

```
base.html
  └── frame_node.html
        ├── list.html      # 列表页
        ├── view.html      # 详情页
        └── edit.html     # 编辑页（新建/编辑共用）
```

---

## 七、module.py 配置

```python
MODULE_INFO = {
    'id': 'resident_info',
    'name': '居民信息',
    'type': 'node',
    'version': '1.2.1',
    'author': 'edouardlicn',
    'description': '管理居民住户信息，适合居委会及网格员使用。',
    'icon': 'bi-person-vcard',
    'require': [],
    'frontpage_card_clickable': True,
    'permissions': [
        {'key': 'view_others', 'name': '查看别人的内容'},
        {'key': 'edit_others', 'name': '修改别人的内容'},
        {'key': 'delete_others', 'name': '删除别人的内容'},
    ],
    'export_fields': [
        {'name': 'name', 'label': '姓名', 'type': 'string', 'required': True},
        {'name': 'relation', 'label': '与户主关系', 'type': 'fk'},
        # ... 更多字段（共34个）
    ],
    'dashboard_stats': True,
    'dashboard_cards': [
        {
            'id': 'resident_info_card',
            'name': '居民信息',
            'template': 'resident_info/dashboard_card.html',
        }
    ],
    'taxonomies': [
        {'slug': 'resident_relation', 'name': '与户主关系', 'items': [...]},
        {'slug': 'resident_type', 'name': '人员类型', 'items': [...]},
        # ... 更多词汇表
    ],
}
```

---

## 八、数据导入导出

### 8.1 导出字段配置

`export_fields` 定义了 34 个可导出字段：

| 字段名 | 中文名 | 类型 | 必填 |
|--------|--------|------|------|
| name | 姓名 | string | 是 |
| relation | 与户主关系 | fk | 否 |
| id_card | 身份证号 | string | 否 |
| gender | 性别 | fk | 否 |
| birth_date | 出生日期 | date | 否 |
| phone | 联系电话 | telephone | 否 |
| ... | ... | ... | ... |

### 8.2 状态字段

| 字段 | 说明 |
|------|------|
| is_key_person | 是否重点人员 |
| is_separated | 是否人户分离 |
| is_moved_out | 是否已迁出 |
| is_deceased | 是否已死亡 |

---

## 九、taxonomies 词汇表配置

模块内置以下词汇表：

| Slug | 名称 | 用途 |
|------|------|------|
| `resident_relation` | 与户主关系 | 人员关系分类 |
| `resident_type` | 人员类型 | 常住/流动人口 |
| `grid` | 所属网格 | 网格划分 |
| `key_category` | 重点类别 | 重点人员分类 |
| `nation` | 民族 | 56个民族 |
| `political_status` | 政治面貌 | 党员/团员/群众 |
| `marital_status` | 婚姻状况 | 未婚/已婚/离异/丧偶 |
| `education` | 文化程度 | 学历分类 |
| `health_status` | 健康状况 | 健康状态 |

---

## 十、依赖关系

### 10.1 模块依赖

| 依赖 | 说明 |
|------|------|
| `core.node` | 节点核心系统 |
| `core.TaxonomyItem` | 词汇表项 |
| `core.services.TaxonomyService` | 词汇表服务 |
| `modules.resident_info.models` | 本模块模型 |

### 10.2 系统依赖

| 依赖 | 说明 |
|------|------|
| Django 6.0+ | Web 框架 |
| Bootstrap 5 | UI 框架 |
| Bootstrap Icons | 图标库 |

---

## 十一、版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.2.1 | 2026-04-28 | 当前版本 |
| 1.2.0 | 2026-04-12 | 优化字段配置 |
| 1.1.0 | 2026-03-20 | 初始版本 |

---

## 十二、相关文档

| 文档 | 说明 |
|------|------|
| [A02_模块技术规范](../../docs/技术规范/A02_模块技术规范.md) | 模块系统实现指南 |
| [A04_模板开发规范](../../docs/技术规范/A04_模板开发规范.md) | Jinja2 模板开发规范 |
| [customer_cn 模块技术规范](../customer_cn/docs/README.md) | 客户信息（国内）模块参考 |