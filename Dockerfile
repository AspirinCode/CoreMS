FROM corilo/corems:base-mono-pythonnet AS base
WORKDIR /home/corems

COPY corems/ /home/corems/corems
COPY README.md disclaimer.txt requirements.txt setup.py /home/corems/
RUN python3 setup.py install
RUN rm -f -r /home/corems/corems
RUN rm /home/corems/setup.py

#RUN apt update && apt install -y --no-install-recommends  build-essential

FROM base AS build
COPY --from=base /home/corems /home/corems
WORKDIR /home/corems

COPY doc/notebooks/*.ipynb README.md disclaimer.txt requirements.txt SettingsCoreMS.json /home/corems/
COPY doc/examples /home/corems/examples
COPY tests/tests_data/ESI_NEG_SRFA.d/ /home/corems/ESI_NEG_SRFA.d/

RUN python3 -m pip install jupyter
ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD jupyter notebook --port=8888 --no-browser --ip=0.0.0.0 --allow-root



