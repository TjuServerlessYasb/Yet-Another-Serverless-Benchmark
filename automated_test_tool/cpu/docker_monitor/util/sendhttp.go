package util

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

func HttpPost(requestUrl string, requestId string, reqBody interface{}, customHeaders map[string]string) {
	byteData, err := json.Marshal(reqBody)
	if err != nil {
		fmt.Errorf("err:%v",err)
		return
	}
	body := bytes.NewReader(byteData)
	//创建post请求
	req, err := http.NewRequest("POST", requestUrl, body)
	if err != nil {
		fmt.Errorf("request uri failed:%v", err)
		return
	}
	for key, value := range customHeaders {
		req.Header.Set(key, value)
	}

	req.Header.Set("Content-Type", "application/json;charset=UTF-8")
	req.Header.Set("Connection", "close")
	if requestId != "" {
		req.Header.Set("RequestId", requestId)
	} else {
		requestId = customHeaders["X-Request-Id"]
	}

	headers, _ := json.Marshal(req.Header)
	fmt.Printf("request url:%s, headers:%s, data:%s", requestUrl, headers, byteData)
	//生成client
	client := &http.Client{}
	resp := &http.Response{}
	for i := 0; ; i++ {
		//发送请求
		resp, err = client.Do(req)
		if err != nil {
			fmt.Errorf("request url:%s, body:%s failed.Error msg:%s.", requestUrl, byteData, err)
			if i < 3 && resp != nil && resp.StatusCode == http.StatusInternalServerError {
				time.Sleep(100 * time.Millisecond)
				fmt.Printf("server return 500, try again:%d", i)
				continue
			}
			return
		}
		resp.Body.Close()
		fmt.Printf("requestId:%s response status code:%d", requestId, resp.StatusCode)
		return
	}
}
