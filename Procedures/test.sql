call insert_customer_with_contacts (
    '憨憨银行合肥分行',
    '350500200001011111',
    '小憨憨',
    '123456',
    '憨憨家',
    '小恐龙',
    '181111',
    '666@hanhan.com',
    '情侣',
    @ret
);

select * from customer, contacts where customer.id = contacts.cus_id;

call remove_customer_with_contacts (
    '350500200001011111',
    @ret
);

