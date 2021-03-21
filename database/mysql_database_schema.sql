-- MySQL dump server version 8.0.23
-- The schema file creates the main database along with two tables which are  
-- necessary for the functionality of the API service.

CREATE DATABASE  IF NOT EXISTS `urlengine`;
USE `urlengine`;

-- Table structure for table `local_api_hash`: This table stores the HMAC cryptographic 
-- hash to authenticate API requests.

DROP TABLE IF EXISTS `local_api_hash`;

CREATE TABLE `local_api_hash` (
  `hash_value` varchar(100) NOT NULL,
  PRIMARY KEY (`hash_value`)
) ENGINE=InnoDB;

-- Table structure for table `local_url_lookup`: This table contains URL entries 
-- categorized for malware lookup.

DROP TABLE IF EXISTS `local_url_lookup`;
CREATE TABLE `local_url_lookup` (
  `id` int NOT NULL AUTO_INCREMENT,
  `url` varchar(3000) DEFAULT NULL,
  `reputation` varchar(50) DEFAULT 'Uncategorized',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;
