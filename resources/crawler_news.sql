-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.6.17 - MySQL Community Server (GPL)
-- Server OS:                    Win64
-- HeidiSQL Version:             8.3.0.4694
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping database structure for crawler_news
CREATE DATABASE IF NOT EXISTS `crawler_news` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci */;
USE `crawler_news`;


-- Dumping structure for table crawler_news.site_content
CREATE TABLE IF NOT EXISTS `site_content` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cate_id` int(11) NOT NULL DEFAULT '0',
  `site` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '0',
  `url` varchar(250) COLLATE utf8_unicode_ci NOT NULL,
  `content` text COLLATE utf8_unicode_ci,
  `word_1` text COLLATE utf8_unicode_ci,
  `word_2` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `cate_id` (`cate_id`),
  KEY `site` (`site`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table crawler_news.site_content: ~0 rows (approximately)
/*!40000 ALTER TABLE `site_content` DISABLE KEYS */;
/*!40000 ALTER TABLE `site_content` ENABLE KEYS */;


-- Dumping structure for table crawler_news.visited_url
CREATE TABLE IF NOT EXISTS `visited_url` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `site` varchar(50) COLLATE utf8_unicode_ci DEFAULT '0',
  `url` varchar(250) COLLATE utf8_unicode_ci DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `url` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table crawler_news.visited_url: ~0 rows (approximately)
/*!40000 ALTER TABLE `visited_url` DISABLE KEYS */;
/*!40000 ALTER TABLE `visited_url` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
