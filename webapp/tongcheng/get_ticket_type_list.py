#!/urs/bin/python
#coding=utf-8

import re
import json
from common.XMLtoJSON import XMLtoJSON
from datetime import datetime, date
from tc_common import *

from common.define import session as Session
from common.logger import get_logger
tc_log = get_logger('tc_tkt_type')
from models.tongcheng_model import TcSceneryTicketType 

_xml = """
<request>
    <header>
        <version>%s</version> 
        <accountID>%s</accountID>
        <serviceName>%s</serviceName> 
        )<digitalSign>%s</digitalSign> 
        <reqTime>%s</reqTime>
    </header>
    <body>
        <sceneryId>%d</sceneryId>     
    </body>
</request>
"""

servicename = "GetSceneryTicketTypeList"

def escape_chr(line):
    line = re.sub('\\\\|\r|\n','',line)
    return ''.join(c for c in line if ord(c) >= 32)

def get_ticket_type_by_sid(sid):
    try:
        _reqtime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        digitalSign = get_sign(servicename=servicename, reqtime=_reqtime)
        req_xml = _xml % (version,accountid,servicename,digitalSign,_reqtime,int(sid))
        result = escape_chr(get_reponse(req_xml=req_xml))
        r = XMLtoJSON(input_string=result).parse()
        return json.loads(r)   
    except Exception,e:
        return None

def parse_ticket_type(sid, cur_time=1, retry_time=5):
    while cur_time <= retry_time:
        try:
            rs = get_ticket_type_by_sid(sid)
            msg = rs['response']['header']['rspDesc']
            if msg == '获取景点信息成功':
                tt = rs['response']['body']['ticketTypeList']['ticketType']
                if type(tt) == type({}):
                    tt = [tt]
                for info in tt:
                    ticket_type_id = info.get('ticketTypeId')
                    ticket_type_name = info.get('ticketTypeName')
                    advice_amount = int(info.get('adviceAmount'))
                    amount = int(info.get('amount'))
                    save_amount = int(info.get('saveAmount'))
                    return_amount = save_amount-(advice_amount-amount)
                    pay_mode = info.get('payMode')
                    get_ticket_mode = info.get('getTicketMode')
                    price_remark = info.get('priceRemark', '')
                    ticket_price_id = info.get('ticketTypeId')
                    tc_log.info("%s\t%s\t%s"%(sid, ticket_type_name, ticket_type_id))
                    obj = Session.query(TcSceneryTicketType).filter(TcSceneryTicketType.scenery_id==int(sid)).filter(TcSceneryTicketType.ticket_type_id==ticket_type_id).first()
                    if not obj:
                        item = TcSceneryTicketType(
                                    scenery_id = int(sid),
                                    ticket_type_id = ticket_type_id,
                                    ticket_type_name = ticket_type_name,
                                    advice_amount = advice_amount,
                                    amount = amount,
                                    save_amount = save_amount,
                                    return_amount = return_amount,
                                    pay_mode = pay_mode,
                                    get_ticket_mode = get_ticket_mode,
                                    price_remark = price_remark,
                                    ticket_price_id = ticket_price_id,
                                    enabled = 1
                                    )
                        Session.add(item)
                    else:
                        obj.ticket_price_id = ticket_price_id
                        obj.ticket_type_name = ticket_type_name
                        obj.advice_amount = advice_amount
                        obj.amount = amount
                        obj.save_amount = save_amount
                        obj.return_amount = return_amount
                        obj.price_remark = price_remark
                        obj.enabled = 1
                        obj.last_update = datetime.now()
                    Session.commit()
            else:
                tc_log.info("%s\t%s"%(sid, msg))
        except Exception,e:
            parse_ticket_type(sid, cur_time=cur_time+1)
            tc_log.error("cur_time:%s\t%s\t%s"%(cur_time, sid, traceback.format_exc()))
        break
    else:
        tc_log.error("scenery_id:%s\tretry 5 times but fail"%sid)

def main():
    for s in Session.execute("select scenery_id from tc_scenery where last_update like '%s%%'"%(date.today())):
        parse_ticket_type(s[0])

if __name__ == '__main__':
    #get_ticket_type_by_sid(8261)
    #parse_ticket_type(27465)
    main()
