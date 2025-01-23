--create perfumes_categories table
create table product_categories(id int auto_increment primary key,
categories varchar(100)
);


--create perfumes_names table
create table product_details(id int auto_increment primary key,
category_id int,
product_name varchar(100),
product_description varchar(255),
product_price int,
foreign key (category_id) references product_categories(id)
);


--creating perfumes_html
create table product_html(id int auto_increment primary key,
category_id int,
htmlcode longtext,
foreign key (category_id) references product_categories(id)
);

