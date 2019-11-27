FROM gitlab.pnnl.gov:4567/mass-spectrometry/corems:corems-base-mono

WORKDIR /home/CoreMS

COPY corems/ /home/CoreMS/corems/
COPY requirements.txt LICENSE README.md setup.py doc/CoreMS_Tutorial.ipynb /home/CoreMS/
COPY lib/ /home/CoreMS/lib/
COPY support_code/ /home/CoreMS/support_code/
COPY ESI_NEG_SRFA.d/ /home/CoreMS/ESI_NEG_SRFA.d/
RUN apt update && apt install -y --no-install-recommends  build-essential
RUN python3 -c "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('win_only/__init__.py')]"
RUN python3 -m pip install -r requirements.txt
RUN python3 setup.py install 
RUN python3 -m pip install jupyter
CMD jupyter notebook --ip 0.0.0.0 --no-browser --allow-root


