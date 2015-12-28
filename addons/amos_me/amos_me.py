# -*- coding: utf-8 -*-
##############################################################################
# OpenERP Connector
# Copyright 2013 Amos <sale@100china.cn>
##############################################################################

from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
import time
from openerp.tools.translate import _
import datetime
import simplejson

try:
    from openerp import SUPERUSER_ID
except ImportError:
    SUPERUSER_ID = SUPERUSER_ID


class amos_me(osv.osv):
    _name = "amos.me"
    _inherit = ['mail.thread']
    _description = "amos.me"
    _order = "date desc"

    _columns = {
        'name': fields.char(u'编号', size=64, help=u"我是编号"),

        'date': fields.date(u'短日期'),
        'price_unit': fields.float(u'价格', required=True, digits_compute=dp.get_precision('Product Price')),
        'files': fields.binary('Files'),
        'date_start': fields.date(u'开始日期'),
        'date_end': fields.date(u'结束日期'),

        'row': fields.integer(u'行数'),

        'active': fields.boolean(u'是否可用'),
        'user_id': fields.many2one('res.users', u'制单人'),
        'partner_id': fields.many2one('res.partner', u'客户',required=True,),

        'partner_id_name': fields.related("partner_id", "phone", type="char", string=u"名称", readonly=True,
                                    track_visibility='onchange'),
        'user_name': fields.related("user_id", "name", type="char", string=u"名称", readonly=True,
                                    track_visibility='onchange'),
        'category_ids': fields.many2many('res.partner.category', 'amos_me_res_partner_category_rel', 'a_id', 'b_id',
                                         U'分类'),
        'note': fields.text(u'备注'),
        'line': fields.one2many('amos.me.line', 'me_line', u'明细'),
        'state': fields.selection([('draft', u'草稿'),
                                   ('review', u'等待审核'),
                                   ('done', u'已完成'),
                                   ('sent', u'发送邮件'),
                                   ('cancel', u'取消'), ],
                                  u'状态', ),
    }

    _defaults = {
        # 'name': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'amos.template'),
        'date': lambda *a: time.strftime('%Y-%m-%d'),
        'date_start': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'state': lambda *a: 'draft',
        'user_id': lambda cr, uid, id, c={}: id,
        'active': lambda *a: True,
        # 'company_id': lambda s, cr, uid, c: s.pool.get('res.company')._company_default_get(cr, uid, 'hr.employee',
        #                                                                                    context=c),
    }

    _sql_constraints = [
        ('name_uniq', 'unique(name)', u'单据编号已存在!'),
    ]

    def _check_dates(self, cr, uid, ids, context=None):
         for phase in self.read(cr, uid, ids, ['date_start', 'date_end'], context=context):
             if phase['date_start'] and phase['date_end'] and phase['date_start'] > phase['date_end']:
                 return False
         return True

    _constraints = [
        (_check_dates, '结束日期必须大于起始日期', ['date_start', 'date_end']  ),
    ]
    def amos_review(self, cr, uid, ids, context=None):
        state = 'review'
        message = '提交草稿 等待审核!'
        self.write(cr, uid, ids, {'state': state}, context=context)
        self.message_post(cr, uid, ids, body=_(message), context=context)
        return True

    def amos_cancel(self, cr, uid, ids, context=None):
        state = 'cancel'
        message = '单据已取消'
        self.amos_action(cr, uid, ids, state, message, context=context)
        return True

    def amos_done(self, cr, uid, ids, context={}):
        state = 'done'
        message = '单据已完成'
        self.amos_action(cr, uid, ids, state, message, context=context)
        return True

    def amos_draft(self, cr, uid, ids, context={}):
        state = 'draft'
        message = '单据重置为草稿'
        self.amos_action(cr, uid, ids, state, message, context=context)
        return True

    #按钮的触发事件类
    def amos_action(self, cr, uid, ids, state, message, context={}):
        self.write(cr, uid, ids, {'state': state}, context=context)

        #推送消息
        self.message_post(cr, uid, ids, body=_(message), context=context)

        #mail_thread.py 文件查询
        #region login 帐户
        # self.message_subscribe_users(cr, uid, ids, user_ids=[4], context=context)
        #加入客户
        if hasattr(self, 'message_subscribe'):
            self.message_subscribe(cr, uid, ids, [4], context=context)


        return True
    def onchange_partner_id(self, cr, uid, ids, partner_id, user_id, context=None):
        print user_id
        res = {}
        if partner_id:
            pream = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
            res['name'] = pream.name
            res['note'] = u'后台传值'
        return {'value': res}


amos_me()


class amos_me_line(osv.osv):
    _name = "amos.me.line"
    _description = "amos.me.line"

    _columns = {
        'name': fields.char(u'备注', size=5),
        'product_id': fields.many2one('product.product', u'费用名称'),
        'me_line': fields.many2one('amos.me', u'明细'),

    }


amos_me_line()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: