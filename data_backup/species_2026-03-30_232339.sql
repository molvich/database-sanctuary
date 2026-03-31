CREATE TABLE `species` (
  `species_id` int NOT NULL AUTO_INCREMENT,
  `common_name` varchar(100) NOT NULL,
  `scientific_name` varchar(100) DEFAULT NULL,
  `diet_type` enum('Herbivore','Carnivore','Omnivore') DEFAULT NULL,
  PRIMARY KEY (`species_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;insert into `species` (`common_name`, `diet_type`, `scientific_name`, `species_id`) values ('Bobcat', 'Carnivore', 'Lynx rufus', 1);
insert into `species` (`common_name`, `diet_type`, `scientific_name`, `species_id`) values ('Chimpanzee', 'Omnivore', 'Pan troglodytes', 2);
insert into `species` (`common_name`, `diet_type`, `scientific_name`, `species_id`) values ('Brown Bear', 'Omnivore', 'Ursus arctos', 3);
insert into `species` (`common_name`, `diet_type`, `scientific_name`, `species_id`) values ('Emperor Penguin', 'Carnivore', 'Aptenodytes forsteri', 4);
