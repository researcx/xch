# USAGE:
# ./run.sh install - install into python virtual environment (does not currently create a virtual environment on windows)
# ./run.sh socket - run as uwsgi socket (for production use)
# ./run.sh http - run as http (for development use)
# ./run.sh windows - run as http (for development use) on windows [MUST MANUALLY `source ./xch/config/vars`]

for arg in "$@"
do
    if [ "$arg" == "install" ]
    then
        virtualenv --python=python3 venv
        source ./venv/bin/activate
        ./venv/bin/pip3 install git+https://github.com/researcx/py_thumbnailer.git
        ./venv/bin/pip3 install -e .
        mkdir -p ./xch/_rsc/f/
        mkdir -p ./xch/_rsc/t/
        mkdir -p ./logs/
        touch ./logs/global.log
        touch ./logs/summary.log
        break
    fi

    if [ "$arg" == "make-release" ]
    then
        break
    fi

    if [ "$arg" != "windows" ]
    then
        source ./venv/bin/activate
        source ./xch/config/vars
    fi

    if [ "$arg" == "pkill-flask" ]
    then
        pkill -9 flask
    fi

    if [ "$arg" == "pkill-uwsgi" ]
    then
        pkill -9 uwsgi
    fi

    if [ "$arg" == "copy-to" ]
    then
        current_time=`date +%s`
        echo "$current_time"
        backups_dir='/home/service/backups/'
        dir='/home/service/xch/xch'
        echo "creating $backups_dir$current_time"
        mkdir "$backups_dir$current_time"
        cp -fvr "$dir/database" "$backups_dir$current_time"
        cp -fvr "$dir/uploads" "$backups_dir$current_time"
        rm -rf /home/service/xch
        mkdir /home/service/xch
        rsync -av --progress . /home/service/xch --exclude venv --exclude .git
        cp -fvr "$backups_dir$current_time/database" "$dir"
        cp -fvr "$backups_dir$current_time/uploads" "$dir"
        chown -R service:service /home/service/xch
        /usr/sbin/runuser -l service -c 'export PBR_VERSION=1.2.3; cd /home/service/xch; /usr/bin/sh /home/service/xch/run.sh install >> log.txt'
        cat /home/service/xch/log.txt
    fi

    if [ "$arg" == "run-as" ]
    then
        /usr/sbin/runuser -l service -c 'export PBR_VERSION=1.2.3; cd /home/service/xch; nohup /usr/bin/sh /home/service/xch/run.sh demo > xch.log 2>&1'
    fi

    echo "=== Starting Server ==="
    if [ "$arg" == "socket" ]
    then
        echo "Running in socket mode..."
        echo "Host:" $UWSGI_HOST
        echo "Port:" $UWSGI_PORT
        uwsgi --socket $UWSGI_HOST:$UWSGI_PORT --module xch --master --enable-threads --workers $UWSGI_WORKERS --processes $UWSGI_PROCESSES --threads $UWSGI_THREADS --callab app -H venv
    elif [ "$arg" == "http" ] || [ -z "$arg" ]
    then
        export XCH_DEBUG=true
        echo "Running in http mode..."
        echo "Host:" $FLASK_HOST
        echo "Port:" $FLASK_PORT
        flask run --host=$FLASK_HOST --port=$FLASK_PORT
    fi
    if [ "$arg" == "windows" ]
    then
        export XCH_DEBUG=true
        echo "Running in http mode (WINDOWS)..."
        echo "Host:" $FLASK_HOST
        echo "Port:" $FLASK_PORT
        flask run --host=$FLASK_HOST --port=$FLASK_PORT
    fi
    if [ "$arg" == "demo" ]
    then
        export FLASK_DEBUG=false
        export XCH_DEMO=true
        echo "Running in http mode (demo)..."
        echo "Host:" $DEMO_HOST
        echo "Port:" $DEMO_PORT
        flask run --host=$DEMO_HOST --port=$DEMO_PORT
    fi
done
