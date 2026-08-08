-- ==========================================
-- SQL SCRIPT 1: Top 100 Athletes
-- ==========================================

SELECT TOP (100)
    [PersonName],
    [Country],
    [Discipline]
FROM [TokyoOlympicDB].[dbo].[athletes];


-- ==========================================
-- SQL SCRIPT 2: Olympic Analysis Queries
-- ==========================================

-- Count number of athletes from each country
SELECT Country, COUNT(*) AS TotalAthletes
FROM athletes
GROUP BY Country
ORDER BY TotalAthletes DESC;


-- Calculate the total medals won by each country
SELECT TeamCountry,
       SUM(Gold) AS Total_Gold,
       SUM(Silver) AS Total_Silver,
       SUM(Bronze) AS Total_Bronze
FROM medals
GROUP BY TeamCountry
ORDER BY Total_Gold DESC;


-- Calculate the average number of entries by gender for each discipline
SELECT Discipline,
       AVG(Female) AS Avg_Female,
       AVG(Male) AS Avg_Male
FROM entriesgender
GROUP BY Discipline;