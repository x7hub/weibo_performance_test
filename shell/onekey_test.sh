#! /bin/sh

DIR_NOW=`date +%s` # use as sub dir name
DIR_RESULT_TMP='result_tmp'
DIR_RESULT='result'

# store test output
mkdir -p ${DIR_RESULT}/${DIR_NOW}

# test one page
function test_one_page()
{
    target_page=$1
    rm -rf ${DIR_RESULT_TMP}/*

    # test
    ./card_performance_test.sh -f -p ${target_page}
    # save data
    cp ${DIR_RESULT_TMP}/*/gfxinfoSum.cvs ${DIR_RESULT}/${DIR_NOW}/${target_page}.cvs
    # save plot
    cp ${DIR_RESULT_TMP}/*/gfxinfo.png ${DIR_RESULT}/${DIR_NOW}/${target_page}.png
    # save count
    echo $target_page >> ${DIR_RESULT}/${DIR_NOW}/count.txt
    cat ${DIR_RESULT_TMP}/*/gfxinfoCount.txt >> ${DIR_RESULT}/${DIR_NOW}/count.txt

    sleep 3
    rm -rf ${DIR_RESULT_TMP}/*

    # test systrace
    ./systrace_test.sh -f -p ${target_page}
    # save systrace data
    cp ${DIR_RESULT_TMP}/*/trace.html ${DIR_RESULT}/${DIR_NOW}/${target_page}.html

    rm -rf ${DIR_RESULT_TMP}/*
}

# test one version
function test_one_version()
{
    test_one_page 'find'
    test_one_page 'music'
    test_one_page 'home'
    test_one_page 'topic'
}


trap "exit" SIGINT

test_one_version

