# GSOC 2020 Influenza Project

## Problem statement
Reducing the impact of seasonal influenza epidemics and other pandemics such as the H1N1 is of paramount importance for public health authorities. Studies have shown that effective interventions can be taken to contain the epidemics if early detection can be made.

Seasonal influenza epidemics result in about three to five million cases of severe illness and about ​ 250,000 to 500,000 deaths worldwide each year. This is of utmost significance for public health agencies to reduce the effects of natural pandemics and epidemics such as the H1N1 influenza. Results have demonstrated that protective steps can be taken to suppress epidemics where there is early warning during outbreak germination. And monitoring and forecasting the occurrence and spread of flu in the community is critical.

In the EU, there are several government institutions which track incidents of influenza-like disease (ILI)​ by gathering statistics from sentinel care activities that provide virological(the study of viruses and the diseases) statistics as well as clinical details, such as physicians reporting on the number of patients observed presenting influenza-like disease, obtaining and releasing information on a weekly basis.

To collect data the following sources were used:

    Austria: FluNet surveillance tool
    Belgium: FluNet surveillance tool
    Germany: Survstat
    Italy: InfluNet service
    Netherlands: FluNet surveillance tool

Since assessments are produced and recorded by physicians, the procedure is almost completely manual, resulting in a period of 1 -2 weeks​ from the moment an individual becomes identified and the moment the data points are accessible in quantitative ILI statistics. It is important to provide up-to-date details about the incidence of ILI in a community in order to better administer vaccinations, staff and other healthcare services.

There have been several attempts at gathering non-traditional, digital information to be used to predict the current or future levels of ILI, and other diseases, in a population.
These include monitoring call volumes to telephone triage advice lines, over the counter drug sales, and patients visit logs to Physicians for flu shots along with several others.

Google Flu Trends was initially very effective in predicting ILI incidence, however, it has been seen to waver in the face of the 2009 H1N1 swine influenza pandemic (pH1N1) due to dramatically expanded media coverage across the pandemic.

It utilizes aggregated web search queries pertaining to influenza to build a comprehensive model that can estimate nationwide
as well as state-level ILI activity

## Project Description
This project is majorly based on the findings of David J. McIver and John S. Brownstein. In their research paper titled Wikipedia Usage Estimates Prevalence of Influenza-Like Illness in the United States in Near Real-Time, they mention how it’s possible to use Wikipedia pageviews data to estimate the incidence of influenza related illnesses.

It has previously been shown that Wikipedia can be a useful tool to monitor the emergence of breaking news stories, to track what topics are ‘‘trending’’ in
the public sphere, and to develop tools for natural language processing. Furthermore, Wikipedia makes all of this information public and freely available, greatly increasing and expediting any potential research studies that aim to make use of their data.

In an attempt to use Wikipedia data to estimate ILI activity, some researchers compiled a list of Wikipedia articles that were likely to be related to influenza, influenza-like activity, or to health in general. These articles were selected based on previous knowledge of the subject area, previously published materials, and expert opinion. This data is all available in this zenodo dataset.

I will be building the web-tool first using some kind of a Linear regression or a Random Forest Regression method and then later add the Poisson Regression to Shogun and implement that into the web-tool.

The basic workflow is going to be as follows:

* Build a web-application using Flask for the backend api.
* Write code for the GLM algorithm.
* Integrate the two.

This will be done under the guidance of my mentors, Lea Goetz and Giovanni De Toni.
