-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 23, 2026 at 03:59 PM
-- Server version: 9.6.0
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cat_cafe`
--

-- --------------------------------------------------------

--
-- Table structure for table `cats`
--

CREATE TABLE `cats` (
  `id` int NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `breed` varchar(100) DEFAULT NULL,
  `info` text,
  `personality` text,
  `likes` text,
  `dislikes` text,
  `fun_facts` text,
  `favorite_toy` varchar(100) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `available` tinyint(1) DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `cats`
--

INSERT INTO `cats` (`id`, `name`, `age`, `breed`, `info`, `personality`, `likes`, `dislikes`, `fun_facts`, `favorite_toy`, `image`, `available`) VALUES
(1, 'Meowther', 2, 'Bombay', 'A sweet and loving cat looking for a home.', 'Calm, affectionate', 'Salmon, naps', 'Loud noises', 'Loves sitting on laptops', 'Plush mouse', 'meowther.jpg', 1),
(2, 'Shochan', 4, 'Indian Calico', 'A quiet and shy cat who prefers calm environments.', 'Introverted', 'Pets and scratches', 'Other people', 'Couldn’t meow for the first few years, so she chirped instead', 'Feather on a string', 'cathony.jpg', 1),
(3, 'Cosmo', 7, 'Domestic Shorthair', 'A calm but playful cat who loves attention and staying active.', 'Calm and fun', 'Playing, catnip, treats, mommy', 'Wet food, sleeping, letting mom sleep', 'Likes to drink water from bottle caps', 'Soft ball', 'darling2.jpg', 0),
(4, 'Medo Bektic', 6, 'Domestic Shorthair', 'A shy but sweet cat with a playful, silly side.', 'Shy, silly, and sweet', 'Dehydrated marshmallows, treats', 'The vet', 'Won a calendar contest and is Mr. October', 'Butterfly wand, baguette plushie, hedgehog squeaky toy', 'melcattie.jpg', 1),
(5, 'Catherine', 3, 'Bombay', 'A vocal and social cat who loves interacting with people.', 'Talkative, friendly', 'Attention, conversation', 'Being ignored', 'Will meow back if you talk to her', 'Bell ball', 'catherine.jpg', 1),
(6, 'Ginger', 0, 'Domestic Shorthair', 'A tiny kitten full of curiosity and mischief.', 'Curious, playful', 'Exploring, climbing', 'Closed doors', 'Tries to fight objects bigger than her', 'Crinkle toy', 'ginger.jpg', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cats`
--
ALTER TABLE `cats`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cats`
--
ALTER TABLE `cats`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
