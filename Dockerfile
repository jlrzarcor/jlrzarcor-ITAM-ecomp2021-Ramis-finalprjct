FROM continuumio/miniconda3
EXPOSE 8080
COPY environment.yml  /jlrzarcor-ITAM-ecomp2021-Ramis-finalprjct/environment.yml
RUN conda env update -f /jlrzarcor-ITAM-ecomp2021-Ramis-finalprjct/environment.yml
COPY . /jlrzarcor-ITAM-ecomp2021-Ramis-finalprjct/
CMD ["conda", "run", "--no-capture-output", "-n", "est_comp", "python", "/Docker/app.py"]
