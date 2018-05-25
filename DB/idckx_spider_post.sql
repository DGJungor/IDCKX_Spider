/*
Navicat MySQL Data Transfer

Source Server         : 本机
Source Server Version : 50722
Source Host           : localhost:3306
Source Database       : idckx

Target Server Type    : MYSQL
Target Server Version : 50722
File Encoding         : 65001

Date: 2018-05-25 16:58:05
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for idckx_spider_post
-- ----------------------------
DROP TABLE IF EXISTS `idckx_spider_post`;
CREATE TABLE `idckx_spider_post` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `host` varchar(20) DEFAULT NULL,
  `url` varchar(60) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `source` varchar(60) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  `keywords` varchar(60) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `content` longtext,
  `create_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6082 DEFAULT CHARSET=utf8mb4;
