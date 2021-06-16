drop table if exists account_update_log;
drop table if exists account_log;

create table account_update_log
(
   acc_upd_log_id       bigint not null auto_increment,
   bra_name             varchar(16) not null,
   acc_id               char(16) not null,
   acc_balance          double not null,
   acc_type             int not null,
   che_overdraft        double,
   sto_interest_rate    double,
   sto_currency_type    varchar(16),
   log_date             date not null,
   primary key (acc_upd_log_id)
);

alter table account_update_log comment '用以记录账户更新信息';

create table account_log
(
   acc_log_id           bigint not null auto_increment,
   bra_name             varchar(16) not null,
   acc_type             int not null,
   acc_id               char(16) not null,
   cus_id               char(18) not null,
   log_type             int not null,
   log_date             date not null,
   primary key (acc_log_id)
);

alter table account_log comment '用以记录账户的用户增删';

-- select * from account_update_log aul, 
--    (select acc_id, max(log_date) as log_date from account_update_log group by acc_id) max_date 
-- where aul.acc_type = 0 and aul.log_date = max_date.log_date and aul.acc_id = max_date.acc_id;

-- select bra_name, sum(acc_balance) balance from account_update_log aul, 
--    (
--       select acc_id, max(log_date) as log_date 
--       from account_update_log 
--       where log_date < "2021-11-01"
--       group by acc_id
--    ) max_date
-- where aul.acc_type = 0 and aul.log_date = max_date.log_date and aul.acc_id = max_date.acc_id
-- group by bra_name;

-- select bra_name, sum(acc_balance) balance from account_update_log aul, 
--            (
--               select acc_id, max(log_date) as log_date 
--               from account_update_log 
--               where log_date < '2021-06-16'
--               group by acc_id
--            ) max_date
--         where aul.acc_type = 0 and aul.log_date = max_date.log_date and aul.acc_id = max_date.acc_id
--         group by bra_name;

-- select bra_name, count(*) as cus_count from account_log al
-- where al.acc_type = 0 and al.log_type = 1 and al.log_date < "2020-11-01" and al.cus_id not in (
--       select distinct cus_id from account_log where acc_type = 0 and log_type = 0 and log_date < "2020-11-01"
--    )
-- group by bra_name;