FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install --yes curl git g++ make unzip

RUN git clone https://github.com/lunasorcery/utf8info.git

WORKDIR utf8info

RUN make && make install

RUN apt-get remove --yes git make g++ unzip && \
    apt autoremove --yes

ENTRYPOINT ["utf8info"]
