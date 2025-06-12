-- SQL code for creating "cards" table
CREATE TABLE IF NOT EXISTS `cards` (
`card_id`            int(11)       NOT NULL AUTO_INCREMENT	COMMENT 'the card id',
`status`             varchar(100)  NOT NULL					        COMMENT 'list status',
`project_name`       varchar(500)  NOT NULL                 COMMENT 'project board that card belongs to',
`card_content`       varchar(500)  NOT NULL                 COMMENT 'card_content',
PRIMARY KEY (`card_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Contains information for every card";