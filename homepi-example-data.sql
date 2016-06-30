/*
Example Data for homepi
*/
INSERT INTO `schedule_type` (`id`,`name`,`data_def`) VALUES (1,'set_lights','PiFace_ID/Value');
INSERT INTO `schedule_type` (`id`,`name`,`data_def`) VALUES (2,'exec_command','cmd');
INSERT INTO `schedule_type` (`id`,`name`,`data_def`) VALUES (3,'set_thermostat','Temp');
INSERT INTO `schedule_type` (`id`,`name`,`data_def`) VALUES (4,'set_mode','mode_id');
INSERT INTO `schedule_type` (`id`,`name`,`data_def`) VALUES (5,'set_occupied','Zone/Value');
INSERT INTO `schedule_type` (`id`,`name`,`data_def`) VALUES (6,'fetch_forcast','period');
INSERT INTO `schedule_type` (`id`,`name`,`data_def`) VALUES (7,'fetch_sunrise_sunset','null');

INSERT INTO `scheduled_task` (`id`,`name`,`type`,`data`,`enabled`,`M`,`T`,`W`,`R`,`F`,`S`,`N`,`start`,`sun_time`,`sun_mod`) VALUES (1,'Porch lights night on',1,'13/1',1,1,1,1,1,1,1,1,'21:15:00',2,'00:20:00');
INSERT INTO `scheduled_task` (`id`,`name`,`type`,`data`,`enabled`,`M`,`T`,`W`,`R`,`F`,`S`,`N`,`start`,`sun_time`,`sun_mod`) VALUES (2,'Porch lights night off',1,'13/0',1,1,1,1,1,1,1,1,'00:47:00',0,'04:30:00');
INSERT INTO `scheduled_task` (`id`,`name`,`type`,`data`,`enabled`,`M`,`T`,`W`,`R`,`F`,`S`,`N`,`start`,`sun_time`,`sun_mod`) VALUES (3,'Porch lights day on',1,'13/1',1,1,1,1,1,1,1,1,'04:57:00',0,'08:40:00');
INSERT INTO `scheduled_task` (`id`,`name`,`type`,`data`,`enabled`,`M`,`T`,`W`,`R`,`F`,`S`,`N`,`start`,`sun_time`,`sun_mod`) VALUES (4,'Porch lights day off',1,'13/0',1,1,1,1,1,1,1,1,'05:45:00',1,'00:05:00');
INSERT INTO `scheduled_task` (`id`,`name`,`type`,`data`,`enabled`,`M`,`T`,`W`,`R`,`F`,`S`,`N`,`start`,`sun_time`,`sun_mod`) VALUES (5,'Thermostat Work',3,'60',1,1,1,1,1,0,0,0,'07:47:00',0,'00:00:00');
INSERT INTO `scheduled_task` (`id`,`name`,`type`,`data`,`enabled`,`M`,`T`,`W`,`R`,`F`,`S`,`N`,`start`,`sun_time`,`sun_mod`) VALUES (6,'Thermostat Home',3,'62',1,1,1,1,1,1,0,0,'14:30:00',0,'00:00:00');
INSERT INTO `scheduled_task` (`id`,`name`,`type`,`data`,`enabled`,`M`,`T`,`W`,`R`,`F`,`S`,`N`,`start`,`sun_time`,`sun_mod`) VALUES (7,'Thermostat Night',3,'60',1,1,1,1,1,1,1,1,'22:25:00',0,'00:00:00');
INSERT INTO `scheduled_task` (`id`,`name`,`type`,`data`,`enabled`,`M`,`T`,`W`,`R`,`F`,`S`,`N`,`start`,`sun_time`,`sun_mod`) VALUES (8,'Thermostat WakeUp',3,'65',1,1,1,1,1,1,1,1,'05:30:00',0,'00:00:00');
INSERT INTO `scheduled_task` (`id`,`name`,`type`,`data`,`enabled`,`M`,`T`,`W`,`R`,`F`,`S`,`N`,`start`,`sun_time`,`sun_mod`) VALUES (9,'Night Mode',4,'3',1,1,1,1,1,1,1,1,'21:40:00',2,'00:45:00');
INSERT INTO `scheduled_task` (`id`,`name`,`type`,`data`,`enabled`,`M`,`T`,`W`,`R`,`F`,`S`,`N`,`start`,`sun_time`,`sun_mod`) VALUES (10,'Day Mode',4,'2',1,1,1,1,1,1,1,1,'06:15:00',0,'00:00:00');
INSERT INTO `scheduled_task` (`id`,`name`,`type`,`data`,`enabled`,`M`,`T`,`W`,`R`,`F`,`S`,`N`,`start`,`sun_time`,`sun_mod`) VALUES (11,'Away Mode',4,'1',1,1,1,1,1,0,0,0,'08:30:00',0,'00:00:00');
INSERT INTO `scheduled_task` (`id`,`name`,`type`,`data`,`enabled`,`M`,`T`,`W`,`R`,`F`,`S`,`N`,`start`,`sun_time`,`sun_mod`) VALUES (12,'Thermostat Weekend',3,'62',1,0,0,0,0,1,1,1,'08:00:00',0,'00:00:00');
INSERT INTO `scheduled_task` (`id`,`name`,`type`,`data`,`enabled`,`M`,`T`,`W`,`R`,`F`,`S`,`N`,`start`,`sun_time`,`sun_mod`) VALUES (13,'Set Occupied Work',5,'0/0',1,1,1,1,1,0,0,0,'08:15:00',0,'00:00:00');
INSERT INTO `scheduled_task` (`id`,`name`,`type`,`data`,`enabled`,`M`,`T`,`W`,`R`,`F`,`S`,`N`,`start`,`sun_time`,`sun_mod`) VALUES (14,'Set Occupied Night',5,'4/1',1,1,1,1,1,1,1,1,'20:35:00',0,'00:00:00');
INSERT INTO `scheduled_task` (`id`,`name`,`type`,`data`,`enabled`,`M`,`T`,`W`,`R`,`F`,`S`,`N`,`start`,`sun_time`,`sun_mod`) VALUES (15,'Forcast Today',6,'0',1,1,1,1,1,0,0,0,'06:40:00',0,'00:00:00');
INSERT INTO `scheduled_task` (`id`,`name`,`type`,`data`,`enabled`,`M`,`T`,`W`,`R`,`F`,`S`,`N`,`start`,`sun_time`,`sun_mod`) VALUES (16,'Forcast Tonight',6,'1',1,1,1,1,1,1,1,1,'16:30:00',0,'00:00:00');
INSERT INTO `scheduled_task` (`id`,`name`,`type`,`data`,`enabled`,`M`,`T`,`W`,`R`,`F`,`S`,`N`,`start`,`sun_time`,`sun_mod`) VALUES (17,'SunRise and SunSet',7,'0',1,1,1,1,1,1,1,1,'21:25:00',0,'00:00:00');
INSERT INTO `scheduled_task` (`id`,`name`,`type`,`data`,`enabled`,`M`,`T`,`W`,`R`,`F`,`S`,`N`,`start`,`sun_time`,`sun_mod`) VALUES (18,'Brayden Bed',8,'Good evening. It is now 8 30 and it is time for Brayden to go to bed.',0,1,1,1,1,1,1,1,'20:30:00',0,'00:00:00');
INSERT INTO `scheduled_task` (`id`,`name`,`type`,`data`,`enabled`,`M`,`T`,`W`,`R`,`F`,`S`,`N`,`start`,`sun_time`,`sun_mod`) VALUES (19,'School Time',8,'Good morning. It is now 6:15 and Nana will be here in 15 minutes.',0,1,1,1,1,0,0,0,'06:15:00',0,'00:00:00');
INSERT INTO `scheduled_task` (`id`,`name`,`type`,`data`,`enabled`,`M`,`T`,`W`,`R`,`F`,`S`,`N`,`start`,`sun_time`,`sun_mod`) VALUES (20,'Forcast Before Wrk',6,'0',1,1,1,1,1,1,0,0,'06:50:00',0,'00:00:00');

