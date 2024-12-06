-- MySQL dump 10.13  Distrib 9.1.0, for macos14 (arm64)
--
-- Host: 127.0.0.1    Database: 7300
-- ------------------------------------------------------
-- Server version	9.1.0-commercial

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
-- Table structure for table `Courses`
--

DROP TABLE IF EXISTS `Courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Courses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_number` varchar(10) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `course_number` (`course_number`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Courses`
--

LOCK TABLES `Courses` WRITE;
/*!40000 ALTER TABLE `Courses` DISABLE KEYS */;
INSERT INTO `Courses` VALUES (1,'CS101','编程基础'),(2,'CS102','数据结构'),(3,'CS103','计算机网络'),(4,'CS201','操作系统'),(5,'CS202','数据库系统'),(6,'CS1111','aaaa'),(7,'CS999','computer');
/*!40000 ALTER TABLE `Courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DegreeCourses`
--

DROP TABLE IF EXISTS `DegreeCourses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `DegreeCourses` (
  `degree_id` int NOT NULL,
  `course_id` int NOT NULL,
  `is_core` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`degree_id`,`course_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `degreecourses_ibfk_1` FOREIGN KEY (`degree_id`) REFERENCES `Degrees` (`id`),
  CONSTRAINT `degreecourses_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `Courses` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DegreeCourses`
--

LOCK TABLES `DegreeCourses` WRITE;
/*!40000 ALTER TABLE `DegreeCourses` DISABLE KEYS */;
INSERT INTO `DegreeCourses` VALUES (1,1,1),(1,2,1),(1,3,0),(2,2,1),(2,4,1),(3,5,1);
/*!40000 ALTER TABLE `DegreeCourses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Degrees`
--

DROP TABLE IF EXISTS `Degrees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Degrees` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `level` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`,`level`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Degrees`
--

LOCK TABLES `Degrees` WRITE;
/*!40000 ALTER TABLE `Degrees` DISABLE KEYS */;
INSERT INTO `Degrees` VALUES (4,'aaa','BA'),(3,'信息系统','BA'),(2,'计算机科学','PhD'),(1,'软件工程','MS');
/*!40000 ALTER TABLE `Degrees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Evaluations`
--

DROP TABLE IF EXISTS `Evaluations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Evaluations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `section_id` int NOT NULL,
  `goal_id` int NOT NULL,
  `evaluation_method` varchar(255) NOT NULL,
  `grade_a` int DEFAULT '0',
  `grade_b` int DEFAULT '0',
  `grade_c` int DEFAULT '0',
  `grade_f` int DEFAULT '0',
  `improvement_suggestion` text,
  PRIMARY KEY (`id`),
  KEY `section_id` (`section_id`),
  KEY `goal_id` (`goal_id`),
  CONSTRAINT `evaluations_ibfk_1` FOREIGN KEY (`section_id`) REFERENCES `Sections` (`id`),
  CONSTRAINT `evaluations_ibfk_2` FOREIGN KEY (`goal_id`) REFERENCES `Goals` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Evaluations`
--

LOCK TABLES `Evaluations` WRITE;
/*!40000 ALTER TABLE `Evaluations` DISABLE KEYS */;
INSERT INTO `Evaluations` VALUES (1,1,1,'1',10,10,10,10,'增加实践任务'),(2,2,2,'Mid-term',15,5,5,0,'题目适当增加难度'),(3,3,3,'Final Exam',5,10,3,2,'改进试卷难度'),(4,4,4,'Project',10,5,0,0,'增加团队合作环节'),(5,5,5,'Oral Presentation',20,10,5,5,'改进演讲评分标准'),(6,9,1,'1',10,10,10,0,''),(7,14,2,'homework',15,15,15,0,'');
/*!40000 ALTER TABLE `Evaluations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Goals`
--

DROP TABLE IF EXISTS `Goals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Goals` (
  `id` int NOT NULL AUTO_INCREMENT,
  `degree_id` int NOT NULL,
  `code` char(4) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `degree_id` (`degree_id`),
  CONSTRAINT `goals_ibfk_1` FOREIGN KEY (`degree_id`) REFERENCES `Degrees` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Goals`
--

LOCK TABLES `Goals` WRITE;
/*!40000 ALTER TABLE `Goals` DISABLE KEYS */;
INSERT INTO `Goals` VALUES (1,1,'G001','掌握编程基础'),(2,1,'G002','理解数据结构和算法'),(3,2,'G003','掌握高性能计算技术'),(4,2,'G004','熟悉分布式系统架构'),(5,3,'G005','具备信息系统分析能力'),(6,3,'0001','qqqq'),(7,1,'001','zzz');
/*!40000 ALTER TABLE `Goals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Instructors`
--

DROP TABLE IF EXISTS `Instructors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Instructors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `instructor_id` char(8) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `instructor_id` (`instructor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Instructors`
--

LOCK TABLES `Instructors` WRITE;
/*!40000 ALTER TABLE `Instructors` DISABLE KEYS */;
INSERT INTO `Instructors` VALUES (1,'00000001','张三'),(2,'00000002','李四'),(3,'00000003','王五'),(4,'00000000','zzz');
/*!40000 ALTER TABLE `Instructors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Sections`
--

DROP TABLE IF EXISTS `Sections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Sections` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_id` int NOT NULL,
  `semester` varchar(6) NOT NULL,
  `year` int NOT NULL,
  `section_number` char(3) NOT NULL,
  `enrolled_students` int NOT NULL,
  `instructor_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_id` (`course_id`),
  KEY `instructor_id` (`instructor_id`),
  CONSTRAINT `sections_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `Courses` (`id`),
  CONSTRAINT `sections_ibfk_2` FOREIGN KEY (`instructor_id`) REFERENCES `Instructors` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Sections`
--

LOCK TABLES `Sections` WRITE;
/*!40000 ALTER TABLE `Sections` DISABLE KEYS */;
INSERT INTO `Sections` VALUES (1,1,'Spring',2024,'001',30,1),(2,2,'Spring',2024,'002',25,2),(3,3,'Fall',2024,'003',20,3),(4,4,'Fall',2024,'004',15,1),(5,5,'Summer',2024,'005',40,2),(9,1,'Summer',2024,'001',90,1),(11,6,'Summer',2024,'004',90,3),(12,1,'summer',2024,'101',30,1),(13,6,'Fall',2024,'105',80,2),(14,7,'Fall',2025,'105',80,4);
/*!40000 ALTER TABLE `Sections` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-06 12:00:24
