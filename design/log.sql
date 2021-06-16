drop table if exists account_update_log;
drop table if exists account_log;
drop table if exists loan_log;

create table account_update_log
(
   log_id               bigint not null auto_increment,
   bra_name             varchar(16) not null,
   acc_id               char(16) not null,
   acc_balance          double not null,
   acc_type             int not null,
   che_overdraft        double,
   sto_interest_rate    double,
   sto_currency_type    varchar(16),
   log_date             date not null,
   primary key (log_id)
);

alter table account_update_log comment '用以记录账户更新信息';

create table account_log
(
   log_id               bigint not null auto_increment,
   bra_name             varchar(16) not null,
   acc_type             int not null,
   acc_id               char(16) not null,
   cus_id               char(18) not null,
   log_type             int not null,
   log_date             date not null,
   primary key (log_id)
);

alter table account_log comment '用以记录账户的用户增删';

create table loan_log
(
   log_id               bigint not null auto_increment,
   bra_name             varchar(16) not null,
   loa_id               bigint not null,
   cus_id               char(18) not null,
   loa_amount           double not null,
   log_date             date not null,
   primary key (log_id)
);

alter table loan_log comment '用以记录贷款量';
