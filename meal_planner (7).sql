-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 29, 2025 at 11:23 AM
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
-- Database: `meal_planner`
--

-- --------------------------------------------------------

--
-- Table structure for table `allergens`
--

CREATE TABLE `allergens` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `allergens`
--

INSERT INTO `allergens` (`id`, `name`) VALUES
(2, 'Telur'),
(3, 'Seafood'),
(4, 'Kacang'),
(5, 'Gluten'),
(6, 'Susu'),
(7, 'Kedelai'),
(8, 'Wijen');

-- --------------------------------------------------------

--
-- Table structure for table `ingredients`
--

CREATE TABLE `ingredients` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `price_per_unit` decimal(10,2) NOT NULL,
  `unit` varchar(20) NOT NULL,
  `allergen_id` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ingredients`
--

INSERT INTO `ingredients` (`id`, `name`, `price_per_unit`, `unit`, `allergen_id`) VALUES
(1, 'Beras Putih (5kg)', 75000.00, 'karung', NULL),
(2, 'Minyak Goreng (1L)', 18000.00, 'botol', NULL),
(3, 'Telur Ayam (10 butir)', 25000.00, 'pack', '2'),
(4, 'Roti Tawar (1 bungkus)', 15000.00, 'bungkus', '5'),
(5, 'Bawang Merah (250g)', 12000.00, 'bungkus', NULL),
(6, 'Bawang Putih (250g)', 10000.00, 'bungkus', NULL),
(7, 'Cabai Merah (250g)', 15000.00, 'bungkus', NULL),
(8, 'Kecap Manis (Botol Kecil)', 10000.00, 'botol', '7'),
(9, 'Wortel (500g)', 8000.00, 'bungkus', NULL),
(10, 'Bayam (1 ikat)', 5000.00, 'ikat', NULL),
(11, 'Dada Ayam Fillet (500g)', 35000.00, 'pack', NULL),
(12, 'Udang Segar (500g)', 45000.00, 'pack', '3'),
(13, 'Daging Sapi (500g)', 65000.00, 'pack', NULL),
(14, 'Kacang Tanah (250g)', 15000.00, 'bungkus', '4'),
(15, 'Susu UHT (1L)', 19000.00, 'kotak', '6'),
(16, 'Tepung Terigu (1kg)', 12000.00, 'bungkus', '5'),
(17, 'Mie Telur Kering', 6000.00, 'bungkus', '5'),
(18, 'Tahu Putih (1 kotak)', 5000.00, 'kotak', '7'),
(19, 'Tempe (1 papan)', 6000.00, 'papan', '7'),
(20, 'Bakso Sapi (1 bungkus)', 25000.00, 'bungkus', '5'),
(21, 'Sosis Sapi (1 pack)', 22000.00, 'pack', NULL),
(22, 'Keju Cheddar (1 blok)', 20000.00, 'blok', '6'),
(23, 'Ikan Lele (1 kg)', 25000.00, 'kg', '3'),
(24, 'Ikan Kembung (1 kg)', 35000.00, 'kg', '3'),
(25, 'Cumi-Cumi Segar (500g)', 40000.00, 'pack', '3'),
(26, 'Teri Medan (100g)', 15000.00, 'bungkus', '3'),
(27, 'Kangkung (1 ikat)', 3000.00, 'ikat', NULL),
(28, 'Sawi Hijau (1 ikat)', 4000.00, 'ikat', NULL),
(29, 'Kol/Kubis (1 kg)', 10000.00, 'kg', NULL),
(30, 'Tauge (250g)', 3000.00, 'bungkus', '7'),
(31, 'Labu Siam (1 buah)', 5000.00, 'buah', NULL),
(32, 'Kacang Panjang (1 ikat)', 5000.00, 'ikat', NULL),
(33, 'Kentang (1 kg)', 18000.00, 'kg', NULL),
(34, 'Tomat Merah (500g)', 8000.00, 'bungkus', NULL),
(35, 'Daun Bawang (1 ikat)', 3000.00, 'ikat', NULL),
(36, 'Jagung Manis (1 buah)', 4000.00, 'buah', NULL),
(37, 'Santan Instan (65ml)', 3000.00, 'kotak', NULL),
(38, 'Gula Merah (250g)', 8000.00, 'bungkus', NULL),
(39, 'Terasi Udang (1 pack)', 5000.00, 'pack', '3'),
(40, 'Jahe (250g)', 5000.00, 'bungkus', NULL),
(41, 'Lengkuas (250g)', 5000.00, 'bungkus', NULL),
(42, 'Kunyit (250g)', 4000.00, 'bungkus', NULL),
(43, 'Sereh (1 ikat)', 3000.00, 'ikat', NULL),
(44, 'Daun Salam (1 ikat)', 2000.00, 'ikat', NULL),
(45, 'Daun Jeruk (1 bungkus)', 2000.00, 'bungkus', NULL),
(46, 'Kemiri (100g)', 5000.00, 'bungkus', '4'),
(47, 'Bihun Jagung (1 bungkus)', 8000.00, 'bungkus', NULL),
(48, 'Tepung Bumbu (1 bungkus)', 6000.00, 'bungkus', '5'),
(49, 'Margarin (1 sachet)', 7000.00, 'sachet', '6'),
(50, 'Garam Meja (1 bungkus)', 3000.00, 'bungkus', NULL),
(51, 'Pisang Raja (1 sisir)', 20000.00, 'sisir', NULL),
(52, 'Apel Merah (1 kg)', 35000.00, 'kg', NULL),
(53, 'Alpukat Mentega (1 kg)', 40000.00, 'kg', NULL),
(54, 'Gula Pasir (1 kg)', 16000.00, 'bungkus', NULL),
(55, 'Madu Murni (Botol Kecil)', 45000.00, 'botol', NULL),
(56, 'Daging Kambing (500g)', 75000.00, 'pack', NULL),
(57, 'Ikan Tuna Fillet (500g)', 55000.00, 'pack', '3'),
(58, 'Daging Giling Sapi (250g)', 35000.00, 'pack', NULL),
(59, 'Telur Puyuh (1 pack)', 15000.00, 'pack', '2'),
(60, 'Brokoli (1 bonggol)', 10000.00, 'bonggol', NULL),
(61, 'Kembang Kol (1 bonggol)', 12000.00, 'bonggol', NULL),
(62, 'Jamur Tiram (250g)', 10000.00, 'bungkus', NULL),
(63, 'Terong Ungu (500g)', 8000.00, 'bungkus', NULL),
(64, 'Spaghetti La Fonte (1 bungkus)', 15000.00, 'bungkus', '5'),
(65, 'Roti Burger (1 bungkus isi 6)', 18000.00, 'bungkus', '5'),
(66, 'Makaroni Kering (1 bungkus)', 8000.00, 'bungkus', '5'),
(67, 'Minyak Wijen (Botol Kecil)', 25000.00, 'botol', '8'),
(68, 'Saus Tiram (Botol Sedang)', 15000.00, 'botol', '3'),
(69, 'Tepung Maizena (1 kotak)', 8000.00, 'kotak', NULL),
(70, 'Biji Wijen Sangrai (1 botol)', 12000.00, 'botol', '8');

-- --------------------------------------------------------

--
-- Table structure for table `recipes`
--

CREATE TABLE `recipes` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL,
  `total_calories` int(11) NOT NULL,
  `meal_type` enum('Breakfast','Lunch','Dinner') NOT NULL,
  `instructions` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `recipes`
--

INSERT INTO `recipes` (`id`, `name`, `total_calories`, `meal_type`, `instructions`) VALUES
(1, 'Nasi Goreng Telur', 450, 'Breakfast', 'Tumis bumbu, masukkan nasi dan telur.'),
(2, 'Sandwich Telur', 350, 'Breakfast', 'Panggang roti, goreng telur, tumpuk.'),
(3, 'Bubur Ayam Jakarta', 400, 'Breakfast', 'Rebus beras hingga jadi bubur, suwir ayam.'),
(4, 'Ayam Kecap Mentega', 600, 'Lunch', 'Goreng ayam, tumis dengan kecap dan mentega.'),
(5, 'Udang Goreng Tepung', 550, 'Lunch', 'Balur udang dengan tepung, goreng kering.'),
(6, 'Gado-Gado Spesial', 500, 'Lunch', 'Rebus sayuran, siram bumbu kacang.'),
(7, 'Capcay Kuah', 300, 'Dinner', 'Tumis aneka sayuran dengan sedikit air.'),
(8, 'Mie Goreng Jawa', 550, 'Dinner', 'Rebus mie, tumis dengan bumbu dan sayur.'),
(9, 'Sapi Lada Hitam', 600, 'Dinner', 'Tumis daging sapi dengan saus lada hitam.'),
(10, 'Soto Ayam Bening', 400, 'Breakfast', 'Rebus ayam, masukkan bumbu soto dan bihun.'),
(11, 'Nasi Uduk Komplit', 550, 'Breakfast', 'Masak beras dengan santan, sajikan dengan orek tempe.'),
(12, 'Roti Bakar Keju', 300, 'Breakfast', 'Panggang roti dengan margarin dan parutan keju.'),
(13, 'Tumis Sawi Telur', 250, 'Breakfast', 'Tumis sawi hijau dengan orak-arik telur.'),
(14, 'Omelet Sayur', 350, 'Breakfast', 'Kocok telur dengan irisan kol dan wortel, goreng.'),
(15, 'Sayur Asem Jakarta', 150, 'Lunch', 'Rebus labu, kacang panjang, dan jagung dengan asam jawa.'),
(16, 'Pepes Tahu', 200, 'Lunch', 'Haluskan tahu dengan bumbu, kukus.'),
(17, 'Ikan Goreng Kuning', 450, 'Lunch', 'Bumbui ikan dengan kunyit, goreng kering.'),
(18, 'Tumis Kangkung Terasi', 180, 'Lunch', 'Tumis kangkung dengan bawang dan terasi.'),
(19, 'Opor Ayam Tahu', 600, 'Lunch', 'Masak ayam dan tahu dengan kuah santan kuning.'),
(20, 'Balado Telur', 300, 'Lunch', 'Rebus telur, goreng sebentar, tumis dengan sambal balado.'),
(21, 'Pecel Lele', 500, 'Lunch', 'Goreng lele, sajikan dengan sambal terasi dan lalapan.'),
(22, 'Oseng Tempe Kacang', 350, 'Lunch', 'Tumis tempe dan kacang panjang dengan kecap.'),
(23, 'Sup Bakso Sayur', 350, 'Dinner', 'Rebus bakso dengan wortel, kol, dan daun bawang.'),
(24, 'Tempe Mendoan', 400, 'Dinner', 'Balur tempe dengan tepung bumbu, goreng setengah matang.'),
(25, 'Cumi Asin Cabai Ijo', 450, 'Dinner', 'Tumis cumi asin dengan irisan cabai hijau.'),
(26, 'Perkedel Kentang', 300, 'Dinner', 'Haluskan kentang goreng, bentuk bulat, goreng.'),
(27, 'Tahu Gejrot', 250, 'Dinner', 'Potong tahu goreng, siram kuah gula merah.'),
(28, 'Bihun Goreng Spesial', 500, 'Dinner', 'Tumis bihun dengan bakso, telur, dan sawi.'),
(29, 'Gulai Ikan', 550, 'Dinner', 'Masak ikan kembung dengan kuah santan gulai.'),
(30, 'Sapo Tahu', 400, 'Dinner', 'Tumis tahu sutra dengan wortel dan sawi.'),
(31, 'Pancake Pisang Madu', 350, 'Breakfast', 'Campur pisang, telur, tepung, masak di teflon, siram madu.'),
(32, 'Jus Alpukat Toast', 400, 'Breakfast', 'Roti panggang dengan topping alpukat lumat dan telur.'),
(33, 'Nasi Goreng Kambing', 600, 'Breakfast', 'Nasi goreng dengan bumbu rempah dan potongan kambing.'),
(34, 'Sandwich Tuna Mayo', 350, 'Breakfast', 'Roti tawar isi tumisan tuna dan telur sebagai pengganti mayo.'),
(35, 'Omelet Jamur Keju', 300, 'Breakfast', 'Telur dadar isi jamur tiram dan parutan keju.'),
(36, 'Sate Kambing', 500, 'Lunch', 'Tusuk daging kambing, bakar dengan kecap.'),
(37, 'Spaghetti Bolognese', 550, 'Lunch', 'Rebus pasta, tumis daging giling dengan saus tomat.'),
(38, 'Beef Burger Homemade', 600, 'Lunch', 'Roti burger isi patty daging sapi, sayur, dan keju.'),
(39, 'Tumis Brokoli Sapi', 400, 'Lunch', 'Tumis brokoli dan daging sapi dengan saus tiram.'),
(40, 'Fuyunghai', 450, 'Lunch', 'Telur dadar tebal isi sayur dan daging/udang, siram saus asam manis.'),
(41, 'Tongseng Kambing', 600, 'Dinner', 'Masak daging kambing dengan kuah santan dan kol.'),
(42, 'Capcay Seafood', 400, 'Dinner', 'Tumis aneka sayur dengan udang atau cumi.'),
(43, 'Terong Balado', 250, 'Dinner', 'Goreng terong, tumis dengan sambal balado.'),
(44, 'Sop Makaroni Ayam', 350, 'Dinner', 'Sup bening isi ayam, makaroni, dan sayuran.'),
(45, 'Ayam Goreng Wijen', 500, 'Dinner', 'Ayam fillet balur tepung dan biji wijen, goreng krispi.');

-- --------------------------------------------------------

--
-- Table structure for table `recipe_ingredients`
--

CREATE TABLE `recipe_ingredients` (
  `id` int(11) NOT NULL,
  `recipe_id` int(11) NOT NULL,
  `ingredient_id` int(11) NOT NULL,
  `amount_needed` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `recipe_ingredients`
--

INSERT INTO `recipe_ingredients` (`id`, `recipe_id`, `ingredient_id`, `amount_needed`) VALUES
(684, 1, 1, 0.03),
(685, 1, 3, 0.10),
(686, 1, 2, 0.02),
(687, 1, 8, 0.05),
(688, 1, 5, 0.02),
(689, 2, 4, 0.20),
(690, 2, 3, 0.10),
(691, 2, 15, 0.05),
(692, 3, 1, 0.05),
(693, 3, 11, 0.10),
(694, 3, 8, 0.02),
(695, 4, 11, 0.30),
(696, 4, 8, 0.10),
(697, 4, 2, 0.05),
(698, 4, 6, 0.05),
(699, 5, 12, 0.40),
(700, 5, 16, 0.10),
(701, 5, 2, 0.10),
(702, 5, 3, 0.10),
(703, 6, 10, 0.50),
(704, 6, 9, 0.20),
(705, 6, 14, 0.30),
(706, 6, 3, 0.10),
(707, 7, 9, 0.30),
(708, 7, 10, 0.50),
(709, 7, 11, 0.10),
(710, 7, 6, 0.02),
(711, 8, 17, 0.50),
(712, 8, 3, 0.10),
(713, 8, 8, 0.05),
(714, 8, 10, 0.20),
(715, 9, 13, 0.40),
(716, 9, 8, 0.05),
(717, 9, 5, 0.05),
(718, 10, 11, 0.20),
(719, 10, 47, 0.50),
(720, 10, 43, 0.10),
(721, 10, 44, 0.10),
(722, 11, 1, 0.05),
(723, 11, 37, 0.50),
(724, 11, 19, 0.20),
(725, 11, 3, 0.10),
(726, 12, 4, 0.20),
(727, 12, 22, 0.10),
(728, 12, 49, 0.50),
(729, 13, 28, 0.50),
(730, 13, 3, 0.10),
(731, 13, 6, 0.02),
(732, 14, 3, 0.20),
(733, 14, 29, 0.10),
(734, 14, 9, 0.10),
(735, 15, 31, 0.50),
(736, 15, 32, 0.50),
(737, 15, 36, 0.50),
(738, 15, 38, 0.10),
(739, 16, 18, 0.50),
(740, 16, 3, 0.05),
(741, 16, 46, 0.02),
(742, 17, 24, 0.50),
(743, 17, 42, 0.02),
(744, 17, 2, 0.10),
(745, 18, 27, 1.00),
(746, 18, 39, 0.10),
(747, 18, 5, 0.02),
(748, 19, 11, 0.30),
(749, 19, 18, 0.30),
(750, 19, 37, 1.00),
(751, 19, 42, 0.02),
(752, 20, 3, 0.30),
(753, 20, 7, 0.20),
(754, 20, 34, 0.20),
(755, 21, 23, 0.50),
(756, 21, 2, 0.15),
(757, 21, 39, 0.10),
(758, 22, 19, 0.50),
(759, 22, 32, 0.50),
(760, 22, 8, 0.05),
(761, 23, 20, 0.50),
(762, 23, 9, 0.20),
(763, 23, 29, 0.10),
(764, 23, 35, 0.20),
(765, 24, 19, 0.50),
(766, 24, 48, 0.20),
(767, 24, 2, 0.10),
(768, 25, 25, 0.50),
(769, 25, 7, 0.20),
(770, 25, 34, 0.20),
(771, 26, 33, 0.30),
(772, 26, 3, 0.05),
(773, 26, 5, 0.02),
(774, 27, 18, 0.50),
(775, 27, 38, 0.20),
(776, 27, 7, 0.05),
(777, 28, 47, 1.00),
(778, 28, 20, 0.20),
(779, 28, 8, 0.05),
(780, 28, 28, 0.20),
(781, 29, 24, 0.50),
(782, 29, 37, 1.00),
(783, 29, 42, 0.02),
(784, 29, 41, 0.05),
(785, 30, 18, 0.50),
(786, 30, 9, 0.20),
(787, 30, 28, 0.20),
(788, 30, 20, 0.20),
(789, 31, 51, 0.20),
(790, 31, 3, 0.10),
(791, 31, 16, 0.10),
(792, 31, 55, 0.05),
(793, 32, 4, 0.20),
(794, 32, 53, 0.30),
(795, 32, 3, 0.10),
(796, 33, 1, 0.05),
(797, 33, 56, 0.20),
(798, 33, 8, 0.05),
(799, 33, 5, 0.02),
(800, 34, 4, 0.20),
(801, 34, 57, 0.20),
(802, 34, 3, 0.05),
(803, 35, 3, 0.20),
(804, 35, 62, 0.20),
(805, 35, 22, 0.10),
(806, 35, 5, 0.05),
(807, 36, 56, 0.30),
(808, 36, 8, 0.10),
(809, 36, 5, 0.05),
(810, 36, 7, 0.05),
(811, 37, 64, 0.30),
(812, 37, 58, 0.20),
(813, 37, 34, 0.30),
(814, 37, 22, 0.05),
(815, 38, 65, 0.16),
(816, 38, 58, 0.20),
(817, 38, 34, 0.10),
(818, 38, 22, 0.10),
(819, 39, 60, 0.50),
(820, 39, 13, 0.20),
(821, 39, 68, 0.05),
(822, 39, 6, 0.02),
(823, 40, 3, 0.30),
(824, 40, 12, 0.10),
(825, 40, 29, 0.10),
(826, 40, 16, 0.05),
(827, 40, 34, 0.20),
(828, 41, 56, 0.30),
(829, 41, 29, 0.20),
(830, 41, 37, 0.50),
(831, 41, 8, 0.05),
(832, 42, 12, 0.10),
(833, 42, 25, 0.10),
(834, 42, 60, 0.20),
(835, 42, 61, 0.20),
(836, 42, 24, 0.20),
(837, 43, 63, 0.50),
(838, 43, 20, 0.10),
(839, 43, 6, 0.05),
(840, 43, 8, 0.05),
(841, 44, 66, 0.20),
(842, 44, 10, 0.20),
(843, 44, 24, 0.10),
(844, 44, 60, 0.10),
(845, 44, 6, 0.02),
(846, 45, 10, 0.30),
(847, 45, 16, 0.10),
(848, 45, 70, 0.05),
(849, 45, 8, 0.05);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `allergens`
--
ALTER TABLE `allergens`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `ingredients`
--
ALTER TABLE `ingredients`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `recipes`
--
ALTER TABLE `recipes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `recipe_ingredients`
--
ALTER TABLE `recipe_ingredients`
  ADD PRIMARY KEY (`id`),
  ADD KEY `recipe_id` (`recipe_id`),
  ADD KEY `ingredient_id` (`ingredient_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `allergens`
--
ALTER TABLE `allergens`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `ingredients`
--
ALTER TABLE `ingredients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=71;

--
-- AUTO_INCREMENT for table `recipes`
--
ALTER TABLE `recipes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT for table `recipe_ingredients`
--
ALTER TABLE `recipe_ingredients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=850;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `recipe_ingredients`
--
ALTER TABLE `recipe_ingredients`
  ADD CONSTRAINT `recipe_ingredients_ibfk_1` FOREIGN KEY (`recipe_id`) REFERENCES `recipes` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `recipe_ingredients_ibfk_2` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
