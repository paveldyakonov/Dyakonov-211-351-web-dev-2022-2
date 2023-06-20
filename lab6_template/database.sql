-- MySQL dump 10.13  Distrib 8.0.29, for Linux (x86_64)
--
-- Host: std-mysql    Database: std_2061_exam
-- ------------------------------------------------------
-- Server version	5.7.26-0ubuntu0.16.04.1

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('b19b29a8c2f3');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_genre`
--

DROP TABLE IF EXISTS `book_genre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_genre` (
  `book_id` int(11) NOT NULL,
  `genre_id` int(11) NOT NULL,
  PRIMARY KEY (`book_id`,`genre_id`),
  KEY `fk_book_genre_genre_id_genres` (`genre_id`),
  CONSTRAINT `fk_book_genre_book_id_books` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`),
  CONSTRAINT `fk_book_genre_genre_id_genres` FOREIGN KEY (`genre_id`) REFERENCES `genres` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_genre`
--

LOCK TABLES `book_genre` WRITE;
/*!40000 ALTER TABLE `book_genre` DISABLE KEYS */;
INSERT INTO `book_genre` VALUES (31,1),(34,1),(36,1),(44,1),(51,1),(31,2),(34,2),(35,2),(36,2),(37,2),(38,2),(39,2),(40,2),(41,2),(42,2),(43,2),(44,2),(37,4),(38,4),(39,4),(40,4),(41,4),(42,4),(43,4);
/*!40000 ALTER TABLE `book_genre` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `short_desc` text NOT NULL,
  `year` varchar(4) NOT NULL,
  `pub_house` varchar(100) NOT NULL,
  `author` varchar(100) NOT NULL,
  `volume` int(11) NOT NULL,
  `rating_sum` int(11) NOT NULL,
  `rating_num` int(11) NOT NULL,
  `image_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_books_image_id_images` (`image_id`),
  CONSTRAINT `fk_books_image_id_images` FOREIGN KEY (`image_id`) REFERENCES `images` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES (31,'Эмма','* Очаровательна \r\n* Остроумна\r\n* Обеспеченна','1815','АААА','Джейн Остин',500,12,3,'d2aceb39-e9d2-486f-aba1-ad44e8ea25fd'),(34,'Великий Гэтсби','Просто супер','1925','ААА','Ф.Скотт Фицджеральд',256,0,0,'dba09995-ff67-4579-816f-e2daf288acdf'),(35,'Тарас Бульба','*Я тебя породил - я тебя и убью*','1835','МИРГОРОД','Н.В.Гоголь',400,0,0,'b2014bb4-04fe-437a-bf6e-9a6007cf4bf0'),(36,'Большие надежды','*Следует верить только фактам, а не полагаться на догадки*','1860','ААА','Чарльз Диккенс',500,10,2,'b9efae20-c068-4ec3-81cc-431796ba9072'),(37,'Гарри Поттер и философский камень','Первая из 7 книга про мальчика, *который выжил*','1997','Супер','Дж.К.Роулинг',600,0,0,'6846cfef-bac3-423b-b043-5dc116a74657'),(38,'Гарри Поттер и тайная комната','Вторая книга из серии про знаменитого волшебника','1998','ОООО','Дж.К.Роулинг',540,0,0,'ce034955-0f0b-4830-bab9-e0af8d8a4549'),(39,'Гарри Поттер и узник Азкабана','Третья книга из серии','1999','ООО','Дж.К.Роулинг',590,0,0,'7a30a9ab-39c2-46b8-8c7f-8c2f04b4e6cb'),(40,'Гарри Поттер и Кубок огня','Гарри наконец-то встретится лицом к лицу с Тёмным Лордом во плоти','2000','ТТТТТ','Дж.К.Роулинг',600,0,0,'1a33b1c0-d0c4-43a1-a699-e65582b0a06a'),(41,'Гарри Поттер и Орден Феникса','Начало подготовки к ***войне***','2003','ГГГГ','Дж.К.Роулинг',800,0,0,'255c01de-f699-477c-b664-d73308e86cc3'),(42,'Гарри Поттер и Принц-полукровка','Это уже не та детская сказка','2005','ШШШ','Дж.К.Роулинг',700,0,0,'e4667146-3913-4fad-86bb-f1e5797df83d'),(43,'Гарри Поттер и Дары Смерти','Мы наконец-то узнаем, чем закончится история о мальчике, *который выжил*','2007','ЩЩЩЩ','Дж.К.Роулинг',750,0,0,'45f7d7a4-112b-4a75-b8d8-22140c05db30'),(44,'Отцы и дети','**Актуально во все времена**','1860','ЗЗЗ','И.С.Тургенев',500,0,0,'7457f726-4c37-4b2a-baa6-7f1485c40bf6'),(51,'Гордость и предубеждение','*Роман о любви людей из разных слоёв общества*','1813','ШШШ','Джейн Остин',450,10,2,'3b6624cf-2eda-4ee2-85b9-2290479e9289');
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mark` int(11) NOT NULL,
  `text` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `book_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_comments_book_id_books` (`book_id`),
  KEY `fk_comments_user_id_users` (`user_id`),
  CONSTRAINT `fk_comments_book_id_books` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`),
  CONSTRAINT `fk_comments_user_id_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES (24,5,'# Всем советую!','2023-06-19 14:09:29',31,1),(25,5,'Автор запутывает вас с самого начала, всё очень круто!!!','2023-06-19 14:14:19',36,1),(26,3,'Прикольно конечно, но, на мой взгляд, роман Джейн Остин \"Гордость и предубеждение\" интереснее','2023-06-19 14:19:06',31,2),(27,4,'Мне понравился на четверочку','2023-06-19 14:22:10',31,3),(30,5,'# Просто класс','2023-06-19 15:16:59',36,2),(31,5,'## Это просто супер','2023-06-20 07:41:33',51,1),(32,5,'**Уважаю**','2023-06-20 07:46:08',51,2);
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genres`
--

DROP TABLE IF EXISTS `genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genres` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_genres_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genres`
--

