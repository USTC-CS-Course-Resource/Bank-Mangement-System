# Bank Management System

PB18111697 王章瀚

-----

## Requirements

- python packages:
  - dateutils
  - flask
  - pyjwt
  - pymysql
- nodejs: see [nodejs requirements](./webui/vue/package.json)

## Report

My Report is in [report.pdf](./report/db-lab03-report.pdf) or [report.docx](.report/db-lab03-report.docx)

## Run This Project

1. install nodejs requirements:
   ```shell
   cd webui/vue
   npm install
   ```
2. start vue server:
   ```shell
   cd webui/vue
   npm run serve
   ```
3. start flask server:
   ```shell
   python -m webui.main
   ```
  
Then just enter the vue server's local address.

## Design

### 客户管理

客户信息在 `customer` 表中由其 `id` 唯一标识

- **增**: 增加客户信息只需要在 `customer` 表加入其信息
- **删**: 删除客户信息需要先在 `have_store_account` / `have_check_account` 表中检查是否存在关联的账户, 以及是否还有贷款信息. 如有, 则拒绝删除; 否则只需要在 `customer` 表删去其信息
- **改**: 由客户 id 唯一标识地修改即可
- **查**: 由客户 id 唯一标识地查找即可

### 账户操作

- **开户**: 应同时向 账户表(`account`) 添加账户, 并在相应子类表储蓄账户(`saving_account`) 或 支票账户(`checking_account`) 中添加相关信息, 最后添加拥有关系:
  - **拥有储蓄/支票账户关系** 由于对于客户身份证号和支行名会有索引, 插入查询等操作是比较快的.
  - **账户表** 保证了账户号的唯一性
- **销户**, 应当事务地先将 `have_store_account` 或 `have_check_account` 内数据删去, 而后 `saving_account` 或 `checking_account` 的数据, 最后 `account` 表内数据.
- **查询**: 
  - 定位账户的依据: 
    - 账户号: 则直接从 `account` 表可查到
    - (客户身份证号, 开户支行, 账户类型): 可直接查到相应的账户号.
  - 查到账户号后其他的数据都能方便地获取.
- **修改**: 抽象为 存款, 汇款(包括普通汇款和透支汇款), 换账户, 改货币类型, 改利率等
  - 客户换用账户: 添加好相应账户(如已有则不用), 而后在 `have_xxxxx_account` 表内关联.
  - 修改利率, 货币类型, 余额, 透支金额 均可由上一步获取账户号的方法之后, 进一步操作.

### 贷款管理

- **增**: 新增贷款则在 `loan` 表中加入新的贷款项目即可.
- **删**: 检查是否处于发放状态, 若否, 则直接从 `loan` 中删除.(是否删除付贷记录需要考虑一下)
- **查**: 根据贷款号进行查询, 可以提供查询已付额, 待付额, 总额, 付贷记录, 发放状态
- **贷款发放**: 贷款发放时, 检查发放额是否小于待发放额后, 在 `pay_loan` 表中加入相关发放记录.

### 业务统计

- 后端 按 月/季/年 及 储蓄/贷款 给出交易量, 银行总额度, 用户数. 
- 前端给出表格和可视化图

具体统计内容与方法待 lab3 设计, 在此不作说明.

## Links

[MySQL Error Codes](https://docs.oracle.com/cd/E17952_01/mysql-errors-8.0-en/)

## 特点

- 上下文管理器捕获异常, 代码更为简洁
- 精致而有效的 logger 配置
- 精准防止 SQL 注入攻击
