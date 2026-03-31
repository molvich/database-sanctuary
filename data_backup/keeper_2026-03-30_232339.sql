CREATE TABLE `keeper` (
  `keeper_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `shift` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`keeper_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;insert into `keeper` (`keeper_id`, `name`, `phone`, `shift`) values (1, 'Nick McKeeper', '555-1010', 'Morning');
insert into `keeper` (`keeper_id`, `name`, `phone`, `shift`) values (2, 'John Smith', '555-9090', 'Afternoon');
