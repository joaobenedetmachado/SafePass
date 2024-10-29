-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: vaultify
-- ------------------------------------------------------
-- Server version	5.5.20-log

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
-- Table structure for table `passwords`
--

DROP TABLE IF EXISTS `passwords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `passwords` (
  `idpassword` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) NOT NULL,
  `passwordhash` text NOT NULL,
  `sitename` text NOT NULL,
  PRIMARY KEY (`idpassword`),
  KEY `userid` (`userid`),
  CONSTRAINT `passwords_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `users` (`idusers`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passwords`
--

LOCK TABLES `passwords` WRITE;
/*!40000 ALTER TABLE `passwords` DISABLE KEYS */;
INSERT INTO `passwords` VALUES (1,1,'abc123abc','instagram'),(2,1,'naosei','123'),(3,1,'minhasenha','meusite'),(4,1,'gAAAAABnITcsMijlHf6XGmfPTMLjeXUSc7fZoynNxrg4Wi89exvFESk1bBy9FzHHSGaQ4f9sCRgBSwk_b1kbWgFxDssXZtiNsg==','b\'gAAAAABnITcsQ8nif8yAK7CtHrQrNd_8lu47KQ5fq-qPkV7-NomtJTX2e13utQ3Fn7ZLDwgAzAsrnNlgJf6u2GNXoLU3EpkAFA==\''),(5,1,'gAAAAABnITodkNcXXGyOwTGdLL4fo3-MGDCicXBdvQISoVNSF8RMS5sh-lqSrLlEsDX_YeRH9dtHHMf7xAhR1ze1WjUAb_wMDqUa3cTOoYcDtXAgwX3YdIw=','meusitetop'),(6,1,'b\'gAAAAABnIT837XCOMNh_O5o7fg_vg9qC6xbQFaCE_slsY836BfbvP4kUbciYp2o5JPJaz4ovWYCrbqUWNBIRvk20rWsv2rowwA==\'','youtube'),(7,2,'b\'gAAAAABnIT-HVPKBgcAIoPONzlvvxH2scDdvWUTDe5HB8XZsI9nHBqX1S9V03xMKuP_76rTUITvbRvjcLf6q4zwCxC-nNKeNGg==\'','instagram'),(8,5,'b\'gAAAAABnIUAifOJp-TdwHzz4gZX6ry_IQgTOBekA3j9b6O-ldUovnFt0ANaKoB9Iyn9YfxQm42ZbPpfOve365vmBxBhbkRHQXQ==\'','123');
/*!40000 ALTER TABLE `passwords` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-29 17:10:16
