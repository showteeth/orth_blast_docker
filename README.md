# orth_blast_docker

This project is used to find homologous gene pairs between two species in docker with blast+.

## software version 
* centos: 7
* blast+: 2.8.1
* Python: 2 or 3

<hr />

## Usage
There are two ways to run this project: self-construction and download constructed images.

### self-construction
You can download this repo and build a docker image follow below step:
* clone this repo:`git clone git@github.com:showteeth/orth_blast_docker.git your_dir`
* build image:`docker build -f .\Dockerfile  -t orth_project:1.0 .`
* run :`docker run -it orth_project:2.0`
* in this interactive shell:`bash /orth/scripts/docker_blast.sh`
* get results

<hr />

### download constructed images
* pull this image: `docker pull registry.cn-beijing.aliyuncs.com/showteeth/orth_blast_project:1.0`
* run :`docker run -it orth_project:2.0`
* in this interactive shell:`bash /orth/scripts/docker_blast.sh`
* get results

<hr />

## more
- [ ] 两个物种(水稻和拟南芥)拓展为任意物种

<hr />