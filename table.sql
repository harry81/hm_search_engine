-- developer pointer81
-- date 2/4/2012

CREATE DATABASE ''hmsearch''; 
 
GRANT ALL PRIVILEGES ON hmsearch.* TO "libbon1"@"*" IDENTIFIED BY "libbon81";
 
FLUSH PRIVILEGES;
 


drop table links;

CREATE TABLE links (
     id          MEDIUMINT NOT NULL AUTO_INCREMENT,
     link        CHAR(255) NOT NULL,
     title       CHAR(255) NOT NULL,
     parent_link CHAR(255) NOT NULL,
     numofchild  CHAR(255) NOT NULL,
     status      CHAR(128) NOT NULL,
     cr_dt       DATETIME,
     md_dt       DATETIME,
     PRIMARY KEY (id)
) ;

