# OmniCCG
**OmniCCG** is a tool for detecting and analyzing Code Clone Genealogies (CCG) in Git repositories. It allows understanding how a piece of code is replicated, evolves, and propagates throughout the history of a software project. This tool uses other two tools that detect clones, the Simian and Nicad.

### What is Code Clone Genealogy?
**Code clone genealogy** tracks how duplicated code fragments evolve through a project’s lifetime — helping identify maintenance patterns, refactoring needs, and code stability. OmniCCG enables users to:
- Detect and visualize code clones across commits
- Track clone lineage evolution (Added, Removed, Unchanged)
- Analyze clone lifespan, density, and volatility
- Identify consistent and inconsistent evolution patterns

## System Overview
OmniCCG is composed of two main parts:
| Component	|	Description |
| --- | --- |
| Backend(API) | Python-based service for clone detection, genealogy extraction, and metrics computation |
| Frontend(Web) | React-based interface for configuration, visualization, and analysis of clone genealogies |

## Tools and Technologies
<img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" width="40" height="40"/>  <img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/java/java-original.svg" width="40" height="40"/>  <img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nodejs/nodejs-plain-wordmark.svg" width="40" height="40"/>  <img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/npm/npm-original-wordmark.svg" width="40" height="40"/>  <img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/react/react-original.svg" width="40" height="40"/>  <img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/vitejs/vitejs-original.svg" width="40" height="40"/>  <img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/typescript/typescript-plain.svg" width="40" height="40"/>
          
## Installation and use		
> For exact instructions, check the README files for each subfolder. Below is a general installation guide.
### Prerequisites
- Python 3.12+
- Node.js 18+ and npm
- Poetry (for Python dependency management)
- Java 17+ (required by NiCad / Simian clone detectors)
- Git

### Clone the Repository 
 ```bash
   git clone https://github.com/denisousa/OmniCCG.git
   cd OmniCCG
```
### Running the API
Install dependencies
[os comandos]
The API will be available at: http://127.0.0.1:5000

### Running the Web
[os comandos]
Access the interface at http://localhost:8080.

## Features
## Project Structure
## Contributing

## Lincense
This project is part of the **OmniCCG** for studying code clone genealogies. All rights reserved by the maintainers.

## Authors/Contact
[nome dos desenvolvedores + link do contato]