/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2021/6/11 12:19:06                           */
/*==============================================================*/


drop table if exists account;

drop table if exists branch;

drop table if exists check_account;

drop table if exists contacts;

drop table if exists customer;

drop table if exists department;

drop table if exists department_manager;

drop table if exists have_check_account;

drop table if exists have_store_account;

drop table if exists loan;

drop table if exists loan_relation;

drop table if exists pay_loan;

drop table if exists responsibility;

drop table if exists staff;

drop table if exists store_account;

/*==============================================================*/
/* Table: account                                               */
/*==============================================================*/
create table account
(
   acc_id               char(16) not null,
   acc_balance          double not null,
   acc_type             int not null,
   acc_open_date        date not null,
   primary key (acc_id)
);

alter table account comment '账户类型type: 0 表示储蓄账户, 1 表示支票账户';

/*==============================================================*/
/* Table: branch                                                */
/*==============================================================*/
create table branch
(
   bra_name             varchar(16) not null,
   bra_city             varchar(16) not null,
   primary key (bra_name)
);

/*==============================================================*/
/* Table: check_account                                         */
/*==============================================================*/
create table check_account
(
   acc_id               char(16) not null,
   che_overdraft        double not null,
   primary key (acc_id)
);

/*==============================================================*/
/* Table: contacts                                              */
/*==============================================================*/
create table contacts
(
   cus_id               varchar(18) not null,
   con_name             varchar(16) not null,
   con_phone            varchar(16) not null,
   con_email            varchar(32) not null,
   con_relation         varchar(16) not null,
   primary key (cus_id, con_name)
);

/*==============================================================*/
/* Table: customer                                              */
/*==============================================================*/
create table customer
(
   cus_id               varchar(18) not null,
   cus_name             varchar(16) not null,
   cus_phone            varchar(16) not null,
   cus_address          varchar(32) not null,
   primary key (cus_id)
);

/*==============================================================*/
/* Table: department                                            */
/*==============================================================*/
create table department
(
   bra_name             varchar(16) not null,
   dep_id               bigint not null,
   dep_name             varchar(16) not null,
   dep_type             varchar(16) not null,
   primary key (bra_name, dep_id)
);

/*==============================================================*/
/* Table: department_manager                                    */
/*==============================================================*/
create table department_manager
(
   bra_name             varchar(16) not null,
   dep_id               bigint not null,
   sta_id               varchar(18) not null,
   primary key (bra_name, dep_id, sta_id)
);

/*==============================================================*/
/* Table: have_check_account                                    */
/*==============================================================*/
create table have_check_account
(
   cus_id               varchar(18) not null,
   bra_name             varchar(16) not null,
   acc_id               char(16),
   che_last_visit_date  datetime,
   primary key (cus_id, bra_name)
);

/*==============================================================*/
/* Table: have_store_account                                    */
/*==============================================================*/
create table have_store_account
(
   cus_id               varchar(18) not null,
   bra_name             varchar(16) not null,
   acc_id               char(16),
   sto_last_visit_date  datetime,
   primary key (cus_id, bra_name)
);

/*==============================================================*/
/* Table: loan                                                  */
/*==============================================================*/
create table loan
(
   loa_id               bigint not null auto_increment,
   bra_name             varchar(16) not null,
   loa_amount           double not null,
   primary key (loa_id)
);

alter table loan comment '这里可能可以加入一个待付贷款额，但不小心可能造成数据不一致';

/*==============================================================*/
/* Table: loan_relation                                         */
/*==============================================================*/
create table loan_relation
(
   cus_id               varchar(18) not null,
   loa_id               bigint not null,
   primary key (cus_id, loa_id)
);

/*==============================================================*/
/* Table: pay_loan                                              */
/*==============================================================*/
create table pay_loan
(
   loa_pay_id           bigint not null auto_increment,
   loa_id               bigint not null,
   loa_pay_amount       double not null,
   loa_pay_date         datetime not null,
   primary key (loa_pay_id)
);

/*==============================================================*/
/* Table: responsibility                                        */
/*==============================================================*/
create table responsibility
(
   cus_id               varchar(18) not null,
   sta_id               varchar(18) not null,
   type                 int not null,
   primary key (cus_id, sta_id)
);

/*==============================================================*/
/* Table: staff                                                 */
/*==============================================================*/
create table staff
(
   sta_id               varchar(18) not null,
   bra_name             varchar(16) not null,
   dep_bra_name         varchar(16) not null,
   dep_id               bigint not null,
   sta_name             varchar(16) not null,
   sta_phone            varchar(16) not null,
   sta_address          varchar(32) not null,
   start_work_date      date not null,
   primary key (sta_id)
);

/*==============================================================*/
/* Table: store_account                                         */
/*==============================================================*/
create table store_account
(
   acc_id               char(16) not null,
   sto_interest_rate    double not null,
   sto_currency_type    varchar(16) not null,
   primary key (acc_id)
);

alter table check_account add constraint FK_checking foreign key (acc_id)
      references account (acc_id) on delete restrict on update restrict;

alter table contacts add constraint FK_contacts_relationship foreign key (cus_id)
      references customer (cus_id) on delete restrict on update restrict;

alter table department add constraint FK_department_branch foreign key (bra_name)
      references branch (bra_name) on delete restrict on update restrict;

alter table department_manager add constraint FK_department_manager_relation foreign key (bra_name, dep_id)
      references department (bra_name, dep_id) on delete restrict on update restrict;

alter table department_manager add constraint FK_manager foreign key (sta_id)
      references staff (sta_id) on delete restrict on update restrict;

alter table have_check_account add constraint FK_check_account_be_haven foreign key (acc_id)
      references check_account (acc_id) on delete restrict on update restrict;

alter table have_check_account add constraint FK_customer_have_check_account foreign key (cus_id)
      references customer (cus_id) on delete restrict on update restrict;

alter table have_check_account add constraint FK_open_check_account foreign key (bra_name)
      references branch (bra_name) on delete restrict on update restrict;

alter table have_store_account add constraint FK_customer_has_store_account foreign key (cus_id)
      references customer (cus_id) on delete restrict on update restrict;

alter table have_store_account add constraint FK_open_store_account foreign key (bra_name)
      references branch (bra_name) on delete restrict on update restrict;

alter table have_store_account add constraint FK_store_account_be_haven foreign key (acc_id)
      references store_account (acc_id) on delete restrict on update restrict;

alter table loan add constraint FK_release_loan foreign key (bra_name)
      references branch (bra_name) on delete restrict on update restrict;

alter table loan_relation add constraint FK_loan_relation foreign key (cus_id)
      references customer (cus_id) on delete restrict on update restrict;

alter table loan_relation add constraint FK_loan_relation2 foreign key (loa_id)
      references loan (loa_id) on delete restrict on update restrict;

alter table pay_loan add constraint FK_pay_loan_relation foreign key (loa_id)
      references loan (loa_id) on delete restrict on update restrict;

alter table responsibility add constraint FK_responsibility foreign key (cus_id)
      references customer (cus_id) on delete restrict on update restrict;

alter table responsibility add constraint FK_responsibility2 foreign key (sta_id)
      references staff (sta_id) on delete restrict on update restrict;

alter table staff add constraint FK_hire foreign key (bra_name)
      references branch (bra_name) on delete restrict on update restrict;

alter table staff add constraint FK_work_in foreign key (dep_bra_name, dep_id)
      references department (bra_name, dep_id) on delete restrict on update restrict;

alter table store_account add constraint FK_saving foreign key (acc_id)
      references account (acc_id) on delete restrict on update restrict;

