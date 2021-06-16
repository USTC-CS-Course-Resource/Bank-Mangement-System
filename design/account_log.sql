drop table if exists account_update_log;
drop table if exists account_log;

create table account_update_log
(
   bra_name             varchar(16) not null,
   acc_id               char(16) not null,
   acc_balance          double not null,
   acc_type             int not null,
   che_overdraft        double,
   sto_interest_rate    double,
   sto_currency_type    varchar(16),
   log_date             date not null
);

alter table account_update_log comment '用以记录账户更新信息';

create table account_log
(
   bra_name             varchar(16) not null,
   acc_type             int not null,
   acc_id               char(16) not null,
   cus_id               char(18) not null,
   log_type             int not null,
   log_date             date not null
);

alter table account_log comment '用以记录账户的用户增删';
