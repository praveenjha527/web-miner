-- phpMyAdmin SQL Dump
-- version 2.9.2
-- http://www.phpmyadmin.net
-- 
-- Host: localhost
-- Generation Time: May 06, 2009 at 05:16 PM
-- Server version: 5.0.33
-- PHP Version: 5.2.1
-- 
-- Database: `crawler`
-- 

-- --------------------------------------------------------

-- 
-- Table structure for table `crawled`
-- 

CREATE TABLE `crawled` (
  `id` int(10) NOT NULL auto_increment,
  `host` varchar(50) collate latin1_general_ci NOT NULL,
  `url` varchar(100) collate latin1_general_ci NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci AUTO_INCREMENT=4 ;


