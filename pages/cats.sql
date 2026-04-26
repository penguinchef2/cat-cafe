-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 24, 2026 at 10:12 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cats`
--

-- --------------------------------------------------------

--
-- Table structure for table `applications`
--

CREATE TABLE `applications` (
  `id` int(11) NOT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `cat_id` int(11) DEFAULT NULL,
  `household_size` int(11) DEFAULT NULL,
  `pets` int(11) DEFAULT NULL,
  `housing` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cats`
--

CREATE TABLE `cats` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `breed` varchar(100) DEFAULT NULL,
  `info` text DEFAULT NULL,
  `personality` text DEFAULT NULL,
  `likes` text DEFAULT NULL,
  `dislikes` text DEFAULT NULL,
  `fun_facts` text DEFAULT NULL,
  `favorite_toy` varchar(100) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `available` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cats`
--

INSERT INTO `cats` (`id`, `name`, `age`, `breed`, `info`, `personality`, `likes`, `dislikes`, `fun_facts`, `favorite_toy`, `image`, `available`) VALUES
(1, 'Meowther', 2, 'Bombay', 'A sweet and loving cat looking for a home.', 'Calm, affectionate', 'Salmon, naps', 'Loud noises', 'Loves sitting on laptops', 'Plush mouse', 'meowther.jpg', 1),
(2, 'Shochan', 4, 'Indian Calico', 'A quiet and shy cat who prefers calm environments.', 'Introverted', 'Pets and scratches', 'Other people', 'Couldn’t meow for the first few years, so she chirped instead', 'Feather on a string', 'cathony.jpg', 1),
(3, 'Cosmo', 7, 'Domestic Shorthair', 'A calm but playful cat who loves attention and staying active.', 'Calm and fun', 'Playing, catnip, treats, mommy', 'Wet food, sleeping, letting mom sleep', 'Likes to drink water from bottle caps', 'Soft ball', 'darling2.jpg', 1),
(4, 'Medo Bektic', 6, 'Domestic Shorthair', 'A shy but sweet cat with a playful, silly side.', 'Shy, silly, and sweet', 'Dehydrated marshmallows, treats', 'The vet', 'Won a calendar contest and is Mr. October', 'Butterfly wand, baguette plushie, hedgehog squeaky toy', 'melcattie.jpg', 1),
(5, 'Catherine', 3, 'Bombay', 'A vocal and social cat who loves interacting with people.', 'Talkative, friendly', 'Attention, conversation', 'Being ignored', 'Will meow back if you talk to her', 'Bell ball', 'catherine.jpg', 1),
(6, 'Ginger', 0, 'Domestic Shorthair', 'A tiny kitten full of curiosity and mischief.', 'Curious, playful', 'Exploring, climbing', 'Closed doors', 'Tries to fight objects bigger than her', 'Crinkle toy', 'ginger.jpg', 1);

-- --------------------------------------------------------

--
-- Table structure for table `userinformation`
--

CREATE TABLE `userinformation` (
  `userid` int(11) NOT NULL,
  `emailid` varchar(55) DEFAULT NULL,
  `username` varchar(40) DEFAULT NULL,
  `password` varchar(70) DEFAULT NULL,
  `name` varchar(70) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `applications`
--
ALTER TABLE `applications`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `cats`
--
ALTER TABLE `cats`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `userinformation`
--
ALTER TABLE `userinformation`
  ADD PRIMARY KEY (`userid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `applications`
--
ALTER TABLE `applications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `cats`
--
ALTER TABLE `cats`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `userinformation`
--
ALTER TABLE `userinformation`
  MODIFY `userid` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
