Drop TABLE IF EXISTS `doctor`;
Drop TABLE IF EXISTS `admin`;
Drop TABLE IF EXISTS `patient`;
Drop TABLE IF EXISTS `technician`;
Drop TABLE IF EXISTS `scan`;
Drop TABLE IF EXISTS `doctor_schedule`;
Drop TABLE IF EXISTS `patient_diagnosis`;
Drop TABLE IF EXISTS `patient_treatment`;
Drop TABLE IF EXISTS `patient_scan`;

CREATE TABLE `doctor` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `first_name` varchar(255),
  `last_name` varchar(255),
  `phone` INTEGER UNIQUE,
  `username` varchar(255) UNIQUE,
  `password` varchar(255),
  `sex` varchar(255),
  `admin_id` INTEGER,
  FOREIGN KEY (admin_id) REFERENCES admin (id)
);

CREATE TABLE `doctor_schedule` (
  `doctor_id` INTEGER UNIQUE,
  `day` varchar(255),
  PRIMARY KEY (`doctor_id`, `day`),
  FOREIGN KEY (doctor_id) REFERENCES doctor (id)
);

CREATE TABLE `patient` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `first_name` varchar(255),
  `last_name` varchar(255),
  `phone` INTEGER UNIQUE,
  `username` varchar(255) UNIQUE,
  `password` varchar(255),
  `sex` varchar(255),
  `birth_date` date,
  `medical_history` varchar(255)
);

CREATE TABLE `patient_diagnosis` (
  `scan_id` INTEGER PRIMARY KEY,
  `patient_id` INTEGER,
  `doctor_id` INTEGER,
  `symptoms` varchar(255),
  `disease` varchar(255),
  FOREIGN KEY (patient_id) REFERENCES patient (id),
  FOREIGN KEY (scan_id) REFERENCES scan (id),
  FOREIGN KEY (doctor_id) REFERENCES doctor (id)
);

CREATE TABLE `patient_treatment` (
  `scan_id` INTEGER PRIMARY KEY,
  `patient_id` INTEGER,
  `doctor_id` INTEGER,
  `treatment` varchar(255),
  FOREIGN KEY (scan_id) REFERENCES scan (id),
  FOREIGN KEY (patient_id) REFERENCES patient (id),
  FOREIGN KEY (doctor_id) REFERENCES doctor (id)
);

CREATE TABLE `scan` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `type` varchar(255),
  `preparations` varchar(255)
);

CREATE TABLE `patient_scan` (
  `scan_id` INTEGER PRIMARY KEY,
  `type` varchar(255),
  `patient_id` INTEGER,
  `technician_id` INTEGER,
  `time` datetime,
  FOREIGN KEY (patient_id) REFERENCES patient (id),
  FOREIGN KEY (scan_id) REFERENCES scan (id),
  FOREIGN KEY (technician_id) REFERENCES technician (id)
  -- `result` blob
);

CREATE TABLE `technician` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `first_name` varchar(255),
  `last_name` varchar(255),
  `phone` INTEGER UNIQUE,
  `username` varchar(255) UNIQUE,
  `password` varchar(255),
  `sex` varchar(255),
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
  `sex` varchar(255)
);
