CREATE TABLE Development(  
    country_name varchar(50),
    AveragScore float,
    SafetySecurity float,
    PersonelFreedom float,
    Governance float,
    SocialCapital float,
    InvestmentEnvironment float,
    EnterpriseConditions float,
    MarketAccessInfrastructure float,
    EconomicQuality float,
    LivingConditions float,
    Health float,
    Education float,
    NaturalEnvironment float,
    PRIMARY KEY (country_name)
);

load data local infile './Development-data.csv'
into table Development
fields terminated by ','
lines terminated by '\n'
ignore 1 lines;

CREATE TABLE World_data(  
    country_name2 varchar(50),
    PopulationDensity int,
    Abbreviation varchar(50),
    Agricultural_Land_Percentage float,
    LandArea int,
    ArmedForcesSize float default 0,
    BirthRate float,
    CallingCode varchar(50),
    Capital varchar(50),
    CO2Emissions float,
    CPI float,
    CPIChange_Percentage float,
    CurrencyCode varchar(50),
    FertilityRate float,
    ForestedArea_Percentage float,
    Gasoline_Price float,
    GDP bigint,
    GrossPrimaryEducationEnrollment_Percentage float,
    GrossTertiaryEducationEnrollment_Percentage float,
    InfantMortality float,
    LargestCity varchar(50),
    LifeExpectancy float,
    MaternalMortalityRatio float,
    MinimumWage float,
    OfficialLanguage varchar(50),
    OutofPocketHealthExpenditure_Percentage float,
    PhysiciansperThousand float,
    Population bigint,
    LaborForceParticipation_Percentage float,
    TaxRevenue_Percentage float,
    TotalTaxRate_Percentage float,
    UnemploymentRate_Percentage float,
    UrbanPopulation int,
    Latitude DECIMAL(10, 6),
    Longitude DECIMAL(10, 6),
    PRIMARY KEY (country_name2)
);

load data local infile './world-data-2023_cleaned.csv'
into table World_data
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;


CREATE TABLE world_happiness(  
    country_name3 varchar(50),
    Regional_indicator varchar(50),
    Ladder_score float,
    Upper_whisker float,
    Lower_whisker float,
    Log_GDP_per_capita float,
    Social_support float,
    Healthy_life_expectancy float,
    Freedom_to_make_life_choices float,
    Generosity float,
    Perceptions_of_corruption float,
    Dystopia_residual float,
    PRIMARY KEY (country_name3,Regional_indicator)
);

load data local infile './World-happiness-report-2024.csv'
into table world_happiness
fields terminated by ','
lines terminated by '\n'
ignore 1 lines;

CREATE TABLE countryinfo as
Select temp.country_name, temp.LandArea, temp.PopulationDensity, temp.ArmedForcesSize, temp.ForestedArea_Percentage, 
       temp.SafetySecurity, temp.Governance, temp.PersonelFreedom, temp.Education, temp.Health,  temp.CPI
From (Select D.country_name, D.AveragScore, D.SafetySecurity, D.PersonelFreedom, D.Governance, D.SocialCapital, D.InvestmentEnvironment, D.EnterpriseConditions, D.MarketAccessInfrastructure, D.EconomicQuality, D.LivingConditions, D.Health, D.Education, D.NaturalEnvironment,
             WD.PopulationDensity, WD.Abbreviation, WD.Agricultural_Land_Percentage, WD.LandArea, WD.ArmedForcesSize, WD.BirthRate, WD.CallingCode, WD.Capital, WD.CO2Emissions, WD.CPI, WD.CPIChange_Percentage, WD.CurrencyCode, WD.FertilityRate, WD.ForestedArea_Percentage, WD.Gasoline_Price, WD.GDP, WD.GrossPrimaryEducationEnrollment_Percentage, WD.GrossTertiaryEducationEnrollment_Percentage, WD.InfantMortality, WD.LargestCity, WD.LifeExpectancy, WD.MaternalMortalityRatio, WD.MinimumWage, WD.OfficialLanguage, WD.OutofPocketHealthExpenditure_Percentage, WD.PhysiciansperThousand, WD.Population, WD.LaborForceParticipation_Percentage, WD.TaxRevenue_Percentage, WD.TotalTaxRate_Percentage, WD.UnemploymentRate_Percentage, WD.UrbanPopulation, WD.Latitude, WD.Longitude
      From Development AS D 
      Inner join World_data AS WD ON D.country_name = WD.country_name2) AS temp
Inner join world_happiness AS WH
ON temp.country_name = WH.country_name3;

ALTER TABLE countryinfo
ADD COLUMN LandArea_perc DECIMAL(5, 4);
ALTER TABLE countryinfo
ADD COLUMN PopulationDensity_perc DECIMAL(5, 4);
ALTER TABLE countryinfo
ADD COLUMN ArmedForcesSize_perc DECIMAL(5, 4);
ALTER TABLE countryinfo
ADD COLUMN CPI_perc DECIMAL(5, 4);


CREATE TABLE weights(
    wid INT AUTO_INCREMENT,
    countrySize INT,
    density INT,
    army INT,
    forest INT,
    safety INT,
    politicalRights INT,
    civilLiberties INT,
    education INT,
    healthcare INT,
    economicStatus INT,
    PRIMARY KEY (wid)
);