LOCK TABLES `genres` WRITE;
/*!40000 ALTER TABLE `genres` DISABLE KEYS */;
INSERT INTO `genres` VALUES (2,'Драма'),(1,'Роман'),(3,'Ужасы'),(4,'Фантастика');
/*!40000 ALTER TABLE `genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `images`
--

DROP TABLE IF EXISTS `images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `images` (
  `id` varchar(100) NOT NULL,
  `file_name` varchar(100) NOT NULL,
  `mime_type` varchar(100) NOT NULL,
  `md5_hash` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_images_md5_hash` (`md5_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `images`
--

LOCK TABLES `images` WRITE;
/*!40000 ALTER TABLE `images` DISABLE KEYS */;
INSERT INTO `images` VALUES ('1a33b1c0-d0c4-43a1-a699-e65582b0a06a','3F3F3F3F3F3F3F.webp','image/webp','294d0c52bd6d31f43883b8064e58ed83'),('255c01de-f699-477c-b664-d73308e86cc3','Harry_Potter_and_the_Order_of_the_Phoenix__movie.jpg','image/jpeg','114f08cf7d60bf9356352af865948182'),('3b6624cf-2eda-4ee2-85b9-2290479e9289','Pride__Prejudice_2005.jpg','image/jpeg','930ad8abce238be57358122116ff7062'),('45f7d7a4-112b-4a75-b8d8-22140c05db30','203px-Harry_Potter_and_the_Deathly_Hallows._Part_2__movie.jpg','image/jpeg','3bd1fdf5a9a11595407ac12e8e9de37c'),('6846cfef-bac3-423b-b043-5dc116a74657','Harry_Potter_and_the_Philosophers_Stone__movie.jpg','image/jpeg','6205697c87b5dafce058fb81d3e2e021'),('7457f726-4c37-4b2a-baa6-7f1485c40bf6','cover.webp','image/webp','3c8a01bea184c313738a0ba1af7ac419'),('7a30a9ab-39c2-46b8-8c7f-8c2f04b4e6cb','8903.jpg','image/jpeg','878d77628b967c33a7659b3951225c0a'),('b2014bb4-04fe-437a-bf6e-9a6007cf4bf0','19429600.jpg','image/jpeg','61a1907a62243f6095cbbc12faed0c8d'),('b706efc6-dc36-4865-91bf-8e162a7af741','a-stack-of-books-an-open-book-and-a-pencil-school-supplies_69317-595.avif','image/avif','05599bf65a692801776e6144281d74b4'),('b9efae20-c068-4ec3-81cc-431796ba9072','0_24b9140b3bae9009f5b97dc8a746f11e_1360260846.jpg','image/jpeg','09ee7b9d8e51417e8048c7d875899ec9'),('ce034955-0f0b-4830-bab9-e0af8d8a4549','Harry_Potter_and_the_Chamber_of_Secrets__movie.jpg','image/jpeg','7d0cd18c27497dc7b8ac62b4bd038a2c'),('d2aceb39-e9d2-486f-aba1-ad44e8ea25fd','2020.jpg','image/jpeg','023c39e602f455c54736fdf26efc3a8c'),('dba09995-ff67-4579-816f-e2daf288acdf','125259.jpg','image/jpeg','b23ab2240be2250587abe978cfa5ccd8'),('e4667146-3913-4fad-86bb-f1e5797df83d','5518.jpg','image/jpeg','2bb2ee625a24c5122bcf20cea13a405c');
/*!40000 ALTER TABLE `images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Администратор','суперпользователь, имеет полный доступ к системе, в том числе к созданию и удалению книг'),(2,'Модератор','может редактировать данные книг и производить модерацию рецензий'),(3,'Пользователь','может оставлять рецензии');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `last_name` varchar(100) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `login` varchar(100) NOT NULL,
  `password_hash` varchar(256) NOT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_users_login` (`login`),
  KEY `fk_users_role_id_roles` (`role_id`),
  CONSTRAINT `fk_users_role_id_roles` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','pasha','pasha','admin','pbkdf2:sha256:600000$ocqyxOMroP7BgfOl$a9a37c9b370146da6391daaa1c271e8d26996d576babd8a896049b00a671036b',1),(2,'aaaa','aaaa','aaaaa','moder','pbkdf2:sha256:600000$2oeJ2nOr0L0HwYaT$b86392f78786345c280595302d76ec7a1345c6556669b32c7112e86cff1c837a',2),(3,'aaaa','aaaa','aaaaa','user','pbkdf2:sha256:600000$qdRCWyI3VtuQDE0g$a1c86be213ab428dda0efdb51ce2844908497e319b57b03291e580b3c8153f50',3);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `visits`
--

DROP TABLE IF EXISTS `visits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `visits` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `book_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_visits_book_id_books` (`book_id`),
  KEY `fk_visits_user_id_users` (`user_id`),
  CONSTRAINT `fk_visits_book_id_books` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`),
  CONSTRAINT `fk_visits_user_id_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=189 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `visits`
--

LOCK TABLES `visits` WRITE;
/*!40000 ALTER TABLE `visits` DISABLE KEYS */;
INSERT INTO `visits` VALUES (70,31,1,'2023-06-19 09:38:12'),(79,31,1,'2023-06-19 10:26:09'),(84,31,1,'2023-06-19 10:51:52'),(85,31,1,'2023-06-19 10:53:20'),(87,31,1,'2023-06-19 11:06:44'),(88,31,1,'2023-06-19 11:07:43'),(91,31,1,'2023-06-19 11:12:44'),(92,31,1,'2023-06-19 11:13:19'),(95,31,1,'2023-06-19 11:20:41'),(97,31,1,'2023-06-19 11:21:44'),(99,31,1,'2023-06-19 11:22:34'),(102,31,1,'2023-06-19 11:24:54'),(106,31,1,'2023-06-19 11:27:45'),(108,31,1,'2023-06-19 11:30:50'),(111,31,1,'2023-06-19 11:45:46'),(120,34,1,'2023-06-19 12:33:29'),(121,34,1,'2023-06-19 12:33:48'),(122,34,NULL,'2023-06-19 12:34:44'),(123,34,NULL,'2023-06-19 12:36:41'),(124,34,1,'2023-06-19 12:37:18'),(139,34,1,'2023-06-19 14:04:18'),(140,35,1,'2023-06-19 14:08:28'),(141,36,1,'2023-06-19 14:13:40'),(142,36,1,'2023-06-19 14:14:20'),(144,31,NULL,'2023-06-19 14:16:45'),(145,31,2,'2023-06-19 14:17:48'),(146,31,2,'2023-06-19 14:19:07'),(148,31,3,'2023-06-19 14:21:42'),(149,31,3,'2023-06-19 14:22:11'),(151,37,1,'2023-06-19 14:34:34'),(152,37,1,'2023-06-19 14:35:48'),(153,38,1,'2023-06-19 14:37:36'),(154,39,1,'2023-06-19 14:39:29'),(155,40,1,'2023-06-19 14:41:50'),(156,41,1,'2023-06-19 14:43:24'),(157,42,1,'2023-06-19 14:44:58'),(158,43,1,'2023-06-19 14:48:17'),(159,44,1,'2023-06-19 14:51:35'),(163,34,1,'2023-06-19 15:14:12'),(164,42,NULL,'2023-06-19 15:15:06'),(165,36,2,'2023-06-19 15:16:33'),(166,36,2,'2023-06-19 15:17:00'),(167,36,NULL,'2023-06-19 15:18:10'),(168,36,1,'2023-06-19 15:18:42'),(170,36,1,'2023-06-19 15:26:26'),(171,43,1,'2023-06-20 06:51:29'),(174,43,1,'2023-06-20 07:28:21'),(175,36,1,'2023-06-20 07:28:34'),(178,51,1,'2023-06-20 07:40:50'),(179,51,1,'2023-06-20 07:41:34'),(180,51,NULL,'2023-06-20 07:44:39'),(181,51,2,'2023-06-20 07:45:48'),(182,51,2,'2023-06-20 07:46:10'),(183,51,NULL,'2023-06-20 07:47:19'),(184,36,3,'2023-06-20 07:47:58'),(185,39,3,'2023-06-20 07:48:42'),(186,51,3,'2023-06-20 07:49:06'),(187,36,1,'2023-06-20 07:50:41'),(188,36,1,'2023-06-20 07:51:38');
/*!40000 ALTER TABLE `visits` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-20  9:56:50
