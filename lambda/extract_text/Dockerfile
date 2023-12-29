FROM public.ecr.aws/lambda/python:3.9

# RUN yum -y install poppler-utils

COPY extract_text.py requirements.txt ${LAMBDA_TASK_ROOT}
RUN python3.9 -m pip install -r requirements.txt -t "${LAMBDA_TASK_ROOT}"

CMD [ "extract_text.handler" ]
