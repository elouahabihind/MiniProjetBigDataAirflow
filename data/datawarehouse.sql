-- MySQL dump 10.13  Distrib 8.0.39, for Linux (x86_64)
--
-- Host: localhost    Database: datawarehouse
-- ------------------------------------------------------
-- Server version	8.0.39-0ubuntu0.24.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `dim_city`
--

DROP TABLE IF EXISTS `dim_city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dim_city` (
  `city_id` int NOT NULL AUTO_INCREMENT,
  `city` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`city_id`),
  UNIQUE KEY `city` (`city`)
) ENGINE=InnoDB AUTO_INCREMENT=321 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dim_country`
--

DROP TABLE IF EXISTS `dim_country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dim_country` (
  `country_id` int NOT NULL AUTO_INCREMENT,
  `country` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`country_id`),
  UNIQUE KEY `country` (`country`)
) ENGINE=InnoDB AUTO_INCREMENT=126 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dim_day`
--

DROP TABLE IF EXISTS `dim_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dim_day` (
  `day_id` int NOT NULL AUTO_INCREMENT,
  `day` int DEFAULT NULL,
  PRIMARY KEY (`day_id`),
  UNIQUE KEY `day` (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dim_month`
--

DROP TABLE IF EXISTS `dim_month`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dim_month` (
  `month_id` int NOT NULL AUTO_INCREMENT,
  `month` int DEFAULT NULL,
  PRIMARY KEY (`month_id`),
  UNIQUE KEY `month` (`month`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dim_region`
--

DROP TABLE IF EXISTS `dim_region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dim_region` (
  `region_id` int NOT NULL AUTO_INCREMENT,
  `region` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`region_id`),
  UNIQUE KEY `region` (`region`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dim_year`
--

DROP TABLE IF EXISTS `dim_year`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dim_year` (
  `year_id` int NOT NULL AUTO_INCREMENT,
  `year` int DEFAULT NULL,
  PRIMARY KEY (`year_id`),
  UNIQUE KEY `year` (`year`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fact_humidity`
--

DROP TABLE IF EXISTS `fact_humidity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fact_humidity` (
  `humidity_id` int NOT NULL AUTO_INCREMENT,
  `city_id` int DEFAULT NULL,
  `region_id` int DEFAULT NULL,
  `country_id` int DEFAULT NULL,
  `year_id` int DEFAULT NULL,
  `month_id` int DEFAULT NULL,
  `day_id` int DEFAULT NULL,
  `humidity` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`humidity_id`),
  KEY `city_id` (`city_id`),
  KEY `year_id` (`year_id`),
  KEY `month_id` (`month_id`),
  KEY `day_id` (`day_id`),
  KEY `region_id` (`region_id`),
  KEY `country_id` (`country_id`),
  CONSTRAINT `fact_humidity_ibfk_1` FOREIGN KEY (`city_id`) REFERENCES `dim_city` (`city_id`),
  CONSTRAINT `fact_humidity_ibfk_2` FOREIGN KEY (`year_id`) REFERENCES `dim_year` (`year_id`),
  CONSTRAINT `fact_humidity_ibfk_3` FOREIGN KEY (`month_id`) REFERENCES `dim_month` (`month_id`),
  CONSTRAINT `fact_humidity_ibfk_4` FOREIGN KEY (`day_id`) REFERENCES `dim_day` (`day_id`),
  CONSTRAINT `fact_humidity_ibfk_5` FOREIGN KEY (`region_id`) REFERENCES `dim_region` (`region_id`),
  CONSTRAINT `fact_humidity_ibfk_6` FOREIGN KEY (`country_id`) REFERENCES `dim_country` (`country_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1183 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fact_pressure`
--

DROP TABLE IF EXISTS `fact_pressure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fact_pressure` (
  `pressure_id` int NOT NULL AUTO_INCREMENT,
  `city_id` int DEFAULT NULL,
  `year_id` int DEFAULT NULL,
  `region_id` int DEFAULT NULL,
  `country_id` int DEFAULT NULL,
  `month_id` int DEFAULT NULL,
  `day_id` int DEFAULT NULL,
  `pressure` decimal(7,2) DEFAULT NULL,
  PRIMARY KEY (`pressure_id`),
  KEY `city_id` (`city_id`),
  KEY `year_id` (`year_id`),
  KEY `month_id` (`month_id`),
  KEY `region_id` (`region_id`),
  KEY `country_id` (`country_id`),
  KEY `day_id` (`day_id`),
  CONSTRAINT `fact_pressure_ibfk_1` FOREIGN KEY (`city_id`) REFERENCES `dim_city` (`city_id`),
  CONSTRAINT `fact_pressure_ibfk_2` FOREIGN KEY (`year_id`) REFERENCES `dim_year` (`year_id`),
  CONSTRAINT `fact_pressure_ibfk_3` FOREIGN KEY (`month_id`) REFERENCES `dim_month` (`month_id`),
  CONSTRAINT `fact_pressure_ibfk_4` FOREIGN KEY (`region_id`) REFERENCES `dim_region` (`region_id`),
  CONSTRAINT `fact_pressure_ibfk_5` FOREIGN KEY (`country_id`) REFERENCES `dim_country` (`country_id`),
  CONSTRAINT `fact_pressure_ibfk_6` FOREIGN KEY (`day_id`) REFERENCES `dim_day` (`day_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1183 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fact_temp`
--

DROP TABLE IF EXISTS `fact_temp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fact_temp` (
  `temp_id` int NOT NULL AUTO_INCREMENT,
  `region_id` int DEFAULT NULL,
  `country_id` int DEFAULT NULL,
  `city_id` int DEFAULT NULL,
  `month_id` int DEFAULT NULL,
  `day_id` int DEFAULT NULL,
  `year_id` int DEFAULT NULL,
  `temperature` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`temp_id`),
  KEY `region_id` (`region_id`),
  KEY `country_id` (`country_id`),
  KEY `city_id` (`city_id`),
  KEY `month_id` (`month_id`),
  KEY `day_id` (`day_id`),
  KEY `year_id` (`year_id`),
  CONSTRAINT `fact_temp_ibfk_1` FOREIGN KEY (`region_id`) REFERENCES `dim_region` (`region_id`),
  CONSTRAINT `fact_temp_ibfk_2` FOREIGN KEY (`country_id`) REFERENCES `dim_country` (`country_id`),
  CONSTRAINT `fact_temp_ibfk_3` FOREIGN KEY (`city_id`) REFERENCES `dim_city` (`city_id`),
  CONSTRAINT `fact_temp_ibfk_4` FOREIGN KEY (`month_id`) REFERENCES `dim_month` (`month_id`),
  CONSTRAINT `fact_temp_ibfk_5` FOREIGN KEY (`day_id`) REFERENCES `dim_day` (`day_id`),
  CONSTRAINT `fact_temp_ibfk_6` FOREIGN KEY (`year_id`) REFERENCES `dim_year` (`year_id`)
) ENGINE=InnoDB AUTO_INCREMENT=38811 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fact_wind`
--

DROP TABLE IF EXISTS `fact_wind`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fact_wind` (
  `wind_id` int NOT NULL AUTO_INCREMENT,
  `city_id` int DEFAULT NULL,
  `year_id` int DEFAULT NULL,
  `region_id` int DEFAULT NULL,
  `country_id` int DEFAULT NULL,
  `month_id` int DEFAULT NULL,
  `day_id` int DEFAULT NULL,
  `wind_speed` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`wind_id`),
  KEY `city_id` (`city_id`),
  KEY `year_id` (`year_id`),
  KEY `region_id` (`region_id`),
  KEY `country_id` (`country_id`),
  KEY `month_id` (`month_id`),
  KEY `day_id` (`day_id`),
  CONSTRAINT `fact_wind_ibfk_1` FOREIGN KEY (`city_id`) REFERENCES `dim_city` (`city_id`),
  CONSTRAINT `fact_wind_ibfk_2` FOREIGN KEY (`year_id`) REFERENCES `dim_year` (`year_id`),
  CONSTRAINT `fact_wind_ibfk_3` FOREIGN KEY (`region_id`) REFERENCES `dim_region` (`region_id`),
  CONSTRAINT `fact_wind_ibfk_4` FOREIGN KEY (`country_id`) REFERENCES `dim_country` (`country_id`),
  CONSTRAINT `fact_wind_ibfk_5` FOREIGN KEY (`month_id`) REFERENCES `dim_month` (`month_id`),
  CONSTRAINT `fact_wind_ibfk_6` FOREIGN KEY (`day_id`) REFERENCES `dim_day` (`day_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1183 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-10  0:26:51