INSERT INTO `config` (`id`,`node`,`name`,`data`) VALUES (1,'homepi','thermostat_temp','60');
INSERT INTO `config` (`id`,`node`,`name`,`data`) VALUES (2,'homepi','delay','10');
INSERT INTO `config` (`id`,`node`,`name`,`data`) VALUES (3,'homepi','lightsoff','10');
INSERT INTO `config` (`id`,`node`,`name`,`data`) VALUES (5,'homepi','mode','2');
INSERT INTO `config` (`id`,`node`,`name`,`data`) VALUES (6,'homepi','http_port','8888');
INSERT INTO `config` (`id`,`node`,`name`,`data`) VALUES (7,'homepi','DST','0');
INSERT INTO `config` (`id`,`node`,`name`,`data`) VALUES (8,'homepi','sunrise','05:40:00');
INSERT INTO `config` (`id`,`node`,`name`,`data`) VALUES (9,'homepi','sunset','20:55:00');
INSERT INTO `config` (`id`,`node`,`name`,`data`) VALUES (10,'homepi','wunderground_api_key','');
INSERT INTO `config` (`id`,`node`,`name`,`data`) VALUES (11,'homepi','wunderground_location','NY/Buffalo');
INSERT INTO `config` (`id`,`node`,`name`,`data`) VALUES (12,'homepi','vol1','90');
INSERT INTO `config` (`id`,`node`,`name`,`data`) VALUES (13,'homepi','vol2','100');
INSERT INTO `config` (`id`,`node`,`name`,`data`) VALUES (14,'homepi','thermostat_limit_upper','78');
INSERT INTO `config` (`id`,`node`,`name`,`data`) VALUES (15,'homepi','thermostat_limit_lower','50');
INSERT INTO `config` (`id`,`node`,`name`,`data`) VALUES (16,'homepi','vol3','85');
INSERT INTO `config` (`id`,`node`,`name`,`data`) VALUES (17,'homepi','inside_zone','11');
INSERT INTO `config` (`id`,`node`,`name`,`data`) VALUES (18,'homepi','outside_zone','8');
INSERT INTO `config` (`id`,`node`,`name`,`data`) VALUES (19,'homepi','temp_interval','60');
INSERT INTO `config` (`id`,`node`,`name`,`data`) VALUES (20,'homepi','temp_mode','F');
INSERT INTO `config` (`id`,`node`,`name`,`data`) VALUES (21,'homepi','piface_boards','1');

