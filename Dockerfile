FROM centos:7

MAINTAINER showteeth

WORKDIR /orth

ADD . /orth

RUN yum -y install epel-release \
	&& yum -y install python-pip \ 
	&& yum -y install vim \
	&& wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.8.1+-x64-linux.tar.gz
	&& pip install -r requirements.txt \
	&& chmod 744 /orth/scripts/docker_blast.sh \
	&& tar -zxvf /orth/ncbi-blast-2.8.1+-x64-linux.tar.gz

ENV PATH /orth/ncbi-blast-2.8.1+/bin:$PATH


CMD /bin/bash