# -*- coding: utf-8 -*-
"""
模块信息
"""

MODULE_INFO = {
    'id': 'resident_info',
    'name': '居民信息',
    'type': 'node',
    'version': '1.0.0',
    'author': 'edouardlicn',
    'description': '管理居民住户信息，适合居委会及网格员使用。',
    'icon': 'bi-person-vcard',
    'permissions': [
        {'key': 'view_others', 'name': '查看别人的内容'},
        {'key': 'edit_others', 'name': '修改别人的内容'},
        {'key': 'delete_others', 'name': '删除别人的内容'},
    ],
    'export_fields': [
        {'name': 'name', 'label': '姓名', 'type': 'string', 'required': True},
        {'name': 'relation', 'label': '与户主关系', 'type': 'fk'},
        {'name': 'id_card', 'label': '身份证号', 'type': 'string'},
        {'name': 'gender', 'label': '性别', 'type': 'fk'},
        {'name': 'birth_date', 'label': '出生日期', 'type': 'date'},
        {'name': 'phone', 'label': '联系电话', 'type': 'telephone'},
        {'name': 'current_community', 'label': '现住小区/建筑', 'type': 'string'},
        {'name': 'current_door', 'label': '门牌地址', 'type': 'string'},
        {'name': 'grid', 'label': '所属网格', 'type': 'fk'},
        {'name': 'resident_type', 'label': '人员类型', 'type': 'fk'},
        {'name': 'is_key_person', 'label': '是否重点人员', 'type': 'boolean'},
        {'name': 'key_category', 'label': '重点类别', 'type': 'fk'},
        {'name': 'registered_community', 'label': '户籍小区/建筑', 'type': 'string'},
        {'name': 'registered_address', 'label': '户籍地址', 'type': 'string'},
        {'name': 'household_number', 'label': '户编号', 'type': 'string'},
        {'name': 'is_separated', 'label': '是否人户分离', 'type': 'boolean'},
        {'name': 'actual_residence', 'label': '实际居住地', 'type': 'string'},
        {'name': 'is_moved_out', 'label': '是否已迁出', 'type': 'boolean'},
        {'name': 'move_out_date', 'label': '迁出日期', 'type': 'date'},
        {'name': 'move_to_place', 'label': '迁往地', 'type': 'string'},
        {'name': 'is_deceased', 'label': '是否已死亡', 'type': 'boolean'},
        {'name': 'death_date', 'label': '死亡日期', 'type': 'date'},
        {'name': 'nation', 'label': '民族', 'type': 'fk'},
        {'name': 'political_status', 'label': '政治面貌', 'type': 'fk'},
        {'name': 'marital_status', 'label': '婚姻状况', 'type': 'fk'},
        {'name': 'education', 'label': '文化程度', 'type': 'fk'},
        {'name': 'work_status', 'label': '工作学习情况', 'type': 'string'},
        {'name': 'health_status', 'label': '健康状况', 'type': 'fk'},
        {'name': 'notes', 'label': '备注', 'type': 'string'},
    ],
    'dashboard_cards': [
        {
            'id': 'resident_info_card',
            'name': '居民信息',
            'template': 'resident_info/dashboard_card.html',
        }
    ],
    'dashboard_stats': True,
    'taxonomies': [
        {'slug': 'resident_relation', 'name': '与户主关系', 'items': ['户主', '配偶', '子女', '父母', '租户', '其他']},
        {'slug': 'resident_type', 'name': '人员类型', 'items': ['常住人口', '流动人口']},
        {'slug': 'grid', 'name': '所属网格', 'items': ['网格1', '网格2', '网格3', '网格4', '网格5']},
        {'slug': 'key_category', 'name': '重点类别', 'items': ['独居老人', '低保户', '残疾人', '重症患者', '刑满释放人员', '社区矫正对象', '涉毒人员', '其他']},
        {'slug': 'nation', 'name': '民族', 'items': ['汉族', '壮族', '满族', '回族', '苗族', '维吾尔族', '蒙古族', '藏族', '布依族', '彝族', '侗族', '瑶族', '白族', '土家族', '哈尼族', '傣族', '黎族', '傈僳族', '佤族', '畲族', '高山族', '拉祜族', '水族', '东乡族', '纳西族', '景颇族', '柯尔克孜族', '土族', '达斡尔族', '仫佬族', '羌族', '布朗族', '撒拉族', '毛南族', '仡佬族', '锡伯族', '阿昌族', '普米族', '塔吉克族', '怒族', '乌孜别克族', '俄罗斯族', '鄂温克族', '德昂族', '保安族', '裕固族', '京族', '塔塔尔族', '独龙族', '鄂伦春族', '赫哲族', '门巴族', '珞巴族', '基诺族', '其他']},
        {'slug': 'political_status', 'name': '政治面貌', 'items': ['中共党员', '中共预备党员', '共青团员', '群众']},
        {'slug': 'marital_status', 'name': '婚姻状况', 'items': ['未婚', '已婚', '离异', '丧偶']},
        {'slug': 'education', 'name': '文化程度', 'items': ['研究生', '本科', '大专', '高中', '初中', '小学', '文盲']},
        {'slug': 'health_status', 'name': '健康状况', 'items': ['健康', '良好', '残疾', '疾病', '慢性病']},
    ],
}


def get_install_sql():
    """获取模块安装时执行的 SQL（可选）"""
    return None


def get_uninstall_sql():
    """获取模块卸载时执行的 SQL（可选）"""
    return None