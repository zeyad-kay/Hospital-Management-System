Drop TABLE IF EXISTS `doctor`;
Drop TABLE IF EXISTS `admin`;
Drop TABLE IF EXISTS `patient`;
Drop TABLE IF EXISTS `technician`;
Drop TABLE IF EXISTS `scan`;
Drop TABLE IF EXISTS `medical_check`;
Drop TABLE IF EXISTS `contact_message`;

CREATE TABLE `doctor` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `first_name` varchar(255),
  `last_name` varchar(255),
  `phone` INTEGER UNIQUE,
  `username` varchar(255) UNIQUE,
  `password` varchar(255),
  `gender` varchar(255),
  `admin_id` INTEGER,
  FOREIGN KEY (admin_id) REFERENCES admin (id)
);

CREATE TABLE `patient` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `first_name` varchar(255),
  `last_name` varchar(255),
  `phone` INTEGER UNIQUE,
  `username` varchar(255) UNIQUE,
  `password` varchar(255),
  `gender` varchar(255),
  `birth_date` date,
  `medical_history` varchar(255)
);

CREATE TABLE `medical_check` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `patient_id` INTEGER,
  `doctor_id` INTEGER,
  `diagnosis` varchar(255),
  `treatment` varchar(255),
  FOREIGN KEY (patient_id) REFERENCES patient (id),
  FOREIGN KEY (doctor_id) REFERENCES doctor (id)
);

CREATE TABLE `contact_message`(
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` varchar(255),
  `email` varchar(255),
  `message` varchar(255)
);


CREATE TABLE `scan` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `type` varchar(255),
  `file` BLOB,
  `time` datetime,
  `patient_id` INTEGER,
  `technician_id` INTEGER,
  FOREIGN KEY (patient_id) REFERENCES patient (id),
  FOREIGN KEY (technician_id) REFERENCES technician (id)
);


CREATE TABLE `technician` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `first_name` varchar(255),
  `last_name` varchar(255),
  `phone` INTEGER UNIQUE,
  `username` varchar(255) UNIQUE,
  `password` varchar(255),
  `gender` varchar(255),
  `admin_id` INTEGER,
  FOREIGN KEY (admin_id) REFERENCES admin (id)
);

CREATE TABLE `admin` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `first_name` varchar(255),
  `last_name` varchar(255),
  `phone` INTEGER UNIQUE,
  `username` varchar(255) UNIQUE,
  `password` varchar(255),
  `gender` varchar(255)
);
