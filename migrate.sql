INSERT INTO `user_group`(`id`, `name`) VALUES (1, 'Biickert, Jr.'), (3, 'Demonstration');

INSERT INTO `user` (`id`, `user_group_id`, `email`, `roles`, `password`, `short_name`, `full_name`) VALUES
(1, 1, 'simon@biickert.ca', '[\"ROLE_ADMIN\", \"ROLE_USER\"]', '$2y$13$m2j.v/IF2pDem3uVE2qoeeXyDqcLVJA8N89qMqLqwcznAd9IXeLdO', 'sjb', 'Simon Biickert'),
(2, 1, 'tammy@biickert.ca', '[\"ROLE_USER\"]', '$2y$13$kXec0BIwsaaf2gKAkUHdHOObFDeJS.OYzUzNqMvWpw4Lras.JBVy6', 'tpb', 'Tammy Biickert'),
(5, 3, 'demo@biickert.ca', '[\"ROLE_USER\"]', 'not a password', 'demo', 'Demo User');

INSERT INTO `transaction_type`(`id`, `name`, `is_active`, `category`, `symbol`) SELECT `transaction_type_id`, `name`, if((`fff_transaction_type`.`IS_ACTIVE` = 'Y'),1,0), `category`, `symbol` from `fff_transaction_type`;

INSERT INTO `transaction`(`id`, `transaction_type_id`, `user_id`, `amount`, `description`, `transaction_date`, `series`) SELECT `transaction_id`, `transaction_type_id`, `user_id`, `amount`, `description`, `transaction_date`, `series_id` FROM `fff_transaction`;