INSERT INTO `devices` (`id`,`type`,`name`) VALUES (1,'output','light');
INSERT INTO `devices` (`id`,`type`,`name`) VALUES (2,'output','speaker');
INSERT INTO `devices` (`id`,`type`,`name`) VALUES (3,'output','thermostat');
INSERT INTO `devices` (`id`,`type`,`name`) VALUES (4,'input','motion');
INSERT INTO `devices` (`id`,`type`,`name`) VALUES (5,'input','switch');
INSERT INTO `devices` (`id`,`type`,`name`) VALUES (6,'input','temp');

INSERT INTO `pi_admin` (`id`,`user`,`pass`) VALUES (1,'homepi','homepi');

INSERT INTO `piface` (`id`,`node`,`board`,`pin`,`status`,`zone`,`device`,`name`,`enabled`,`output`,`default_value`) VALUES (1,'homepi',0,2,0,1,3,'Thermostat',1,1,1);
INSERT INTO `piface` (`id`,`node`,`board`,`pin`,`status`,`zone`,`device`,`name`,`enabled`,`output`,`default_value`) VALUES (2,'homepi',0,4,0,2,1,'Lights',1,1,1);
INSERT INTO `piface` (`id`,`node`,`board`,`pin`,`status`,`zone`,`device`,`name`,`enabled`,`output`,`default_value`) VALUES (3,'homepi',0,0,0,2,4,'Motion',1,0,1);
INSERT INTO `piface` (`id`,`node`,`board`,`pin`,`status`,`zone`,`device`,`name`,`enabled`,`output`,`default_value`) VALUES (4,'homepi',0,1,0,12,4,'Motion',1,0,0);
INSERT INTO `piface` (`id`,`node`,`board`,`pin`,`status`,`zone`,`device`,`name`,`enabled`,`output`,`default_value`) VALUES (5,'homepi',0,5,0,7,1,'Door Light',1,1,1);
INSERT INTO `piface` (`id`,`node`,`board`,`pin`,`status`,`zone`,`device`,`name`,`enabled`,`output`,`default_value`) VALUES (6,'homepi',0,6,0,3,1,'Main Lights',1,1,1);
INSERT INTO `piface` (`id`,`node`,`board`,`pin`,`status`,`zone`,`device`,`name`,`enabled`,`output`,`default_value`) VALUES (7,'homepi',0,2,0,7,5,'DVR Motion',1,0,0);
INSERT INTO `piface` (`id`,`node`,`board`,`pin`,`status`,`zone`,`device`,`name`,`enabled`,`output`,`default_value`) VALUES (8,'homepi',0,3,0,1,4,'Motion',1,0,1);
INSERT INTO `piface` (`id`,`node`,`board`,`pin`,`status`,`zone`,`device`,`name`,`enabled`,`output`,`default_value`) VALUES (9,'homepi',0,4,0,2,4,'Motion',1,0,1);
INSERT INTO `piface` (`id`,`node`,`board`,`pin`,`status`,`zone`,`device`,`name`,`enabled`,`output`,`default_value`) VALUES (10,'homepi',0,5,0,3,4,'Motion',1,0,1);
INSERT INTO `piface` (`id`,`node`,`board`,`pin`,`status`,`zone`,`device`,`name`,`enabled`,`output`,`default_value`) VALUES (11,'homepi',0,6,0,4,4,'Motion',1,0,1);
INSERT INTO `piface` (`id`,`node`,`board`,`pin`,`status`,`zone`,`device`,`name`,`enabled`,`output`,`default_value`) VALUES (12,'homepi',0,7,0,5,4,'Motion',1,0,1);
INSERT INTO `piface` (`id`,`node`,`board`,`pin`,`status`,`zone`,`device`,`name`,`enabled`,`output`,`default_value`) VALUES (13,'homepi',0,7,0,9,1,'Lights',1,1,1);

