CREATE DATABASE  IF NOT EXISTS `user_profiling` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `user_profiling`;
-- MySQL dump 10.13  Distrib 8.0.20, for Linux (x86_64)
--
-- Host: 192.168.20.30    Database: user_profiling
-- ------------------------------------------------------
-- Server version	5.7.29-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Associated`
--

DROP TABLE IF EXISTS `Associated`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Associated` (
  `Flow_ID` int(11) NOT NULL,
  `Associated_App_ID` int(11) NOT NULL,
  PRIMARY KEY (`Flow_ID`,`Associated_App_ID`),
  KEY `fk_Flow_ID_idx` (`Flow_ID`),
  KEY `fk_App_ID_idx` (`Associated_App_ID`),
  CONSTRAINT `fk_Associated_App_ID` FOREIGN KEY (`Associated_App_ID`) REFERENCES `application_type` (`App_ID`) ON UPDATE CASCADE,
  CONSTRAINT `fk_Flow_ID` FOREIGN KEY (`Flow_ID`) REFERENCES `Flows` (`Flow_ID`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Flows`
--

DROP TABLE IF EXISTS `Flows`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Flows` (
  `Flow_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Flow_Date_Time` varchar(45) DEFAULT NULL,
  `Source_Name` varchar(45) DEFAULT NULL,
  `Destination_Name` varchar(45) DEFAULT NULL,
  `Flow_Category` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Flow_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2823997 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`parker`@`192.168.20.44`*/ /*!50003 TRIGGER `user_profiling`.`Flows_AFTER_INSERT` AFTER INSERT ON `Flows` FOR EACH ROW
BEGIN
	UPDATE application_type Set App_Count = App_Count + 1 WHERE Application_name = new.Source_Name;
    UPDATE application_type Set App_Count = App_Count + 1 WHERE Application_name = new.Destination_Name;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `Identify_apps`
--

DROP TABLE IF EXISTS `Identify_apps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Identify_apps` (
  `App_ID` int(11) NOT NULL,
  `identify_by` varchar(45) NOT NULL,
  PRIMARY KEY (`App_ID`,`identify_by`),
  CONSTRAINT `fk_App_ID_2` FOREIGN KEY (`App_ID`) REFERENCES `application_type` (`App_ID`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `User_IP_addr` varchar(45) NOT NULL,
  `User_Name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`User_IP_addr`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`parker`@`192.168.20.44`*/ /*!50003 TRIGGER `user_profiling`.`Users_AFTER_INSERT` AFTER INSERT ON `Users` FOR EACH ROW

BEGIN
	DECLARE ID INT(11);
	INSERT INTO application_type (application_name, Category) VALUES (new.User_Name, 'USERS');
    SELECT App_ID INTO ID FROM application_type WHERE application_name = new.User_Name;
    INSERT INTO Identify_apps (App_ID, identify_by) VALUES (ID, new.User_IP_Addr);
    INSERT INTO Identify_apps (App_ID, identify_by) VALUES (ID, new.User_Name);
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `application_type`
--

DROP TABLE IF EXISTS `application_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `application_type` (
  `App_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Application_name` varchar(45) DEFAULT NULL,
  `Category` varchar(45) DEFAULT NULL,
  `App_Count` int(11) DEFAULT '0',
  `time_between_flows` varchar(45) DEFAULT NULL,
  `no_required_flows` int(11) DEFAULT NULL,
  PRIMARY KEY (`App_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=123456822 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`parker`@`192.168.20.44`*/ /*!50003 TRIGGER `user_profiling`.`application_type_AFTER_INSERT` AFTER INSERT ON `application_type` FOR EACH ROW

BEGIN
    IF new.Category = "CDN" then
		INSERT INTO stats_table (App_ID) VALUES (new.App_ID);
	end if;
    
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `name_table`
--

DROP TABLE IF EXISTS `name_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `name_table` (
  `IP_address` varchar(20) NOT NULL,
  `AS_name` varchar(100) DEFAULT NULL,
  `NS_name` varchar(100) DEFAULT NULL,
  `App_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`IP_address`),
  KEY `fk_App_ID_idx` (`App_ID`),
  CONSTRAINT `fk_App_ID` FOREIGN KEY (`App_ID`) REFERENCES `application_type` (`App_ID`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `processed_nfdump_data`
--

DROP TABLE IF EXISTS `processed_nfdump_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `processed_nfdump_data` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Category` varchar(45) NOT NULL,
  `Flow_date_time` varchar(45) NOT NULL,
  `Protocol` varchar(10) NOT NULL,
  `AS_Src` varchar(100) NOT NULL,
  `AS_Dst` varchar(100) NOT NULL,
  `NS_Src` varchar(100) NOT NULL,
  `NS_Dst` varchar(100) NOT NULL,
  `Associated_1` varchar(45) DEFAULT NULL,
  `Associated_2` varchar(45) DEFAULT NULL,
  `Associated_3` varchar(45) DEFAULT NULL,
  `date_time_flow_less_specific` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=26928 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stats_table`
--

DROP TABLE IF EXISTS `stats_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stats_table` (
  `App_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Assoc_News` int(11) DEFAULT '0',
  `Assoc_Social_Media` int(11) DEFAULT '0',
  `Assoc_Streaming` int(11) DEFAULT '0',
  PRIMARY KEY (`App_ID`),
  CONSTRAINT `fk_stats_App_ID` FOREIGN KEY (`App_ID`) REFERENCES `application_type` (`App_ID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=123456819 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping events for database 'user_profiling'
--

--
-- Dumping routines for database 'user_profiling'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-10 13:36:53
