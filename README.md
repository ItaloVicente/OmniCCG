# Repository History Analyzer and Clone Genealogies

This project generates the commit history of a Git repository and
performs clone genealogy analysis on **production code** and **test
code**, inspired by the article:\
***"A Comparative Study of Code Clone Genealogies in Test Code and
Production Code"***

------------------------------------------------------------------------

## Project Structure

-   The repository to be analyzed should be placed in:

        workspace/repo

-   The commit history will be saved in:

        gitHistory.txt

-   The repository code will be separated into datasets:

    -   `dataset/production` → production code\
    -   `dataset/test` → test code

------------------------------------------------------------------------

## Configuration

The analyzer behavior can be adjusted through the following settings:

``` python
# Project settings
GIT_URL = "https://github.com/apache/thrift.git"  # URL of the Git repository to clone
COMMIT_INTERVAL = 10      # How often a commit should be analyzed (1 = every commit)
MAX_COMMITS = 10          # Maximum number of commits to analyze
USE_ICLONES = False       # Enable iClones for clone detection
LANGUAGE = "java"         # Project language ("java" or "c")
```

------------------------------------------------------------------------

## Output: Clone Genealogies

The results of the analysis are stored in two sets of files:

-   **Production**
    -   `P_LIN_DATA` → raw data\
    -   `P_RES_FILE` → consolidated results file
-   **Test**
    -   `T_DENS_DATA` → raw data\
    -   `T_RES_FILE` → consolidated results file

------------------------------------------------------------------------

## Workflow Summary

1.  Clone the repository defined in `GIT_URL`.\
2.  Generate commit history in `gitHistory.txt`.\
3.  Extract and separate the code into `dataset/production` and
    `dataset/test`.\
4.  Run clone analysis according to the configuration.\
5.  Save genealogies into the corresponding output files.


# Link
https://figshare.com/articles/dataset/A_Comparative_Study_of_Code_Clone_Genealogies_in_Test_Code_and_Production_Code_-_Replication_Package/17206997?file=34642655

