FROM public.ecr.aws/lambda/python:3.9

RUN yum -y install poppler-utils

COPY thumbnail.py requirements.txt ${LAMBDA_TASK_ROOT}
RUN python3.9 -m pip install -r requirements.txt -t "${LAMBDA_TASK_ROOT}"

CMD [ "thumbnail.handler" ]
