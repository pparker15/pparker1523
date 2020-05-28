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
  `Source_Name_ID` int(11) DEFAULT NULL,
  `Destination_Name_ID` int(11) DEFAULT NULL,
  `Flow_Category` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Flow_ID`),
  KEY `fk_Dest_ID_idx` (`Destination_Name_ID`),
  KEY `fk_Src_ID_idx` (`Source_Name_ID`),
  CONSTRAINT `fk_Dest_ID` FOREIGN KEY (`Destination_Name_ID`) REFERENCES `name_table` (`name_id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_Src_ID` FOREIGN KEY (`Source_Name_ID`) REFERENCES `name_table` (`name_id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=65310 DEFAULT CHARSET=latin1;
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
    DECLARE SrcID INT;
    DECLARE DstID INT;
    
	SET SrcID = (SELECT name_table.App_ID FROM name_table INNER JOIN Flows on Flows.Source_Name_ID = name_table.name_id WHERE Flows.Flow_ID = new.Flow_ID);
	UPDATE application_type SET App_Count = App_Count + 1 WHERE App_ID = SrcID;
    
	SET DstID = (SELECT name_table.App_ID FROM name_table INNER JOIN Flows on Flows.Destination_Name_ID = name_table.name_id WHERE Flows.Flow_ID = new.Flow_ID);
	UPDATE application_type SET App_Count = App_Count + 1 WHERE App_ID = DstID;
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
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=latin1;
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
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`parker`@`192.168.20.44`*/ /*!50003 TRIGGER `user_profiling`.`application_type_AFTER_DELETE` AFTER DELETE ON `application_type` FOR EACH ROW
BEGIN
	INSERT INTO application_type (App_ID, Application_name, Category) VALUES (1, "Unknown", "UNKNOWN");
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
  `name_id` int(11) NOT NULL AUTO_INCREMENT,
  `IP_address` varchar(20) DEFAULT NULL,
  `AS_name` varchar(100) DEFAULT NULL,
  `NS_name` varchar(100) DEFAULT NULL,
  `App_ID` int(11) DEFAULT NULL,
  `Assoc_Facebook` int(11) DEFAULT '0',
  `Assoc_Twitter` int(11) DEFAULT '0',
  `Assoc_BBC` int(11) DEFAULT '0',
  `Assoc_Spotify` int(11) DEFAULT '0',
  PRIMARY KEY (`name_id`),
  KEY `fk_application_ID_idx` (`App_ID`),
  CONSTRAINT `fk_application_ID` FOREIGN KEY (`App_ID`) REFERENCES `application_type` (`App_ID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7385 DEFAULT CHARSET=latin1;
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

-- Dump completed on 2020-05-28  2:10:15
