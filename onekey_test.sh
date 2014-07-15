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
    ./card_performance_test.sh -f -p ${target_page}
    cp ${DIR_RESULT_TMP}/*/gfxinfoSum.cvs ${DIR_RESULT}/${DIR_NOW}/${target_page}.cvs
    cp ${DIR_RESULT_TMP}/*/gfxinfo.png ${DIR_RESULT}/${DIR_NOW}/${target_page}.png
}

test_one_page 'find'
test_one_page 'topic'
test_one_page 'music'
test_one_page 'home'
