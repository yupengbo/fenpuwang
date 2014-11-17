#!/bin/bash
NAME='fenpu_mobile_web'                            #应用的名称
DJANGODIR=/home/jihuanli/fenpu-mobile              #django项目的目录
DJANGO_SETTINGS_MODULE=settings                    #django的配置文件
DJANGO_WSGI_MODULE=wsgi                            #wsgi模块

#log
LOGFILE=/data/mobile_web/guni.log
LOGDIR=$(dirname $LOGFILE)
test -d $LOGDIR || mkdir -p $LOGDIR

echo "starting $NAME as `whoami`"
#激活python虚拟运行环境
cd $DJANGODIR
#source ../bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

#启动Django
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $NAME \
    --config=config/config.py \
    --log-level=debug \
    --log-file=$LOGFILE 2>>$LOGFILE
#gunicorn wsgi:application --bind 0.0.0.0:8001
