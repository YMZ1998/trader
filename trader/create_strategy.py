import os
import sys

import django
sys.path.append('../dashboard')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dashboard.settings")
django.setup()

from panel.models import Strategy, Broker, Instrument, Address


# 1. 创建 Address 实例（交易前置和行情前置地址）
addr_trade = Address.objects.create(
    name='交易前置1',
    url='tcp://trade.example.com:1234',
    type='trade',  # 具体值要对应 AddressType.choices 里的有效选项
    operator='operator1'  # 同理，要对应 OperatorType.choices 的有效值
)

addr_market = Address.objects.create(
    name='行情前置1',
    url='tcp://market.example.com:5678',
    type='market',
    operator='operator2'
)

# 2. 创建 Broker 实例，必须传入 Address 实例对象
broker = Broker.objects.create(
    name='测试账户',
    contract_type='contract_type_value',  # 对应 ContractType.choices 里的有效值
    trade_address=addr_trade,
    market_address=addr_market,
    identify='unique_id_001',
    username='user1',
    password='pass1',
    fake=100000,
    cash=100000,
    current=100000,
    pre_balance=100000,
    margin=10000,
)

print("Broker 创建成功:", broker)

strategy = Strategy.objects.create(name='大哥2.2', broker=broker)

instruments = Instrument.objects.all()[:2]
strategy.instruments.set(instruments)
strategy.force_opens.set(instruments)
strategy.save()

print("策略创建成功:", strategy)
