## Abstract
Traditionally, partnerships are formed between people in the same community, and are people who have familial or social ties with each other. However, online dating has allowed people to meet and form partnerships with others who are not connected to their social group. We can model the process of forming partnerships by using an agent based model, where each agent has traits and preferences and a network of people they can marry. We want to explore different kinds of agents, specifically agents who prefer same-sex partners, and analyze the impact of online dating on their number and quality of their partnerships.

## Replication

We will replicate Ortega and Hergovich’s experiment in which they model the impact of online dating on the diversity and strength of marriages. They start with an Erdos-Renyi random graph and assign each node a social and political preference, as well as a race, racial preference, and other preferences. The agents marry by choosing their preferred partner every timestep, and if two agents point to each other, they are married and removed from the pool of available partners. Since Ortega and Hergovich assume all couples are heterosexual, we will add a percentage of people who prefer partners of the same sex. This is especially compelling because Rosenfeld and Thomas have shown that partnership rate has increased the most for middle aged or gay/lesbian individuals since the advent of online dating.

## Expected Results

We expect to see an increase in interracial marriages comparable to the results found in Ortega and Hergovich’s experiment, and we expect to replicate their findings of fewer marriages through online dating ending in divorce. We can also plot the welfare metrics (size, diversity, and size) to see if our replication of the model produces the same results. Ortega and Hergovich state that agents are heterosexual because in one-sided matching there may be no stable pairings, so we expect to see some evidence of this when adding one-sided matching by adding a percentage of people who prefer same-sex relationships. We still expect the number of interracial marriages to increase, and we expect the relationship between interracial marriages and the welfare metrics for heterosexual agents to hold for lesbian/gay/bisexual agents. 

![][img/graphs.png]

Figure 1: Sample graphs that we will plot.

## Concerns and Next Steps

One major concern is how to add agents that prefer same-sex relationships to the model- it is unclear how to model one-sided matching (should agents be able to point at only other agents who have expressed interest in dating a person of their sex?). 

Our next steps are looking over the Matlab code for the Ortega and Hergovich model to replicate it and to understand how the diversity metrics are computed. 

## Annotated Bibliography

Ortega, J., & Hergovich, P. (2017). The Strength of Absent Ties: Social Integration via Online Dating. ArXiv e-prints. Retrieved October 24, 2017, from https://arxiv.org/pdf/1709.10478.pdf.

This paper models marriages in social networks and the impact of online dating, specifically in racial diversity. Before online dating, someone usually dated people they had mutual friends with, or people in their community, which were usually racially homogenous. However, online dating allowed people to meet others outside their community, which is less racially homogenous. They generate these communities using random graphs (Erdos-Renyi), and model each node's preferences using a number between 0 and 1 for its social preferences and political preferences. The authors then analyze the models and determine if the introduction of online dating has improved the welfare of society. The finding of the model is consistent with previous findings, such as the increase in interracial couples in America and that marriages from online dating are stronger than marriages from traditional means of dating.

Rosenfeld, M. and Thomas, R. (2012). “Searching for a mate: the rise of the internet as a social intermediary,” *American Sociological Review, 77, 523-547. 

Rosenfeld and Thomas use results from the How Couples Meet and Stay Together survey to determine behavior (and changes in behavior over time) of couples with the rise of online dating. In particular, they outline differences in how heterosexual and same-sex couples use online dating. Ortega and Hergovich use this paper for providing the context for their paper, and we could use it to extend their model to same-sex couples.

Erdos, P. and Renyi, A. (1959) “On random graphs 1.” *Publicationes Matheimaticae (Debrecen)*, 6, 290-297.

Ortega and Hergovich construct random graphs using the method outlined in this paper by Erdos and Renyi, and we will be using the same method to replicate their experiment.


