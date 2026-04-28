-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 26, 2026 at 10:07 PM
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
-- Database: `cats`
--

-- --------------------------------------------------------

--
-- Table structure for table `applications`
--

CREATE TABLE `applications` (
  `id` int NOT NULL DEFAULT '0',
  `full_name` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `address` text,
  `cat_id` int DEFAULT NULL,
  `household_size` int DEFAULT NULL,
  `pets` int DEFAULT NULL,
  `housing` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `applications`
--

INSERT INTO `applications` (`id`, `full_name`, `phone`, `email`, `address`, `cat_id`, `household_size`, `pets`, `housing`, `status`) VALUES
(0, 'mitha poop', '2162012901', 'mithapoop@gmail.com', '1920109', 1, 1, 12, 'Rent', 'pending');

-- --------------------------------------------------------

--
-- Table structure for table `cats`
--

CREATE TABLE `cats` (
  `id` int NOT NULL DEFAULT '0',
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
(6, 'Ginger', 0, 'Domestic Shorthair', 'A tiny kitten full of curiosity and mischief.', 'Curious, playful', 'Exploring, climbing', 'Closed doors', 'Tries to fight objects bigger than her', 'Crinkle toy', 'ginger.jpg', 0),
(0, 'Chinchi', 7, 'Russian Blue', 'Chinchi is a calm and chill cat but extremely shy.', 'Very shy, calm, observant', 'Watching cat videos, chicken', 'Fish', 'Got into a fight with another cat and now hates going outside. Tail was injured and had to be trimmed to look like Espeon.', 'Feather wand toy', 'chinchi.jpg', 0),
(101, 'Pinto', 4, 'Tuxedo', 'A calm but curious cat who loves observing everything from the best seat in the house.', 'Chill, observant, a little mischievous', 'Jumping onto high places, lounging, watching people', 'Being ignored, loud sudden noises', 'Known for randomly appearing on top of furniture he definitely should not be on.', 'Feather wand', 'pinto.jpg', 1),
(102, 'Luna', 3, 'Domestic Shorthair', 'A sleek and elegant cat with a soft side once she warms up to you.', 'Affectionate, dramatic, graceful', 'Soft blankets, stretching out, attention', 'Being disturbed while relaxing', 'Will fully extend one paw like she is posing for a renaissance painting.', 'String toy', 'luna.jpg', 1);

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE `reviews` (
  `id` int NOT NULL,
  `userid` int DEFAULT NULL,
  `rating` int DEFAULT NULL,
  `review_text` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `reviews`
--

INSERT INTO `reviews` (`id`, `userid`, `rating`, `review_text`, `created_at`) VALUES
(1, 5, 5, 'THIS PLACE IS THE BEST PLACE EVERRRR!!!!', '2026-04-26 19:52:49');

-- --------------------------------------------------------

--
-- Table structure for table `userinformation`
--

CREATE TABLE `userinformation` (
  `userid` int NOT NULL,
  `emailid` varchar(55) DEFAULT NULL,
  `username` varchar(40) DEFAULT NULL,
  `password` varchar(70) DEFAULT NULL,
  `name` varchar(70) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `userinformation`
--

INSERT INTO `userinformation` (`userid`, `emailid`, `username`, `password`, `name`) VALUES
(4, 'mithapoop@gmail.com', 'mithapoop1', '$2b$12$4W6oZrWelBdqrpXWOxep8eds4H8R8e.wnfg1giPE9Sv0TLfWXu/i.', 'mitha poop'),
(5, 'poop1@gmail.com', 'poopyehead', '$2b$12$wo.ugtuqv07rut4vuWTJZe9X616gll6EpElBCRsKPfY/NloORP9ha', 'poop1');

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
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`id`),
  ADD KEY `userid` (`userid`);

--
-- Indexes for table `userinformation`
--
ALTER TABLE `userinformation`
  ADD PRIMARY KEY (`userid`),
  ADD UNIQUE KEY `emailid` (`emailid`);

--
-- Indexes for table `userinformation`
--
ALTER TABLE `userinformation`
  ADD PRIMARY KEY (`userid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `reviews`
--
ALTER TABLE `reviews`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `userinformation`
--
ALTER TABLE `userinformation`
  MODIFY `userid` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `reviews`
--
ALTER TABLE `reviews`
  ADD CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `userinformation` (`userid`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
