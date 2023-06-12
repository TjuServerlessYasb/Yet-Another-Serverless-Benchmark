package util

import (
	"math/rand"
	"time"
)

func RandString(len int) string {
	/*
	   rand.Seed:
	       还函数是用来创建随机数的种子,如果不执行该步骤创建的随机数是一样的，因为默认Go会使用一个固定常量值来作为随机种子。

	   time.Now().UnixNano():
	       当前操作系统时间的毫秒值
	*/
	rand.Seed(time.Now().UnixNano())
	/*
	   生成一个随机chuan
	*/
	var str string
	for i := 0; i < len; i++ {
		a := rand.Intn(26)
		X := 'A'+a
		str+=string(X)
	}
	return str
}

