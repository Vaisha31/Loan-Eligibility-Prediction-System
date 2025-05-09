-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 18, 2025 at 09:45 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `loan_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `loan_applications`
--

CREATE TABLE `loan_applications` (
  `id` int(11) NOT NULL,
  `loan_id` varchar(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `nic` varchar(20) DEFAULT NULL,
  `contact` varchar(11) DEFAULT NULL,
  `no_of_dependents` int(11) DEFAULT NULL,
  `education` varchar(50) DEFAULT NULL,
  `self_employed` varchar(10) DEFAULT NULL,
  `income_annum` float DEFAULT NULL,
  `loan_amount` float DEFAULT NULL,
  `loan_term` int(11) DEFAULT NULL,
  `purposes` varchar(255) DEFAULT NULL,
  `cibil_score` int(11) DEFAULT NULL,
  `residential_assets_value` float DEFAULT NULL,
  `commercial_assets_value` float DEFAULT NULL,
  `luxury_assets_value` float DEFAULT NULL,
  `bank_asset_value` float DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `document_paths` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `loan_applications`
--

INSERT INTO `loan_applications` (`id`, `loan_id`, `name`, `nic`, `contact`, `no_of_dependents`, `education`, `self_employed`, `income_annum`, `loan_amount`, `loan_term`, `purposes`, `cibil_score`, `residential_assets_value`, `commercial_assets_value`, `luxury_assets_value`, `bank_asset_value`, `status`, `created_at`, `document_paths`) VALUES
(0, '2141241', 'Myra Snyder', 'Nisi consectetur se', '0774241242', 7, 'Graduate', 'Yes', 174, 4730000, 30, 'Education', 422, 19, 84, 96, 41, 'pending', '2025-01-18 19:07:37', NULL),
(1, '84545', 'Varanan', '98293294v', '0774241242', 2, 'Graduate', 'Yes', 12000000, 4730000, 3, 'Education', 780, 1900000, 840000, 960000, 410000, 'approved', '2025-01-18 19:07:37', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`) VALUES
(1, 'admin', 'admin123', 'admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `loan_applications`
--
ALTER TABLE `loan_applications`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `loan_id` (`loan_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
