CREATE TABLE old (
   header_hash VARCHAR(1000) PRIMARY KEY NOT NULL,
   scraping_date VARCHAR(100) NOT NULL,
   new_header VARCHAR(1000) NOT NULL,
   source VARCHAR(100) NOT NULL,
   public_date VARCHAR(100) NULL
);

CREATE TABLE current (
   header_hash VARCHAR(1000) PRIMARY KEY NOT NULL,
   scraping_date VARCHAR(100) NOT NULL,
   new_header VARCHAR(1000) NOT NULL,
   source VARCHAR(100) NOT NULL,
   public_date VARCHAR(100) NULL
);