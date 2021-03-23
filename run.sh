# USAGE:
# ./run.sh install - install into python virtual environment (does not currently create a virtual environment on windows)
# ./run.sh socket - run as uwsgi socket (for production use)
# ./run.sh http - run as http (for development use)
# ./run.sh windows - run as http (for development use) on windows [MUST MANUALLY `source ./vars`]

for arg in "$@"
do
    if [ "$arg" == "install" ]
    then
        virtualenv --python=python3 venv
        source venv/bin/activate
        pip3 install -e .
        mkdir -p xch/_rsc/f/
        mkdir -p xch/_rsc/t/
        mkdir -p logs/
        touch logs/global.log
        touch logs/summary.log
        break
    fi

    if [ "$arg" == "make-release" ]
    then
        break
    fi

    if [ "$arg" != "windows" ]
    then
        source venv/bin/activate
        source vars
    fi

    echo "=== Starting Server ==="
    if [ "$arg" == "socket" ]
    then
        echo "Running in socket mode..."
        echo "Host:" $XCH_HOST
        echo "Port:" $XCH_PORT
        uwsgi --socket $XCH_HOST:$XCH_PORT --module syndbb --master --enable-threads --workers $UWSGI_WORKERS --processes $UWSGI_PROCESSES --threads $UWSGI_THREADS --callab app -H venv
    elif [ "$arg" == "http" ] || [ -z "$arg" ]
    then
        echo "Running in http mode..."
        echo "Host:" $FLASK_HOST
        echo "Port:" $FLASK_PORT
        flask run --host=$FLASK_HOST --port=$FLASK_PORT
    fi
    if [ "$arg" == "windows" ]
    then
        echo "Running in http mode (WINDOWS)..."
        flask run --host=$FLASK_HOST --port=$FLASK_PORT
    fi
done
