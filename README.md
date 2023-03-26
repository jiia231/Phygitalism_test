# Phygitalism Test Task
## Description
Notes API with JWT authentication.  
[Tech requirements](https://github.com/phygitalism/test-task-backend)

## Stack:
1) FastAPI+uvicorn
2) SQLAlchemy
3) Alembic
4) AsyncPG
5) Nginx
6) Pre-commit

## Launch
1) Enter this command to launch tests and see coverage:
```shell
docker-compose -f docker-compose.yaml -f docker-compose.test.yaml --env-file ./.env up --build
```

2) Enter this command to launch API:
```shell
docker-compose -f docker-compose.yaml --env-file ./.env up --build
```