INSERT INTO `sensors` (`id`,`type`,`zone_id`,`ident`,`name`) VALUES (1,1,8,'28-03146baeecff','Outside Temp');
INSERT INTO `sensors` (`id`,`type`,`zone_id`,`ident`,`name`) VALUES (2,1,11,'28-03146bb0e5ff','Inside Temp');

INSERT INTO `speak` (`id`,`text`) VALUES (1,'Hey, what are you looking at?');

INSERT INTO `zone_type` (`id`,`name`) VALUES (1,'Room');
INSERT INTO `zone_type` (`id`,`name`) VALUES (2,'Active Room');
INSERT INTO `zone_type` (`id`,`name`) VALUES (3,'Hall/Stairs');
INSERT INTO `zone_type` (`id`,`name`) VALUES (4,'Bedroom');
INSERT INTO `zone_type` (`id`,`name`) VALUES (5,'Outside');

INSERT INTO `zones` (`id`,`name`,`type`,`occupied`,`occupied_time`,`audio`) VALUES (1,'Living Room',1,0,'2015-12-27 20:35:05',0);
INSERT INTO `zones` (`id`,`name`,`type`,`occupied`,`occupied_time`,`audio`) VALUES (2,'Basement',2,0,'2015-06-12 08:05:15',0);
INSERT INTO `zones` (`id`,`name`,`type`,`occupied`,`occupied_time`,`audio`) VALUES (3,'Kitchen',2,0,'2013-10-26 23:16:29',0);
INSERT INTO `zones` (`id`,`name`,`type`,`occupied`,`occupied_time`,`audio`) VALUES (4,'Dinning Room',1,0,'2013-10-26 23:16:29',0);
INSERT INTO `zones` (`id`,`name`,`type`,`occupied`,`occupied_time`,`audio`) VALUES (5,'Bathroom',1,0,'2013-10-26 23:16:29',0);
INSERT INTO `zones` (`id`,`name`,`type`,`occupied`,`occupied_time`,`audio`) VALUES (6,'Hall',2,0,'2013-10-26 23:16:29',0);
INSERT INTO `zones` (`id`,`name`,`type`,`occupied`,`occupied_time`,`audio`) VALUES (7,'Garage',5,0,'2016-01-30 15:23:15',0);
INSERT INTO `zones` (`id`,`name`,`type`,`occupied`,`occupied_time`,`audio`) VALUES (8,'Outside',0,0,'2013-10-27 14:59:55',0);
INSERT INTO `zones` (`id`,`name`,`type`,`occupied`,`occupied_time`,`audio`) VALUES (9,'Portch',5,0,'2013-10-26 23:16:29',0);
INSERT INTO `zones` (`id`,`name`,`type`,`occupied`,`occupied_time`,`audio`) VALUES (10,'Kids Bdrm',4,0,'2016-06-28 20:35:06',0);
INSERT INTO `zones` (`id`,`name`,`type`,`occupied`,`occupied_time`,`audio`) VALUES (11,'Master Bdrm',4,0,'2016-06-28 20:35:06',0);
INSERT INTO `zones` (`id`,`name`,`type`,`occupied`,`occupied_time`,`audio`) VALUES (12,'Closet',3,0,'2016-06-25 09:32:39',0);

