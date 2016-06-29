CREATE DATABASE `homepi` /*!40100 DEFAULT CHARACTER SET utf8 */;

CREATE TABLE `cache` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL DEFAULT 'name1',
  `data` varchar(256) NOT NULL DEFAULT 'data1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `node` varchar(45) NOT NULL,
  `name` varchar(45) NOT NULL,
  `data` varchar(45) NOT NULL,
  PRIMARY KEY (`id`,`node`,`name`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `devices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(45) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `event_action` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `piface_id` int(11) NOT NULL DEFAULT '0',
  `value` varchar(45) NOT NULL DEFAULT '0',
  `datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `input_action` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `piface_id` int(2) NOT NULL DEFAULT '0',
  `action_id` int(2) NOT NULL DEFAULT '0',
  `output_id` int(2) DEFAULT NULL,
  `output_value` int(2) DEFAULT NULL,
  `mode` int(2) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `input_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `piface_id` int(11) NOT NULL DEFAULT '0',
  `time_stamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `logging` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `node` varchar(45) NOT NULL DEFAULT 'homepi',
  `message` varchar(512) DEFAULT NULL,
  `time_stamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `modes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL DEFAULT 'mode1',
  `enabled` int(2) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `pi_admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(255) NOT NULL,
  `pass` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;

CREATE TABLE `piface` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `node` varchar(45) NOT NULL,
  `board` int(11) NOT NULL,
  `pin` int(11) NOT NULL,
  `status` int(2) NOT NULL DEFAULT '0',
  `zone` int(2) NOT NULL DEFAULT '1',
  `device` int(11) NOT NULL DEFAULT '1',
  `name` varchar(45) DEFAULT NULL,
  `enabled` int(2) NOT NULL DEFAULT '0',
  `output` int(2) NOT NULL DEFAULT '0',
  `default_value` int(2) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`,`node`,`board`,`pin`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `schedule_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `data_def` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `scheduled_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL DEFAULT 'task1',
  `type` int(2) NOT NULL DEFAULT '1',
  `data` varchar(256) NOT NULL DEFAULT 'ps',
  `enabled` int(1) NOT NULL DEFAULT '0',
  `M` int(1) NOT NULL DEFAULT '0',
  `T` int(1) NOT NULL DEFAULT '0',
  `W` int(1) NOT NULL DEFAULT '0',
  `R` int(1) NOT NULL DEFAULT '0',
  `F` int(1) NOT NULL DEFAULT '0',
  `S` int(1) NOT NULL DEFAULT '0',
  `N` int(1) NOT NULL DEFAULT '0',
  `start` time NOT NULL DEFAULT '00:04:00',
  `sun_time` int(1) NOT NULL DEFAULT '0',
  `sun_mod` time NOT NULL DEFAULT '00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `sensors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` int(11) NOT NULL DEFAULT '0',
  `zone_id` int(11) NOT NULL DEFAULT '0',
  `ident` varchar(45) NOT NULL,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `speak` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(45) NOT NULL DEFAULT 'Hello',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `tempzone` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `temp` double NOT NULL DEFAULT '0',
  `zone_id` int(11) NOT NULL DEFAULT '0',
  `date_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL DEFAULT 'user1',
  `home` int(1) NOT NULL DEFAULT '0',
  `phone_mac` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `last_seen` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `zone_action` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `zone_id` int(11) NOT NULL DEFAULT '0',
  `action_type` int(2) NOT NULL DEFAULT '0',
  `action_value` int(2) NOT NULL DEFAULT '0',
  `time_stamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `zone_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL DEFAULT 'Room',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `zones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL DEFAULT 'Room',
  `type` int(2) NOT NULL DEFAULT '1',
  `occupied` int(2) NOT NULL DEFAULT '0',
  `occupied_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `audio` int(2) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

