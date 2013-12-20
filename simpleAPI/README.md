SimpleAPI
=========

This project was created to check the capability of connecting Jenkins
to TestLink and henceforth, learn how they work together.

Learnings:
  - In the custom filed in TestLink, one can add any value which is available
    in Jenkins as an ENVIRONMENT VARIABLE.
  - Based on the imported Environment Variable from TestLink, one could also
    start other Jenkins builds (e.g. the env var is the name of the job itself)
  - Finally learned how to set custom classpath in build.xml and compiling
    stuff without having to use "ant -lib <mylibsdir>"
 