INSERT INTO `input_action` (`id`,`piface_id`,`action_id`,`output_id`,`output_value`,`mode`) VALUES (1,3,1,2,1,0);
INSERT INTO `input_action` (`id`,`piface_id`,`action_id`,`output_id`,`output_value`,`mode`) VALUES (2,4,3,0,1,0);
INSERT INTO `input_action` (`id`,`piface_id`,`action_id`,`output_id`,`output_value`,`mode`) VALUES (3,7,1,5,1,0);
INSERT INTO `input_action` (`id`,`piface_id`,`action_id`,`output_id`,`output_value`,`mode`) VALUES (4,8,1,2,1,0);
INSERT INTO `input_action` (`id`,`piface_id`,`action_id`,`output_id`,`output_value`,`mode`) VALUES (5,9,1,2,1,0);
INSERT INTO `input_action` (`id`,`piface_id`,`action_id`,`output_id`,`output_value`,`mode`) VALUES (6,10,1,2,1,0);
INSERT INTO `input_action` (`id`,`piface_id`,`action_id`,`output_id`,`output_value`,`mode`) VALUES (7,11,1,5,1,0);
INSERT INTO `input_action` (`id`,`piface_id`,`action_id`,`output_id`,`output_value`,`mode`) VALUES (8,12,1,2,1,0);
INSERT INTO `input_action` (`id`,`piface_id`,`action_id`,`output_id`,`output_value`,`mode`) VALUES (9,7,2,0,0,0);
INSERT INTO `input_action` (`id`,`piface_id`,`action_id`,`output_id`,`output_value`,`mode`) VALUES (10,3,2,0,0,0);
INSERT INTO `input_action` (`id`,`piface_id`,`action_id`,`output_id`,`output_value`,`mode`) VALUES (11,4,2,0,0,0);



