<?php

$filename = "./test_data/huati.json";
$json_string = file_get_contents($filename);
$huati_arr = json_decode($json_string, false, 512, JSON_BIGINT_AS_STRING);

$filename = "./test_data/feeds.json";
$json_string = file_get_contents($filename);
$feeds_arr = json_decode($json_string, false, 512, JSON_BIGINT_AS_STRING);
//print_r($feeds_arr);

$result = array();
foreach($huati_arr->{'cards'}[5]->{'card_group'} as $item) {
    $result[] = $item->{'mblog'};
}

foreach($huati_arr->{'cards'} as $item) {
    if($item->{'card_type_name'} === 'feed列表') {
        $result[] = $item->{'card_group'}[0]->{'mblog'};
    }
}

//print_r($result);

$feeds_arr->{'statuses'} = $result;

$new_feeds_arr = json_encode($feeds_arr, JSON_UNESCAPED_UNICODE);

$new_feeds_arr = preg_replace('/"id":"(\d+)"/', '"id":${1}', $new_feeds_arr);
$new_feeds_arr = preg_replace('/"geo":""/', '"geo":null', $new_feeds_arr);

print($new_feeds_arr);
?>
