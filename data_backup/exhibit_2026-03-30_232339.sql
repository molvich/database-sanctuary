CREATE TABLE `exhibit` (
  `exhibit_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `type` varchar(100) DEFAULT NULL,
  `capacity` int DEFAULT NULL,
  `species_id` int DEFAULT NULL,
  PRIMARY KEY (`exhibit_id`),
  KEY `species_id` (`species_id`),
  CONSTRAINT `exhibit_ibfk_1` FOREIGN KEY (`species_id`) REFERENCES `species` (`species_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;insert into `exhibit` (`capacity`, `exhibit_id`, `name`, `species_id`, `type`) values (3, 1, 'Bobcat Exhibit', 1, 'Big Cat');
insert into `exhibit` (`capacity`, `exhibit_id`, `name`, `species_id`, `type`) values (20, 2, 'Chimpanzee Complex', 2, 'Primate');
insert into `exhibit` (`capacity`, `exhibit_id`, `name`, `species_id`, `type`) values (3, 3, 'Bear Canyon', 3, 'Forest');
insert into `exhibit` (`capacity`, `exhibit_id`, `name`, `species_id`, `type`) values (16, 4, 'Penguin Palace', 4, 'Artic');
