Thesis Instructions
-----------------------------------------------

1.) CREATE Tables (FFSD_TestData2, FFSD_TrainingData2,PPSD_TrainingData2,PPSD_TestData2)
   edit tablename in code below
-----------------------------------------------
   
	CREATE TABLE [dbo].TABLENAME(
		[region] [varchar](1000) NOT NULL,
		[month_no] [varchar](1000) NOT NULL,
		[popdensity] [varchar](1000) NOT NULL,
		[ssta] [varchar](1000) NOT NULL,
		[soi] [varchar](1000) NOT NULL,
		[typhoon_distance] [varchar](1000) NOT NULL,
		[typhoon_wind] [varchar](1000) NOT NULL,
		[rainfall] [varchar](1000) NOT NULL,
		[poverty] [varchar](1000) NOT NULL,
		[ndvi] [varchar](1000) NOT NULL,
		[evi] [varchar](1000) NOT NULL,
		[daily_temp] [varchar](1000) NOT NULL,
		[nightly_temp] [varchar](1000) NOT NULL,
		[polstab] [varchar](1000) NOT NULL,
		[dengue] [varchar](1000) NOT NULL,
		[dengue_next] [varchar](1000) NOT NULL
	) ON [PRIMARY]
	GO

2.) Import CSV Files
 Right click database ThesisSampleDB 
-> Tasks -> Import Data -> Source = Flat File Source
-> SQL Server Client 11.0 or 10.0 for destination  -> Map to table PPSD_TrainingData 
Repeat but map TESTDATA to PPSD_TestData2
-----------------------------------------------
3.)Create Table FP_Rules
-----------------------------------------------

CREATE TABLE [dbo].[FP_Rules](
	[Antecedent] [varchar](1000) NOT NULL,
	[Consequent] [varchar](1000) NOT NULL,
	[Confidence] [float] NOT NULL,
	[Num_Antecedent] [int] NULL
) ON [PRIMARY]
GO

Create table Apriori_Rules2
CREATE TABLE [dbo].[Apriori_Rules2](
	[Antecedent] [varchar](1000) NOT NULL,
	[Consequent] [varchar](1000) NOT NULL,
	[Confidence] [float] NOT NULL,
	[Num_Antecedent] [int] NULL,
	[Lift] [float] NOT NULL
) ON [PRIMARY]

-----------------------------------------------
4.)Run code after succesful import
-----------------------------------------------

