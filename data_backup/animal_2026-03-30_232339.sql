CREATE TABLE `animal` (
  `animal_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `age` int DEFAULT NULL,
  `sex` enum('M','F','Other') DEFAULT NULL,
  `health_status` varchar(100) DEFAULT NULL,
  `date_acquired` date DEFAULT NULL,
  `species_id` int DEFAULT NULL,
  `exhibit_id` int DEFAULT NULL,
  `keeper_id` int DEFAULT NULL,
  PRIMARY KEY (`animal_id`),
  KEY `species_id` (`species_id`),
  KEY `exhibit_id` (`exhibit_id`),
  KEY `keeper_id` (`keeper_id`),
  CONSTRAINT `animal_ibfk_1` FOREIGN KEY (`species_id`) REFERENCES `species` (`species_id`),
  CONSTRAINT `animal_ibfk_2` FOREIGN KEY (`exhibit_id`) REFERENCES `exhibit` (`exhibit_id`),
  CONSTRAINT `animal_ibfk_3` FOREIGN KEY (`keeper_id`) REFERENCES `keeper` (`keeper_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;insert into `animal` (`age`, `animal_id`, `date_acquired`, `exhibit_id`, `health_status`, `keeper_id`, `name`, `sex`, `species_id`) values (5, 1, '2021-03-10', 1, 'Healthy', 2, 'Chester', 'M', 1);
insert into `animal` (`age`, `animal_id`, `date_acquired`, `exhibit_id`, `health_status`, `keeper_id`, `name`, `sex`, `species_id`) values (25, 2, '2019-10-10', 2, 'Healthy', 1, 'Barry', 'M', 2);
insert into `animal` (`age`, `animal_id`, `date_acquired`, `exhibit_id`, `health_status`, `keeper_id`, `name`, `sex`, `species_id`) values (28, 3, '2018-07-20', 2, 'Healthy', 1, 'Jared', 'M', 2);
insert into `animal` (`age`, `animal_id`, `date_acquired`, `exhibit_id`, `health_status`, `keeper_id`, `name`, `sex`, `species_id`) values (38, 4, '2020-05-05', 2, 'Healthy', 1, 'Margaret', 'F', 2);
insert into `animal` (`age`, `animal_id`, `date_acquired`, `exhibit_id`, `health_status`, `keeper_id`, `name`, `sex`, `species_id`) values (16, 5, '2026-03-30', 3, 'Injured', 1, 'Jeff', 'M', 3);
