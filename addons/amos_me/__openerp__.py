# -*- coding: utf-8 -*-
##############################################################################
# OpenERP Connector
# Copyright 2013 Amos <sale@100china.cn>
##############################################################################

{
    'name': 'Amos me', #模块名称
    'summary': 'me', #摘要
    'version': '1.0', #版本
    'category': 'Tools', #分类
    'sequence': 1001, #排序
    'author': 'Amos', #作者
    'website': 'http://www.amoserp.com', #网址
    # 'images' : ['images/amos.jpeg',],#模块图片
    'depends': ['base','product','mail'], #关联模块
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'amos_me.xml',

        # 'wizard/amos_template_warning_view.xml',
        # 'sequence.xml',
        # 'amos_template_view.xml',
        # "data/precision_data.xml",
    ], #更新XML,CSV
    'installable': True, #是否可安装
    'application': True, #是否认证
    'auto_install': False, #是否自动安装
    'description': """
实例模块
====================================
模块描述

作用域:
------
    * 菜单
        * 小分类
    * 工作流
        * 固定工作流
其它说明
""",
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
