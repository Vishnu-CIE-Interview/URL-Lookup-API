-- MySQL data server version 8.0.23
-- The data dump contains URL lookup malware categorization for huge number of -- URLs. This froms the backend datastore for the URL Lookup API service.


-- Dumping data for table `local_api_hash`
-- Inserting test cryptographic hash to enable the user authentication token: 
-- "user-token-555", which is used for initial testing. This token is passed in
-- the HTTP header as 'X-Api-Key'.

LOCK TABLES `local_api_hash` WRITE;
INSERT INTO `local_api_hash` VALUES ('6d564be269a44389e5dd0fee352a854dbe62c7cc9cacc9a84b63e12487102e69');
UNLOCK TABLES;

-- Dumping URL lookup data for table `local_url_lookup`. 
LOCK TABLES `local_url_lookup` WRITE;

UNLOCK TABLES;
