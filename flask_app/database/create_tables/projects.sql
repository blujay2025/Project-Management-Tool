-- SQL code for creating "projects" table
CREATE TABLE IF NOT EXISTS `projects` (
`project_id`         int(11)       NOT NULL AUTO_INCREMENT	COMMENT 'the project id',
`email`              varchar(100)  NOT NULL					        COMMENT 'the email',
`project_name`       varchar(500)  NOT NULL                 COMMENT 'project board name',
PRIMARY KEY (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Contains association of user to projects";