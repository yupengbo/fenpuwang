#!/bin/bash
NAME='fenpu-mobile'                            #应用的名称
DJANGODIR=/usr/local/services/$NAME            #django项目的目录
DJANGO_SETTINGS_MODULE=settings.production     #django生产环境配置文件
#DJANGO_SETTINGS_MODULE=settings.development   #django开发环境配置文件
DJANGO_WSGI_MODULE=wsgi                        #wsgi模块

#log
LOGFILE=/data/$NAME/guni.log
LOGDIR=$(dirname $LOGFILE)
test -d $LOGDIR || mkdir -p $LOGDIR

echo "starting $NAME as `whoami`"
cd $DJANGODIR
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

#启动Django
exec python /usr/local/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $NAME \
    --config=config/config.py \
    --log-level=debug \
    --log-file=$LOGFILE 2>>$LOGFILE
