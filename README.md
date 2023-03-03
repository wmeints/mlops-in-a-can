# MLOps in a can

Welcome to the MLOps in a can repository. This repository contains a basic MLOps environment that you can deploy with
a single command. 

## :checkered_flag: Goal of this repository

The main objective of this repository is to educate and enlighten people about MLOps and the significance of introducing
quality engineering to the working field of machine-learning and data science.

MLOps is an approach to machine learning operations that emphasizes collaboration and communication between data 
scientists and IT professionals. It is a set of best practices that help data scientists to build, test, and deploy 
machine learning models in a systematic and efficient way.

In today's world, where machine learning and data science are becoming increasingly popular, it is crucial to ensure 
that best practices are followed to deploy and run AI solutions safely. The lack of quality engineering in the machine 
learning workflow can lead to various problems such as low accuracy, poor performance, and even security issues.

Thus, this repository aims to provide a comprehensive guide on MLOps and quality engineering, which will enable 
individuals to effectively manage machine learning workflows and improve the quality and performance of the models 
they build.

------------------------------------------------------------------------------------------------------------------------

 **:warning: This is not a production setup.**

The tools in this repository are tools that we use in production at Aigency. But the docker-compose setup is not a
setup that we recommend for production use. Interested in taking this to production? [Check the docs topic](docs)

------------------------------------------------------------------------------------------------------------------------

## :rocket: Getting started

* Clone this repository to disk
* Navigate to the repository in a terminal
* Run `docker compose up -d`

You now have a fully prepared MLOps environment. Please open the following URLs in your browser to check out various
systems:

* http://localhost:5000 - MLFlow, this component tracks the machine-learning models and experiments
* http://localhost:4200 - Prefect, this component manages the machine-learning pipelines

## :book: Documentation

We've included engineering documentation with this repository that explains various aspects of the repository.
Please review the documentation topics below:

* [Scope and context](docs/scope-and-context.md) - Covers the scope of MLOps and the context of this repository
* [Solution strategy](docs/solution-strategy.md) - Covers various directions you can go in and what we used
* [Building blocks](docs/building-blocks.md) - Covers the structure of the components in this repository
* [Deployment structure](docs/deployment.md) - Covers the deployment of the various components
* [Usage scenarios](usage-scenarios.md) - Covers various day-to-day scenarios covered in this repository

