# 增加客户模块
drop procedure insert_customer_with_contacts;
delimiter //
create procedure insert_customer_with_contacts(
    in cus_id char(18),
    in cus_name varchar(16),
    in cus_phone varchar(16),
    in cus_address varchar(32),
    in con_name varchar(16),
    in con_phone varchar(16),
    in con_email varchar(32),
    in con_relation varchar(16),
    out ret int
)
begin
    declare s int default 0;
    declare continue handler for sqlexception set s = -1;

    start transaction;
    
    insert into customer (id, name, phone, address)
    values (cus_id, cus_name, cus_phone, cus_address);

    insert into contacts (cus_id, name, phone, email, relation) 
    values (cus_id, con_name, con_phone, con_email, con_relation);

    select s into ret;
    if s = 0 then
        select s as 'error_code', 'ok' as 'error_msg';
        commit;
    elseif s = 1068 then
        select s as 'error_code', 'id' as 'error_msg';
        commit;
    else
        select s as 'error_code', 'unknown error' as 'error_msg';
        rollback;
    end if;
end //
delimiter ;

# 删除客户模块
drop procedure remove_customer_with_contacts;
delimiter //
create procedure remove_customer_with_contacts(
    in cus_id char(18),
    out ret int
)
begin
    declare s int default 0;
    declare continue handler for sqlexception set s = -1;

    start transaction;

    select count(*) from have_store_account 
        where have_store_account.cus_id = cus_id
        into @store_account_count;
    select count(*) from have_check_account 
        where have_check_account.cus_id = cus_id
        into @check_account_count;
    select count(*) from loan_relation 
        where loan_relation.cus_id = cus_id
        into @loan_count;
    
    if @have_store_account > 0 then
        set s = 1;
        select s as 'error_code', 
            'still has store account' as 'error_msg';
        rollback;
    end if;
    
    if @have_check_account > 0 then
        set s = 2;
        select s as 'error_code', 
            'still has check account' as 'error_msg';
        rollback;
    end if;
    
    if @loan_relation > 0 then
        set s = 3;
        select s as 'error_code', 
            'still has loan' as 'error_msg';
        rollback;
    end if;
    
    delete from contacts where contacts.cus_id = cus_id;
    delete from customer where customer.id = cus_id;

    select s into ret;
    if s = 0 then
        select s as 'error_code', 'ok' as 'error_msg';
        commit;
    else
        select s as 'error_code', 'unknown error' as 'error_msg';
        rollback;
    end if;
end //
delimiter ;


