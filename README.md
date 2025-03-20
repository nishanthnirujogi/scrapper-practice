# scrapper-practice


--- data cleaning project

USE world_layoffs;
SELECT *
FROM layoffs;

-- 1. remove duplicates
-- 2. Standarize the Data
-- 3. Null Values or Blank Values
-- 4. Remove Any Columns

-- TO WORK DONT USE RAW DATA INSTEAD CREATE A 
-- DUPLICATE DATA OF RAW DATA
CREATE TABLE laysoff_staging
LIKE layoffs;

SELECT *
FROM laysoff_staging;

INSERT laysoff_staging
SELECT *
FROM layoffs;

SELECT company, COUNT(stage)
FROM laysoff_staging
GROUP BY company;

SELECT *
FROM laysoff_staging
WHERE company = 'Oda';

SELECT *,
ROW_NUMBER () OVER( 
PARTITION BY company, location,industry,total_laid_off, 
percentage_laid_off,`date`, stage, country, 
funds_raised_millions) AS row_numb
FROM laysoff_staging;

WITH duplicte_cte AS
(
SELECT *,
ROW_NUMBER () OVER( 
PARTITION BY company, location,industry,total_laid_off, 
percentage_laid_off,`date`, stage, country, 
funds_raised_millions) AS row_numb
FROM laysoff_staging
)
SELECT *
FROM duplicte_cte
WHERE row_numb > 1;

SELECT *
FROM laysoff_staging
WHERE company = 'Casper';

-- 

WITH duplicte_cte AS
(
SELECT *,
ROW_NUMBER () OVER( 
PARTITION BY company, location,industry,total_laid_off, 
percentage_laid_off,`date`, stage, country, 
funds_raised_millions) AS row_num
FROM laysoff_staging
)
SELECT *
FROM duplicte_cte
WHERE row_num > 1;

CREATE TABLE `laysoff_staging2` (
  `company` text,
  `location` text,
  `industry` text,
  `total_laid_off` int DEFAULT NULL,
  `percentage_laid_off` text,
  `date` text,
  `stage` text,
  `country` text,
  `funds_raised_millions` int DEFAULT NULL,
  `row_num` INT 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

SELECT *
FROM laysoff_staging2;

INSERT INTO laysoff_staging2
SELECT *,
ROW_NUMBER () OVER( 
PARTITION BY company, location,industry,total_laid_off, 
percentage_laid_off,`date`, stage, country, 
funds_raised_millions) AS row_num
FROM laysoff_staging;


SELECT *
FROM laysoff_staging2
WHERE row_num > 1; 

SET SQL_SAFE_UPDATES = 0;

DELETE
FROM laysoff_staging2
WHERE row_num > 1;

SET SQL_SAFE_UPDATES = 1;

SELECT *
FROM laysoff_staging2;

-- Standarizing the Data
SELECT DISTINCT(company)
FROM laysoff_staging2;

SELECT company, TRIM(company)
FROM laysoff_staging2;

UPDATE laysoff_staging2 
SET company = TRIM(company);

SELECT DISTINCT (industry)
FROM laysoff_staging2
ORDER BY 1;

SELECT *
FROM laysoff_staging2
WHERE industry LIKE 'Crypto%';

UPDATE laysoff_staging2
SET industry = 'Crypto'
WHERE industry LIKE 'Crypto%';

SELECT *
FROM laysoff_staging2;

SELECT DISTINCT (country)
FROM laysoff_staging2
ORDER BY 1;

SELECT DISTINCT country, TRIM(TRAILING '.' FROM country)
FROM laysoff_staging2
ORDER BY 1;

UPDATE laysoff_staging2
SET country = TRIM(TRAILING '.' FROM country)
WHERE country LIKE 'United States%';

UPDATE laysoff_staging2
SET country = 'United States'
WHERE country LIKE 'United States%';
 
ALTER TABLE laysoff_staging2 
MODIFY date DATETIME;

-- Code: 1292.Incorrect datetime value: '12/16/2022' for column 'date' at row 1
-- WE CAN MODIFY IF THE ROWS ARE IN DATA FORMAT SO CONVERT THE ROWS AND THE MODIFY!!

SELECT `date`,
STR_TO_DATE(`date`, '%m/%d/%Y')
FROM laysoff_staging2;

UPDATE laysoff_staging2
SET `date`= STR_TO_DATE(`date`, '%m/%d/%Y');

-- 3. Null Values or Blank Values
-- POPULATING DATA REQUIRES TOTAL VALUES OR TEXT DATA SIMILAR TYPES

SELECT *
FROM laysoff_staging2
WHERE total_laid_off IS NULL
AND percentage_laid_off IS NULL;

SELECT *
FROM laysoff_staging2
WHERE industry IS NULL
OR industry = '';

SELECT *
FROM laysoff_staging2
WHERE company = "Bally's Interactive";

SELECT t1.industry,t2.industry
FROM laysoff_staging2 t1
JOIN laysoff_staging2 t2
	ON t1.company = t2.company
WHERE (t1.industry IS NULL OR t1.industry = '')
AND t2.industry IS NOT NULL;

UPDATE laysoff_staging2
SET industry = NULL
WHERE industry = '';

UPDATE laysoff_staging2 t1
JOIN laysoff_staging2 t2
	ON t1.company = t2.company
SET t1.industry = t2.industry
WHERE (t1.industry IS NULL)
AND t2.industry IS NOT NULL;

-- REMOVING 

SELECT *
FROM laysoff_staging2
WHERE total_laid_off IS NULL
AND percentage_laid_off IS NULL;

DELETE
FROM laysoff_staging2
WHERE total_laid_off IS NULL
AND percentage_laid_off IS NULL;

ALTER TABLE laysoff_staging2 
DROP COLUMN row_num;

SELECT *
FROM laysoff_staging2;



