# docker_openmc
A repository to build a clean OpenMC installation from a Dockerfile

## build instructions
```
docker build -t user_name/image_name:tag_name .
```
If the Dockerfile is not located at `.`, you can supply the path. If no tag is used, the tag latest will be applied to the image with the most recent build.
## For building a known stable version of OpenMC, use
```
docker build -t ligross/openmc:openmc_stable .
```
## if you want a build from no cache (sometimes useful for debugging)
```
docker build --no-cache -t ligross/openmc:openmc_stable .
```
## run the image in interactive mode with -i
```
docker container run -it image_id
```
## you can also use docker run -it <user>/repo:tag
```
docker run -it ligross/openmc:openmc_stable
```
## push instructions
```
docker push ligross/openmc:openmc_stable