# Building the App Container

The base Dockerfile comes with everything necessary to build and start the application as is. The application container is built using a multi stage build, where the first stage builds the wheel file, and the second stage copies the wheel from the first, then install it. 

If more libraries are needed for the application to successfully start/compile, add the packages to the `apk add` line on the second stage of the build.