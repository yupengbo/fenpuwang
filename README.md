需要安装的python包：
1. requests：用来做API请求，详情见 http://docs.python-requests.org/en/latest/
#djang+gunicorn部署
###一.软件安装
- 1.python 2.7  
- 2.pip: apt-get install python-pip  
- 3.django: pip install django  
- 4.gunicorn: pip install gunicorn  
- 5.requests: pip install --upgrade requests  
- 6.git  
- 7.supervisor: apt-get install supervisor  

###二.django开发环境和生产环境分离
- 1.配置文件控制：  
生产和开发环境通用的django配置：settings/common.py  
开发环境：settings/development.py  
生产环境：settings/production.py 
  
 
- 2.进程数量=cpu*2+1,详情见config/config.py如下：
<pre><code>
import multiprocessing
bind = "0.0.0.0:8888"
workers = multiprocessing.cpu_count()×2\+1
</pre></code>
- 3.开发环境服务单进程启动：  
sudo python manage.py runserver 0.0.0.0:8003 --settings=settings.development

###三.线上服务启动
1.gunicorn_start 脚本
<pre><code>
\#!/bin/bash
NAME='fenpu-mobile'                            #应用的名称
DJANGODIR=/usr/local/services/$NAME            #django项目的目录
DJANGO_SETTINGS_MODULE=settings.production     #django生产环境配置文件
\#DJANGO_SETTINGS_MODULE=settings.development   #django开发环境配置文件
DJANGO_WSGI_MODULE=wsgi                        #wsgi模块

\#log
LOGFILE=/data/$NAME/guni.log
LOGDIR=$(dirname $LOGFILE)
test -d $LOGDIR || mkdir -p $LOGDIR

echo "starting $NAME as \`whoami\`"
cd $DJANGODIR
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

\#启动Django
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $NAME \
    --config=config/config.py \
    --log-level=debug \
    --log-file=$LOGFILE 2>>$LOGFILE
                                                                      
</pre></code>
2.我们需要确保系统能够自动启动或者重启，因为系统可能会由于某些原因导致异常终止，这个任务就交给supervisor，在/etc/supervisor/conf.d/目录下创建配置文件/etc/supervisor/conf.d/fenpu-mobile.conf，用来启动监视应用程序。
<pre><code>
[program:fenpu-mobile]
command = /usr/local/services/fenpu-mobile/bin/gunicorn_start.sh
user = root
stdout_logfile = /data/fenpu-mobile/gunicorn_supervisor.log
redirect_stderr = true
</pre></code>
3.配置好了之后，supervisor重新加载配置文件
<pre><code>
$ sudo supervisorctl reread
hello: available
$ sudo supervisorctl update
hello: added process group
</pre></code>
4.同时你还可以检查app的状态、启动、停止、重启
<pre><code>
$ sudo supervisorctl status fenpu-mobile 
hello                RUNNING
$ sudo supervisorctl stopfenpu-mobile 
hello: stopped
$ sudo supervisorctl start fenpu-mobile 
hello: started
$sudo supervisorctl restart fenpu-mobile 
hello:stoped
hello:started
</pre></code>  

5.日志：supervisor、gunicorn和django的日志都在/data/fenpu-mobile下  

###四.nginx反向代理配置

