--create perfumes_categories table
create table perfumes_categories(id int auto_increment primary key,
categories varchar(100)
);


--create perfumes_names table
create table perfumes_details(id int auto_increment primary key,
category_id int,
perfumes_name varchar(100),
perfumes_description varchar(255),
perfumes_price int,
foreign key (category_id) references perfumes_categories(id)
);


--creating perfumes_html
create table perfumes_html(id int auto_increment primary key,
category_id int,
htmlcode longtext,
foreign key (category_id) references perfumes_categories(id)
);

