#!/bin/zsh

#set test url and post data to be used in the test
URL="http://localhost:5000/api/timeline_post"
POST_DATA='name=Tester&email=Tester@test.com&content=This is your friendly neighborhood test post'

#send POST request with test data and save the response
echo "Sending POST request..."
POST_RESPONSE=$(curl -s -X POST "$URL" -d "$POST_DATA")

#check if the POST request was successful and continue if so
if [ "$(echo "$POST_RESPONSE" | jq -r '.name')" = "Tester" ]
then
    echo "POST request successful. Test post added."

    #send GET request and save the response
    echo "Sending GET request..."
    GET_RESPONSE=$(curl -s -X GET "$URL")

    #check if the GET request was successful and continue if so
    if [[ "$GET_RESPONSE" == *"Tester"* ]]
    then
        echo "GET request successful. Test post found."

        #get the ID of the test post from the GET response
        POST_ID=$(echo "$GET_RESPONSE" | jq -r '.timeline_posts[0].id')

        #send DELETE request to remove test post and save the response
        echo "Sending DELETE request..."
        DELETE_RESPONSE=$(curl -s -X DELETE "$URL/$POST_ID")

        #check if the DELETE was successful
        if [ "$(echo "$DELETE_RESPONSE" | jq -r '.message')" = "Timeline post deleted successfully" ]
        then
            echo "DELETE request successful. Test post removed."
        else
            echo "DELETE request failed. Test post not removed."
        fi
    else
        echo "GET request failed. Test post not found."
    fi
else
    echo "POST request failed. Test post not added."
fi
