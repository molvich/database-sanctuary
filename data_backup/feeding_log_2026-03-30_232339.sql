CREATE TABLE `feeding_log` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `fed_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `food_type` varchar(100) DEFAULT NULL,
  `quantity` varchar(50) DEFAULT NULL,
  `notes` text,
  `animal_id` int DEFAULT NULL,
  `keeper_id` int DEFAULT NULL,
  PRIMARY KEY (`log_id`),
  KEY `animal_id` (`animal_id`),
  KEY `keeper_id` (`keeper_id`),
  CONSTRAINT `feeding_log_ibfk_1` FOREIGN KEY (`animal_id`) REFERENCES `animal` (`animal_id`),
  CONSTRAINT `feeding_log_ibfk_2` FOREIGN KEY (`keeper_id`) REFERENCES `keeper` (`keeper_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;